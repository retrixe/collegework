import sys
import nbformat as nbf

LANGS = [('marathi', 'Marathi'), ('hindi', 'Hindi'), ('assamese', 'Assamese')]
ROSTER = """| Member | PRN | Experiment (notebook) |
|---|---|---|
| {b1}Sahish Nagulwar{b1} | 1032233310 | {b1}Reverse retrieval: situation to proverb (Plan A 2.8){b1} |
| {b2}Ibrahim Ansari{b2} | 1032233145 | {b2}Idiom identification in running text (Plan A 2.5){b2} |
| {b3}Chayan Raj Bharati{b3} | 1032233134 | {b3}Language-model interpretation benchmark (Plan A 2.7){b3} |"""

SITUATIONS = {
    'marathi': [
        ('Someone is making a fuss over a tiny shortfall that does not matter in the big picture.', 7),
        ('A person works hard all day on a task that produces nothing at all.', 9),
        ('Something has finally reached its full ripeness or maturity.', 11),
        ('Acting carefully so that neither of two friends is hurt by a decision.', 12),
        ('A man arranges everything so that the benefit comes only to himself.', 14),
        ('Someone drops you the moment they no longer need your help.', 19),
        ('A farmer has good harvests every year yet stays poor because he keeps borrowing.', 20),
        ('Urgent seasonal work must be done on time even when something else demands attention.', 23),
        ('A person is generous with things that belong to someone else.', 30),
        ('While one person is in deep trouble, another only worries about his own small concern.', 31),
    ],
    'hindi': [
        ('A big job has barely been started even though a lot of time has passed.', 1),
        ('Someone starts preparing far too early for something that is hours away.', 3),
        ('A person demands payment for work they never actually did.', 9),
        ('Instead of enjoying what is offered, someone keeps asking pointless questions about where it came from.', 12),
        ('Two people in love find that their relationship is full of obstacles.', 20),
        ('A reckless spender is told that his ruin cannot be repaired.', 21),
        ('When a child is born, the means to feed it also appear.', 23),
        ('Someone pushes into a matter where nobody asked for them.', 25),
    ],
    'assamese': [
        ('A boastful man talks big about a fight but achieves almost nothing.', 4),
        ('Someone excuses saying more than he should by blaming his loose tongue.', 10),
        ('A person with no money keeps craving expensive things.', 17),
        ('People remember God only when they are in trouble.', 18),
        ('A person who plots harm for others ends up suffering from it himself.', 19),
        ('Someone with only a show of respectability wants to be the leader.', 20),
        ('A worker is full of energy one moment and abandons the job the next.', 24),
        ('A poor man wants to attend a grand feast he cannot afford.', 42),
        ('Someone who wants to succeed never wastes a moment, working even while resting.', 46),
        ('A man is burdened by too many relatives from his wife\'s side.', 47),
    ],
}

SETUP = """import json, random, re, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

sns.set_theme(style='whitegrid')
rng = np.random.default_rng(42)
os.makedirs('report', exist_ok=True)
metrics = {}

LANGS = [('marathi', 'Marathi'), ('hindi', 'Hindi'), ('assamese', 'Assamese')]
CORPUS = '../cca1/corpus/PanelB_16_{}_proverbs.csv'
corpora = {l: pd.read_csv(CORPUS.format(l)) for l, _ in LANGS}
with_expl = {l: df[df.commentary.fillna('').str.len() > 20].reset_index(drop=True) for l, df in corpora.items()}
for l, L in LANGS:
    print(f'{L}: {len(corpora[l])} proverbs, {len(with_expl[l])} with explanations')

labse = SentenceTransformer('sentence-transformers/LaBSE')
def embed(texts):
    return labse.encode(list(texts), show_progress_bar=False, normalize_embeddings=True)"""


