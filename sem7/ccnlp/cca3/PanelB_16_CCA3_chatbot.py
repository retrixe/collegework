"""Proverb chatbot for CCA3 (Group 16, Panel B).

One chat loop over the three CCA3 experiments:
  * a situation in plain words      -> reverse retrieval (suggest)      [Sahish Nagulwar]
  * "figurative: <sentence>"        -> idiom usage detection            [Ibrahim Ansari]
  * "explain: <proverb>"            -> language-model interpretation    [Chayan Raj Bharati]
Commands: /lang <marathi|hindi|assamese|all>, /llm on|off, /help, /quit

Run from the cca3 folder:  python PanelB_16_CCA3_chatbot.py
No dependencies beyond the ones the notebooks already use.
"""
import json
import re
import sys

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import make_pipeline

LANGS = [('marathi', 'Marathi'), ('hindi', 'Hindi'), ('assamese', 'Assamese')]
CORPUS = '../cca1/corpus/PanelB_16_{}_proverbs.csv'
MAGPIE = 'external/MAGPIE_filtered_split_random.jsonl'
LLM = 'Qwen/Qwen2.5-0.5B-Instruct'


class ProverbBot:
    def __init__(self):
        print('loading corpora and LaBSE ...', flush=True)
        from sentence_transformers import SentenceTransformer
        self.labse = SentenceTransformer('sentence-transformers/LaBSE')
        self.corp = {}
        for l, L in LANGS:
            df = pd.read_csv(CORPUS.format(l))
            df = df[df.commentary.fillna('').str.len() > 20].reset_index(drop=True)
            self.corp[l] = {'df': df, 'D_labse': self.embed(df.commentary), 'P_labse': self.embed(df.literal_en)}
        print('training the idiom detector on MAGPIE ...', flush=True)
        rows = [json.loads(x) for x in open(MAGPIE, encoding='utf8')]
        train = [m for m in rows if m['label'] in ('i', 'l') and m['split'] == 'training']
        mag = pd.DataFrame([{'s': m['context'][2], 'y': {'i': 'idiomatic', 'l': 'literal'}[m['label']]} for m in train])
        # third class: the neighbouring BNC sentences in each context window, which carry no annotated idiom
        plain = pd.Series([c for m in train for c in (m['context'][1], m['context'][3]) if 5 <= len(c.split()) <= 40]).drop_duplicates()
        plain = plain.sample(min(len(plain), 15000), random_state=42)
        # two-class detector: the one reported in Section 2.6.2 (figurative vs literal use of an idiom)
        self.det = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, min_df=2),
                                 LogisticRegression(max_iter=3000, class_weight='balanced'))
        self.det.fit(mag.s, mag.y)
        # three-class spotter for running text: adds 'plain' so sentences with no idiom are not forced into a class
        mag3 = pd.concat([mag, pd.DataFrame({'s': plain.values, 'y': 'plain'})], ignore_index=True)
        self.det3 = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, min_df=2),
                                  LogisticRegression(max_iter=3000, class_weight='balanced'))
        self.det3.fit(mag3.s, mag3.y)
        self.llm = None
        self.llm_on = True
        self.lang = 'all'
        print('ready.\n', flush=True)

    def embed(self, texts):
        return self.labse.encode(list(texts), show_progress_bar=False, normalize_embeddings=True)

    # ---- objective 1: situation -> proverb (Sahish) ----
    def suggest(self, query, k=3):
        q = self.embed([query])
        out = []
        for l, L in LANGS:
            if self.lang not in ('all', l):
                continue
            c = self.corp[l]
            sims = cosine_similarity(q, c['D_labse'])[0]
            for i in np.argsort(-sims)[:k]:
                r = c['df'].iloc[i]
                out.append((L, float(sims[i]), r.proverb_translit, r.literal_en, r.commentary))
        out.sort(key=lambda t: -t[1])
        return out[:k if self.lang != 'all' else 2 * k]

    # ---- objective 2: figurative or literal (Ibrahim) ----
    def is_figurative(self, sentence):
        proba = self.det.predict_proba([sentence])[0]
        return dict(zip(self.det.classes_, proba))

    def scan(self, paragraph):
        """Running-text detection: split a paragraph into sentences, score each one,
        and for the figurative ones look up the closest proverb in the corpora."""
        sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', paragraph.strip()) if s.strip()]
        lines = [f'[idiom detection, running text] {len(sents)} sentences']
        for i, s in enumerate(sents, 1):
            pr = dict(zip(self.det3.classes_, self.det3.predict_proba([s])[0]))
            lab = max(pr, key=pr.get)
            mark = {'idiomatic': 'FIGURATIVE', 'literal': 'literal   ', 'plain': 'plain     '}[lab]
            lines.append(f'  {i}. {mark} (idiomatic {pr["idiomatic"]:.2f}, literal {pr["literal"]:.2f}, plain {pr["plain"]:.2f})  {s}')
            if lab == 'idiomatic':
                clauses = [c.strip() for c in re.split(r'[,;:]|\bthey say\b|\bsays?\b|\bthat\b', s) if len(c.split()) >= 3] + [s]
                best = max((self.lookup(c) for c in clauses), key=lambda t: t[0])
                score, L, row = best
                if score >= 0.45:
                    lines.append(f'       matches {L} proverb "{row.proverb_translit}" ({score:.2f}): {row.commentary[:120]}')
        return '\n'.join(lines)

    # ---- objective 3: what does it mean (Chayan) ----
    def lookup(self, text):
        q = self.embed([text])
        best = None
        for l, L in LANGS:
            c = self.corp[l]
            sims = cosine_similarity(q, c['P_labse'])[0]
            i = int(np.argmax(sims))
            tf_hit = c['df'].proverb_translit.str.lower().str.contains(re.escape(text.lower()[:25])).any()
            score = float(sims[i]) + (0.3 if tf_hit else 0)
            if best is None or score > best[0]:
                best = (score, L, c['df'].iloc[i])
        return best

    def explain(self, text):
        if not self.llm_on:
            return None
        if self.llm is None:
            print('  (loading Qwen2.5-0.5B-Instruct, first use only) ...', flush=True)
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
            tok = AutoTokenizer.from_pretrained(LLM); tok.padding_side = 'left'
            self.llm = (tok, AutoModelForCausalLM.from_pretrained(LLM, dtype=torch.float32), torch)
        tok, mdl, torch = self.llm
        prompt = f'Explain the meaning of this proverb in one sentence: "{text}"'
        chat = tok.apply_chat_template([{'role': 'user', 'content': prompt}], tokenize=False, add_generation_prompt=True)
        enc = tok([chat], return_tensors='pt')
        with torch.no_grad():
            gen = mdl.generate(**enc, max_new_tokens=48, do_sample=False)
        return tok.decode(gen[0][enc['input_ids'].shape[1]:], skip_special_tokens=True).strip()

    # ---- routing ----
    def reply(self, msg):
        m = msg.strip()
        low = m.lower()
        if not m:
            return ''
        if low in ('/quit', '/exit', 'quit', 'exit'):
            return None
        if low == '/help':
            return ('Type a situation to get fitting proverbs.\n'
                    '  figurative: <sentence>   is the sentence using an idiom figuratively or literally?\n'
                    '  scan: <paragraph>        flag the figurative sentences in running text and match them to proverbs\n'
                    '  explain: <proverb>       what does this proverb mean? (model answer next to the recorded one)\n'
                    '  /lang marathi|hindi|assamese|all    /llm on|off    /quit')
        if low.startswith('/lang'):
            arg = low.split()[-1] if len(low.split()) > 1 else 'all'
            if arg in ('all', 'marathi', 'hindi', 'assamese'):
                self.lang = arg
                return f'language set to {arg}'
            return 'use /lang marathi | hindi | assamese | all'
        if low.startswith('/llm'):
            self.llm_on = not low.endswith('off')
            return f'language model {"on" if self.llm_on else "off"}'
        if low.startswith('scan:') or (len(re.findall(r'[.!?](\s|$)', m)) >= 2 and not low.startswith(('explain', 'what does'))):
            return self.scan(m.split(':', 1)[1] if low.startswith('scan:') else m)
        if low.startswith('figurative:') or low.startswith('is this figurative'):
            sent = m.split(':', 1)[1].strip() if ':' in m else m
            pr = self.is_figurative(sent)
            lab = max(pr, key=pr.get)
            return f'[idiom detection] {lab} usage (idiomatic {pr["idiomatic"]:.2f}, literal {pr["literal"]:.2f})'
        if low.startswith('explain:') or re.match(r'^(what does|what is the meaning of)', low):
            text = m.split(':', 1)[1].strip() if ':' in m else re.sub(r'^(what does|what is the meaning of)\s*', '', m, flags=re.I).rstrip('?').strip()
            text = re.sub(r'\s+mean$', '', text).strip('"\' ')
            score, L, row = self.lookup(text)
            lines = ['[interpretation]']
            known = score >= 0.6
            if known:
                lines.append(f'  closest corpus entry ({L}): "{row.proverb_translit}" / {row.literal_en}')
                lines.append(f'  recorded meaning: {row.commentary}')
            else:
                lines.append('  not found in the corpora (closest match too weak), so only the model can answer')
            ans = self.explain(text)
            if ans is None:
                lines.append('  language model is off (/llm on to enable)')
            else:
                lines.append(f'  Qwen2.5-0.5B says: {ans}')
                if known:
                    sim = float((self.embed([ans]) * self.embed([row.commentary])).sum())
                    lines.append(f'  similarity of model answer to recorded meaning: {sim:.2f}')
            return '\n'.join(lines)
        hits = self.suggest(m)
        lines = ['[reverse retrieval] proverbs for that situation:']
        for L, s, pr, lit, mean in hits:
            lines.append(f'  {L} ({s:.2f}): "{pr}"\n      literal: {lit}\n      meaning: {mean}')
        return '\n'.join(lines)


def main():
    bot = ProverbBot()
    print('Proverb bot (Group 16). Type a situation, "figurative: ...", "explain: ...", or /help.')
    interactive = sys.stdin.isatty()
    while True:
        try:
            line = input('you> ') if interactive else sys.stdin.readline()
        except EOFError:
            break
        if not interactive:
            if not line:
                break
            print(f'you> {line.rstrip()}')
        r = bot.reply(line)
        if r is None:
            print('bye'); break
        if r:
            print('bot> ' + r + '\n')


if __name__ == '__main__':
    main()