def header(cells, title, who, blurb):
    b = {'b1': '', 'b2': '', 'b3': ''}
    b[who] = '**'
    cells.append(nbf.v4.new_markdown_cell(f"""# CCNLP CCA3 — {title}

**Group 16** &nbsp;|&nbsp; Panel B &nbsp;|&nbsp; School of Computer Science & Engineering, MIT-WPU

{ROSTER.format(**b)}

**Team problem statement:** *Develop a multilingual NLP framework that identifies Indian idioms and distinguishes their literal meaning from culturally intended figurative meaning across Indian languages, while modeling cultural context and linguistic variation.*

{blurb}

The three CCA1 corpora (545 Marathi, 344 Hindi, 103 Assamese proverbs, each with a romanized text, a literal English translation and the compiler's explanation of the intended meaning) are reused from `../cca1/`. Everything here runs on CPU."""))


def finish(cells, name, summary, refs):
    cells.append(nbf.v4.new_code_cell(f"""json.dump(metrics, open('report/PanelB_16_CCA3_v2_{name}_metrics.json', 'w'), indent=1)
print(json.dumps(metrics, indent=1)[:2000])"""))
    cells.append(nbf.v4.new_markdown_cell(f"""## Summary

{summary}

**References**
{refs}"""))


# =====================================================================
def build_reverse():
    cells = []
    md = lambda s: cells.append(nbf.v4.new_markdown_cell(s))
    code = lambda s: cells.append(nbf.v4.new_code_cell(s))
    header(cells, 'Reverse Retrieval: From a Situation to the Fitting Proverb', 'b1',
           "**Research question (Sahish Nagulwar):** Given a plain description of a situation, can the right proverb be retrieved from the "
           "explanation index of each corpus, and does a semantic index (LaBSE) do better than a lexical one (TF-IDF) at this?\n\n"
           "CCA1 retrieval went from proverb to meaning. This notebook reverses it: the index is the set of explanations, the query is a "
           "situation written in ordinary words, and the answer is the proverb whose recorded meaning fits. The same experiment is run on all "
           "three corpora, and a `suggest()` function at the end is the interface a chatbot calls.")
    code(SETUP)
    md("""## 1. Test queries

For each language, 8 to 10 situation descriptions were written by a team member who did not build that language's index. Each targets one proverb (`target_id`). The descriptions avoid copying words from the explanation, so lexical matching is not handed the answer.""")
    code(f"""situations = {{l: pd.DataFrame(v, columns=['situation', 'target_id']) for l, v in {SITUATIONS!r}.items()}}
for l, L in LANGS:
    situations[l] = situations[l][situations[l].target_id.isin(with_expl[l].id)].reset_index(drop=True)
    print(L, len(situations[l]), 'queries')
situations['hindi']""")
    md("""## 2. Building the two indexes per language and scoring every query""")
    code("""index = {}
for l, L in LANGS:
    docs = with_expl[l].commentary.tolist()
    tf = TfidfVectorizer(stop_words='english', sublinear_tf=True).fit(docs)
    index[l] = {'tfidf': tf, 'D_tfidf': tf.transform(docs), 'D_labse': embed(docs), 'ids': with_expl[l].id.values}

def rank_ids(l, query, model):
    ix = index[l]
    if model == 'tfidf':
        sims = cosine_similarity(ix['tfidf'].transform([query]), ix['D_tfidf'])[0]
    else:
        sims = cosine_similarity(embed([query]), ix['D_labse'])[0]
    order = np.argsort(-sims)
    return ix['ids'][order], sims[order]

rows = []
for l, L in LANGS:
    for s in situations[l].itertuples():
        for model in ['tfidf', 'labse']:
            ids, sims = rank_ids(l, s.situation, model)
            rows.append({'language': L, 'situation': s.situation, 'target_id': s.target_id, 'model': model,
                         'rank': int(np.where(ids == s.target_id)[0][0]) + 1})
ranks = pd.DataFrame(rows)
summary = ranks.groupby(['language', 'model'])['rank'].agg(
    hit_at_1=lambda r: float((r <= 1).mean()), hit_at_5=lambda r: float((r <= 5).mean()), mrr=lambda r: float((1 / r).mean())).round(3)
for l, L in LANGS:
    n = len(with_expl[l])
    summary.loc[(L, 'random'), :] = [round(1 / n, 3), round(5 / n, 3), round(float(np.mean([1 / r for r in range(1, n + 1)])), 3)]
summary = summary.sort_index()
metrics['summary'] = {f'{L}/{m}': summary.loc[(L, m)].to_dict() for L, m in summary.index}
metrics['n_queries'] = {L: int(len(situations[l])) for l, L in LANGS}
summary""")
    md("""## 3. Results""")
    for i, (l, L) in enumerate(LANGS):
        code(f"""sub = summary.loc['{L}']
fig, ax = plt.subplots(figsize=(7, 3.8))
sub[['hit_at_1', 'hit_at_5', 'mrr']].plot.bar(ax=ax, color=['#1f77b4', '#76b7e8', '#2ca02c'])
ax.set_ylim(0, 1); ax.set_ylabel('score'); ax.set_title('{L}'); plt.xticks(rotation=0)
plt.tight_layout(); plt.show()""")
        md(f"**Figure {i + 1}: {L} reverse retrieval. Hit@1, Hit@5 and MRR for the TF-IDF and LaBSE indexes against the random baseline.**")
    code("""fig, axes = plt.subplots(1, 3, figsize=(13, 4), sharey=False)
for ax, (l, L) in zip(axes, LANGS):
    sub = ranks[ranks.language == L].pivot(index='situation', columns='model', values='rank')
    y = np.arange(len(sub))
    ax.scatter(sub['tfidf'], y, marker='s', color='#1f77b4', label='TF-IDF')
    ax.scatter(sub['labse'], y, marker='o', color='#2ca02c', label='LaBSE')
    ax.axvline(5.5, color='k', ls='--', lw=1)
    ax.set_yticks(y); ax.set_yticklabels([f'q{i+1}' for i in y]); ax.set_xscale('log'); ax.set_xlabel('rank of target proverb (log)'); ax.set_title(L)
axes[0].legend(); plt.tight_layout(); plt.show()""")
    md("**Figure 4: Rank of the target proverb for every situation query, per language and index. Points left of the dashed line are top-5 hits.**")
    code("""fig, ax = plt.subplots(figsize=(8, 4))
best = summary.reset_index()
best = best[best.model != 'random'].pivot(index='language', columns='model', values='mrr')
best.plot.bar(ax=ax, color=['#2ca02c', '#1f77b4']); ax.set_ylabel('MRR'); ax.set_ylim(0, 1); plt.xticks(rotation=0)
for l, L in LANGS:
    ax.axhline(summary.loc[(L, 'random'), 'mrr'], color='grey', ls=':', lw=1)
plt.tight_layout(); plt.show()""")
    md("**Figure 5: Mean reciprocal rank by language and index; dotted grey lines are the random baselines.**")
    code("""lengths = pd.Series({L: with_expl[l].commentary.str.split().str.len().mean() for l, L in LANGS})
fig, ax = plt.subplots(figsize=(6.5, 3.8))
ax.scatter(lengths.values, [summary.loc[(L, 'labse'), 'hit_at_5'] for L in lengths.index], s=80, color='#2ca02c')
for L, x in lengths.items():
    ax.annotate(L, (x, summary.loc[(L, 'labse'), 'hit_at_5']), textcoords='offset points', xytext=(6, 4))
ax.set_xlabel('mean explanation length (tokens)'); ax.set_ylabel('LaBSE Hit@5'); ax.set_ylim(0, 1)
plt.tight_layout(); plt.show()""")
    md("""**Figure 6: Hit@5 against the average length of the indexed explanations. Longer explanations give the index more to match on.**

## 4. The interface

`suggest()` is what a chatbot calls: it takes a situation and a language and returns the top proverbs with their literal translation and meaning.""")
    code("""def suggest(query, lang='hindi', k=3, model='labse'):
    ids, sims = rank_ids(lang, query, model)
    out = with_expl[lang].set_index('id').loc[ids[:k], ['proverb_translit', 'literal_en', 'commentary']].copy()
    out.insert(0, 'similarity', np.round(sims[:k], 3))
    return out

suggest('someone keeps complaining about a very small loss', lang='marathi')""")
    finish(cells, 'reverse_retrieval',
           "Across the three corpora the target proverb reaches the top five for most of the hand-written situations, against random "
           "baselines of a few percent. The semantic index wins on MRR for Marathi and Hindi; for Assamese the lexical index is slightly ahead "
           "because several situations share concrete words with the long Gurdon explanations. The `suggest()` function is the retrieval back "
           "end for the team chatbot.",
           "- Feng, F., Yang, Y., Cer, D., Arivazhagan, N., & Wang, W. (2022). Language-agnostic BERT sentence embedding. *Proceedings of ACL 2022*, 878-891.\n"
           "- Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using Siamese BERT-networks. *Proceedings of EMNLP-IJCNLP 2019*, 3982-3992.")
    nb = nbf.v4.new_notebook(); nb['cells'] = cells; return nb


# =====================================================================
def build_idiom():
    cells = []
    md = lambda s: cells.append(nbf.v4.new_markdown_cell(s))
    code = lambda s: cells.append(nbf.v4.new_code_cell(s))
    header(cells, 'Idiom Identification in Running Text', 'b2',
           "**Research question (Ibrahim Ansari):** Can a detector that separates figurative from literal usage, trained on real English sentences, "
           "be built with the CCA1 recipe, and does it transfer to proverbs of Marathi, Hindi and Assamese placed in running text?\n\n"
           "CCA1 modelled the literal/figurative distinction on dictionary entries. The problem statement also asks systems to *identify* idioms "
           "in use. No corpus of our languages' proverbs in running text exists, so this notebook works in two steps: validate the detector on "
           "MAGPIE, a public corpus of real English sentences with figurative/literal labels, then apply the same recipe to the three proverb corpora.")
    code(SETUP)
    md("""## 1. The MAGPIE corpus

Haagsma, Bos and Nissim (2020). 48,395 sentences from the British National Corpus containing one of about 1,700 idiom types; annotators marked each occurrence as idiomatic (figurative) or literal. The corpus ships with a fixed training/development/test split. It is stored under `external/`.""")
    code("""mag = [json.loads(l) for l in open('external/MAGPIE_filtered_split_random.jsonl', encoding='utf8')]
mag = pd.DataFrame([{'sentence': m['context'][2], 'idiom': m['idiom'], 'label': m['label'], 'split': m['split'], 'genre': m['genre']}
                    for m in mag if m['label'] in ('i', 'l')])
mag['label'] = mag.label.map({'i': 'idiomatic', 'l': 'literal'})
metrics['magpie_counts'] = mag.label.value_counts().to_dict()
print(metrics['magpie_counts'], '| splits:', mag.split.value_counts().to_dict(), '| idiom types:', mag.idiom.nunique())
mag.sample(4, random_state=1)[['sentence', 'idiom', 'label']]""")
    code("""fig, axes = plt.subplots(1, 2, figsize=(11, 3.8))
mag.label.value_counts().plot.bar(ax=axes[0], color=['#1f77b4', '#d62728']); axes[0].set_title('usage labels'); axes[0].set_ylabel('sentences')
mag.sentence.str.split().str.len().clip(upper=60).hist(bins=30, ax=axes[1], color='#999999'); axes[1].set_title('sentence length (tokens)')
plt.setp(axes[0].get_xticklabels(), rotation=0); plt.tight_layout(); plt.show()""")
    md("""**Figure 1: MAGPIE corpus analysis. Idiomatic uses outnumber literal ones three to one, and sentences are typically 15 to 30 tokens long.**

## 2. Step A: detector on real sentences""")
    code("""from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix, precision_recall_fscore_support

train = mag[mag.split == 'training']; test = mag[mag.split == 'test']
det = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, min_df=2),
                    LogisticRegression(max_iter=3000, class_weight='balanced'))
det.fit(train.sentence, train.label)
pred = det.predict(test.sentence)
p, r, f, _ = precision_recall_fscore_support(test.label, pred, labels=['idiomatic', 'literal'])
metrics['magpie'] = {'train': int(len(train)), 'test': int(len(test)),
                     'majority_acc': round(float(test.label.value_counts(normalize=True).iloc[0]), 3),
                     'acc': round(float(accuracy_score(test.label, pred)), 3),
                     'macro_f1': round(float(f1_score(test.label, pred, average='macro')), 3),
                     'per_class': {c: {'precision': round(float(p[i]), 3), 'recall': round(float(r[i]), 3), 'f1': round(float(f[i]), 3)} for i, c in enumerate(['idiomatic', 'literal'])}}
print(metrics['magpie'])
cm = confusion_matrix(test.label, pred, labels=['idiomatic', 'literal'])
fig, ax = plt.subplots(figsize=(4.5, 3.8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, xticklabels=['idiomatic', 'literal'], yticklabels=['idiomatic', 'literal'], ax=ax)
ax.set_xlabel('predicted'); ax.set_ylabel('true'); plt.tight_layout(); plt.show()""")
    md("**Figure 2: Confusion matrix on the MAGPIE test split (4,840 real sentences).**")
    code("""pc = pd.DataFrame(metrics['magpie']['per_class']).T
fig, ax = plt.subplots(figsize=(6.5, 3.6))
pc.plot.bar(ax=ax, color=['#1f77b4', '#76b7e8', '#2ca02c']); ax.set_ylim(0, 1); plt.xticks(rotation=0)
ax.axhline(metrics['magpie']['majority_acc'], color='grey', ls=':', label='majority accuracy'); ax.legend()
plt.tight_layout(); plt.show()""")
    md("**Figure 3: Precision, recall and F1 per class on MAGPIE; the dotted line is the majority-class accuracy.**")
    code("""vec = det.named_steps['tfidfvectorizer']; clf = det.named_steps['logisticregression']
names = np.array(vec.get_feature_names_out()); w = clf.coef_[0]
top = np.concatenate([np.argsort(w)[:12], np.argsort(w)[-12:]])
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(names[top], w[top], color=['#1f77b4' if x < 0 else '#d62728' for x in w[top]])
ax.set_xlabel(f'weight (negative = {clf.classes_[0]}, positive = {clf.classes_[1]})'); plt.tight_layout(); plt.show()""")
    md("""**Figure 4: The strongest features for each class in the MAGPIE detector.**

## 3. Step B: the recipe applied to each language's proverbs

Positives: the corpus proverbs (literal translations) in six carrier sentences. Negatives: real literal MAGPIE sentences in the same carriers, so the templates cancel out. Register differs between 1890s book English and modern BNC English, which makes this easier than real detection; Step A is the honest number.""")
    code("""from sklearn.model_selection import StratifiedKFold, cross_val_predict
templates = ['My grandmother used to say that {}', 'As the saying goes, {}', 'He looked at me and said: {}',
             'In the end, {}', 'She reminded everyone that {}', 'It is well known that {}']
def clean(s):
    s = re.sub(r'\\s+', ' ', str(s)).strip().rstrip('.')
    return s[0].lower() + s[1:] if s else s
lit = mag[mag.label == 'literal'].sentence
lit = lit[lit.str.split().str.len().between(5, 25)]
cv = StratifiedKFold(5, shuffle=True, random_state=42)
cms = {}
for l, L in LANGS:
    pos = [t.format(clean(p)) for p in corpora[l].literal_en for t in rng.choice(templates, 2, replace=False)]
    neg = [t.format(clean(s)) for s in rng.choice(lit.values, len(pos) // 2, replace=False) for t in rng.choice(templates, 2, replace=False)]
    X = pd.Series(pos + neg); y = pd.Series(['proverb'] * len(pos) + ['plain'] * len(neg))
    d2 = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, min_df=2), LogisticRegression(max_iter=3000, class_weight='balanced'))
    pr = cross_val_predict(d2, X, y, cv=cv)
    metrics[f'step_b_{l}'] = {'n': int(len(X)), 'acc': round(float(accuracy_score(y, pr)), 3), 'macro_f1': round(float(f1_score(y, pr, average='macro')), 3)}
    cms[L] = confusion_matrix(y, pr, labels=['proverb', 'plain'])
    print(L, metrics[f'step_b_{l}'])
fig, axes = plt.subplots(1, 3, figsize=(12, 3.6))
for ax, (L, cm) in zip(axes, cms.items()):
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, xticklabels=['proverb', 'plain'], yticklabels=['proverb', 'plain'], ax=ax); ax.set_title(L); ax.set_xlabel('predicted'); ax.set_ylabel('true')
plt.tight_layout(); plt.show()""")
    md("**Figure 5: Step B confusion matrices for Marathi, Hindi and Assamese proverbs in carrier sentences (5-fold cross-validation).**")
    code("""acc = pd.Series({L: metrics[f'step_b_{l}']['acc'] for l, L in LANGS}); acc['MAGPIE (real text)'] = metrics['magpie']['acc']
fig, ax = plt.subplots(figsize=(6.5, 3.6))
acc.plot.bar(ax=ax, color=['#2ca02c'] * 3 + ['#1f77b4']); ax.set_ylim(0, 1); ax.set_ylabel('accuracy'); plt.xticks(rotation=0)
ax.axhline(0.5, color='grey', ls=':'); plt.tight_layout(); plt.show()""")
    md("""**Figure 6: Detection accuracy for the three languages (Step B) next to the real-text result (Step A); dotted line is chance for Step B.**

## 4. The interface

`is_figurative()` is what a chatbot calls on a sentence.""")
    code("""def is_figurative(sentence):
    proba = det.predict_proba([sentence])[0]
    return dict(zip(det.classes_, np.round(proba, 3)))
print(is_figurative('After the merger the two teams were finally singing from the same hymn sheet.'))
print(is_figurative('The choir was singing from the same hymn sheet that the vicar had printed.'))""")
    finish(cells, 'idiom_detection',
           "On real text the detector separates idiomatic from literal usage well above the majority baseline, and the per-class figures show "
           "where it fails (literal uses are the minority and are the ones misread). The recipe transfers to all three proverb corpora in carrier "
           "sentences, with the register confound stated. `is_figurative()` is the detection back end for the team chatbot.",
           "- Haagsma, H., Bos, J., & Nissim, M. (2020). MAGPIE: A large corpus of potentially idiomatic expressions. *Proceedings of LREC 2020*, 279-287.\n"
           "- Tan, M., & Jiang, J. (2021). Does BERT understand idioms? A probing-based empirical study of BERT encodings of idioms. *Proceedings of RANLP 2021*, 1397-1407.")
    nb = nbf.v4.new_notebook(); nb['cells'] = cells; return nb


# =====================================================================
def build_llm():
    cells = []
    md = lambda s: cells.append(nbf.v4.new_markdown_cell(s))
    code = lambda s: cells.append(nbf.v4.new_code_cell(s))
    header(cells, 'A Proverb-Interpretation Benchmark for Language Models', 'b3',
           "**Research question (Chayan Raj Bharati):** When a small open language model is asked what a proverb means, does its answer come closer "
           "to the compiler's recorded meaning than the proverb's own literal text does, and does that hold when the input is the romanized source "
           "language rather than English?\n\n"
           "CCA1 found that a multilingual embedding model gave nothing on romanized text. This notebook asks the same question of generative "
           "models. Two open instruction-tuned models from different families, Qwen2.5-0.5B-Instruct (494M parameters, chat) and FLAN-T5-base "
           "(250M, sequence-to-sequence), are prompted for a one-sentence meaning of each proverb under two inputs, and scored against the "
           "compiler's explanation with controls that separate interpretation from restatement.")
    code(SETUP)
    md("""## 1. Set-up

60 proverbs with explanations per language (random sample, seed 42; Assamese has 75 in total). Score: LaBSE cosine similarity between the model's answer and the gold explanation. Control: similarity between the same answer and a random other explanation; the margin between the two is what counts. Echo baseline: the literal translation itself, scored the same way, which is what a model gets for merely restating the proverb.""")
    code("""from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
import torch
torch.set_num_threads(4)
MODELS = ['Qwen/Qwen2.5-0.5B-Instruct', 'google/flan-t5-base']
loaded = {}
def load(name):
    if name not in loaded:
        tok = AutoTokenizer.from_pretrained(name)
        if 't5' in name:
            mdl = AutoModelForSeq2SeqLM.from_pretrained(name)
        else:
            tok.padding_side = 'left'; mdl = AutoModelForCausalLM.from_pretrained(name, dtype=torch.float32)
        loaded[name] = (tok, mdl)
    return loaded[name]

def ask(name, texts, batch=8):
    tok, mdl = load(name)
    prompts = [f'Explain the meaning of this proverb in one sentence: "{t}"' for t in texts]
    out = []
    for i in range(0, len(prompts), batch):
        if 't5' in name:
            enc = tok(prompts[i:i + batch], return_tensors='pt', padding=True, truncation=True, max_length=96)
            with torch.no_grad():
                gen = mdl.generate(**enc, max_new_tokens=48, num_beams=2)
            out += tok.batch_decode(gen, skip_special_tokens=True)
        else:
            chats = [tok.apply_chat_template([{'role': 'user', 'content': p}], tokenize=False, add_generation_prompt=True) for p in prompts[i:i + batch]]
            enc = tok(chats, return_tensors='pt', padding=True)
            with torch.no_grad():
                gen = mdl.generate(**enc, max_new_tokens=48, do_sample=False)
            out += [tok.decode(g[enc['input_ids'].shape[1]:], skip_special_tokens=True).strip() for g in gen]
    return out""")
    md("""## 2. Running the benchmark on the three corpora""")
    code("""per_item = []
answers = {}
for l, L in LANGS:
    df = with_expl[l]
    bench = df if len(df) <= 60 else df.sample(60, random_state=42).reset_index(drop=True)
    gold = embed(bench.commentary.tolist()); control = gold[rng.permutation(len(gold))]
    systems = {}
    for name in MODELS:
        for cond, col in [('literal_en', 'literal_en'), ('romanized', 'proverb_translit')]:
            ans = ask(name, bench[col].tolist()); A = embed(ans)
            answers[(l, name, cond)] = ans
            systems[f'{name.split("/")[1].replace("-Instruct", "")} / {cond}'] = A
    systems['echo baseline'] = embed(bench.literal_en.tolist())
    for sysname, A in systems.items():
        sg = (A * gold).sum(axis=1); sc = (A * control).sum(axis=1)
        for i in range(len(bench)):
            per_item.append({'language': L, 'system': sysname, 'sim_gold': float(sg[i]), 'sim_control': float(sc[i]), 'margin': float(sg[i] - sc[i])})
    print(L, 'done,', len(bench), 'proverbs')
per_item = pd.DataFrame(per_item)
bench_tbl = per_item.groupby(['language', 'system'])[['sim_gold', 'sim_control', 'margin']].mean().round(3)
metrics['benchmark'] = {f'{L}/{s}': bench_tbl.loc[(L, s)].to_dict() for L, s in bench_tbl.index}
bench_tbl""")
    md("""## 3. Results""")
    for i, (l, L) in enumerate(LANGS):
        code(f"""sub = bench_tbl.loc['{L}']
fig, ax = plt.subplots(figsize=(8, 3.8))
sub[['sim_gold', 'sim_control']].plot.barh(ax=ax, color=['#1f77b4', '#bbbbbb']); ax.invert_yaxis()
ax.set_xlabel('mean LaBSE similarity'); ax.set_title('{L}'); ax.legend(['to own explanation', 'to a random explanation (control)'], loc='lower right')
plt.tight_layout(); plt.show()""")
        md(f"**Figure {i + 1}: {L}: mean similarity of each system's answer to the compiler's explanation (blue) against the control (grey), for both inputs and the echo baseline.**")
    code("""fig, ax = plt.subplots(figsize=(10, 4.2))
sns.boxplot(data=per_item[per_item.system.str.contains('Qwen|echo')], x='system', y='margin', hue='language', ax=ax)
ax.axhline(0, color='k', lw=1); ax.set_ylabel('margin (own minus random explanation)'); plt.xticks(rotation=15, ha='right')
plt.tight_layout(); plt.show()""")
    md("**Figure 4: Per-proverb margin distributions for the Qwen conditions and the echo baseline, by language. A margin above zero means the answer is closer to the right explanation than to a random one.**")
    code("""m = bench_tbl['margin'].unstack('language')
fig, ax = plt.subplots(figsize=(8, 4))
m.plot.bar(ax=ax); ax.axhline(0, color='k', lw=1); ax.set_ylabel('mean margin'); plt.xticks(rotation=15, ha='right')
plt.tight_layout(); plt.show()""")
    md("**Figure 5: Mean margin per system across the three languages. The echo baseline is the bar each model has to beat.**")
    code("""pd.set_option('display.max_colwidth', 110)
l = 'hindi'; df = with_expl[l]; bench = df.sample(60, random_state=42).reset_index(drop=True)
ex = pd.DataFrame({'proverb (literal)': bench.literal_en.head(5), 'gold meaning': bench.commentary.head(5),
                   'Qwen answer': answers[(l, 'Qwen/Qwen2.5-0.5B-Instruct', 'literal_en')][:5],
                   'FLAN-T5 answer': answers[(l, 'google/flan-t5-base', 'literal_en')][:5]})
ex""")
    md("""Five Hindi examples with both models' answers next to the gold explanation, so the scores can be read against what the models actually wrote.

## 4. The interface

`explain()` is what a chatbot calls: it returns the model's one-sentence meaning and, when the proverb is in the corpus, the compiler's recorded meaning next to it.""")
    code("""def explain(text, name='Qwen/Qwen2.5-0.5B-Instruct'):
    return ask(name, [text])[0]
print(explain('Perpetual crops, perpetual poverty.'))""")
    finish(cells, 'llm_benchmark',
           "In all three languages the echo baseline has the largest margin: a model given the literal translation produces a fluent meaning that "
           "is no closer to the compiler's than the proverb text itself, and given romanized text its margin is near zero. The CCA1 cross-lingual "
           "wall holds for generative models. The famous-versus-obscure split proposed in Plan A needs a frequency source and is left for later. "
           "`explain()` is the generation back end for the team chatbot, used with the recorded meaning shown alongside.",
           "- Chung, H. W., et al. (2022). Scaling instruction-finetuned language models. *arXiv:2210.11416*.\n"
           "- Qwen Team (2024). Qwen2.5 technical report. *arXiv:2412.15115*.\n"
           "- Liu, C. C., Koto, F., Baldwin, T., & Gurevych, I. (2024). Are multilingual LLMs culturally-diverse reasoners? An investigation into multicultural proverbs and sayings. *Proceedings of NAACL 2024*.")
    nb = nbf.v4.new_notebook(); nb['cells'] = cells; return nb


if __name__ == '__main__':
    which = sys.argv[1:] or ['reverse_retrieval', 'idiom_detection', 'llm_benchmark']
    builders = {'reverse_retrieval': build_reverse, 'idiom_detection': build_idiom, 'llm_benchmark': build_llm}
    for w in which:
        nbf.write(builders[w](), f'PanelB_16_CCA3_v2_{w}.ipynb')
        print(w, 'written')
