"""Extra figures and case tables for the CCA3 v2 report: methodology diagram,
data screenshots, training-data screenshot, idiom/proverb records, and
success/failure cases computed with the same models the notebooks use."""
import json, re, os, textwrap
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = 'report/figures/extras'; os.makedirs(OUT, exist_ok=True)
LANGS = [('marathi', 'Marathi'), ('hindi', 'Hindi'), ('assamese', 'Assamese')]
CORPUS = '../cca1/corpus/PanelB_16_{}_proverbs.csv'
corpora = {l: pd.read_csv(CORPUS.format(l)) for l, _ in LANGS}
with_expl = {l: df[df.commentary.fillna('').str.len() > 20].reset_index(drop=True) for l, df in corpora.items()}

def cut(s, n):
    s = re.sub(r'\s+', ' ', str(s)).strip()
    return s if len(s) <= n else s[:n - 1] + '…'

def table_image(df, path, col_widths, title=None, fontsize=7.5, wrap=None):
    """Render a dataframe as a screenshot-like table."""
    cells = []
    for _, r in df.iterrows():
        row = []
        for c in df.columns:
            v = str(r[c])
            if wrap and c in wrap:
                v = '\n'.join(textwrap.wrap(v, wrap[c])) or v
            row.append(v)
        cells.append(row)
    nlines = sum(max(v.count('\n') + 1 for v in row) for row in cells) + 1
    fig, ax = plt.subplots(figsize=(11, 0.28 * nlines + 0.8))
    ax.axis('off')
    t = ax.table(cellText=cells, colLabels=list(df.columns), loc='upper left', cellLoc='left', colWidths=col_widths)
    t.auto_set_font_size(False); t.set_fontsize(fontsize)
    base = None
    for (i, j), cell in t.get_celld().items():
        cell.set_linewidth(0.4)
        cell.get_text().set_verticalalignment('center')
        if base is None: base = cell.get_height()
        if i == 0:
            cell.set_facecolor('#dfe7f3'); cell.get_text().set_weight('bold')
        else:
            rowlines = max(v.count('\n') + 1 for v in cells[i - 1])
            cell.set_height(base * (rowlines * 0.9 + 0.3))
    if title:
        ax.set_title(title, fontsize=9, loc='left')
    plt.savefig(path, dpi=170, bbox_inches='tight', facecolor='white'); plt.close()

# ---------- 1. methodology diagram ----------
fig, ax = plt.subplots(figsize=(10, 6.2)); ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off')
def box(x, y, w, h, text, fc='#eef3fb', ec='#2b4c7e', fs=8.6, bold=False):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle='round,pad=0.06', fc=fc, ec=ec, lw=1.3))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, fontweight='bold' if bold else 'normal')
def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>', mutation_scale=12, lw=1.2, color='#2b4c7e'))
box(5, 9.2, 8.6, 1.0, 'CCA1 proverb corpora (reused unchanged)\nMarathi 545 | Hindi 344 | Assamese 103 proverbs — each: romanized text, literal English translation, recorded meaning', fc='#fdf3e0', ec='#a66a12', bold=True)
box(8.6, 7.5, 2.4, 0.9, 'MAGPIE corpus\n48,395 English sentences\nidiomatic / literal labels', fc='#fdf3e0', ec='#a66a12')
for x in (1.7, 5, 8.3):
    arrow(5 if x == 5 else x, 8.7, x, 6.75)
arrow(8.6, 7.05, 8.3, 6.75)
box(1.7, 6.0, 3.0, 1.5, 'Reverse retrieval (Sahish)\nindex = explanations\nTF-IDF and LaBSE\nquery = situation description\nHit@k, MRR vs random', fc='#e8f5e9', ec='#2e7d32')
box(5, 6.0, 3.0, 1.5, 'LLM benchmark (Chayan)\nQwen2.5-0.5B, FLAN-T5-base\ninputs: literal / romanized\nLaBSE similarity to meaning\ncontrol + echo baseline', fc='#e8f5e9', ec='#2e7d32')
box(8.3, 6.0, 3.0, 1.5, 'Idiom detection (Ibrahim)\nStep A: train/test on MAGPIE\nTF-IDF 1-2-grams + LogReg\nStep B: proverbs in carriers\nvs real literal sentences', fc='#e8f5e9', ec='#2e7d32')
for x in (1.7, 5, 8.3):
    arrow(x, 5.25, x, 4.35)
box(1.7, 3.8, 3.0, 0.9, 'suggest(situation)\n-> ranked proverbs + meanings')
box(5, 3.8, 3.0, 0.9, 'explain(proverb)\n-> model answer next to recorded meaning')
box(8.3, 3.8, 3.0, 0.9, 'is_figurative(sentence)\nscan(paragraph)')
for x in (1.7, 5, 8.3):
    arrow(x, 3.35, 5, 2.45)
box(5, 1.9, 7.4, 0.95, 'Terminal chatbot (team): rule-based routing, /lang filter, /llm switch; every reply names the experiment that answered', fc='#fbeeee', ec='#9c2f2f', bold=True)
box(5, 0.55, 8.6, 0.75, 'Evaluation: per-experiment metrics with baselines, saved to metrics JSON; all report numbers are generated from those files', fc='#f4f4f4', ec='#555555')
plt.savefig(f'{OUT}/methodology.png', dpi=170, bbox_inches='tight', facecolor='white'); plt.close()

# ---------- 2. corpus / data screenshots ----------
CLEAN_IDS = {'marathi': [13, 23, 68, 216], 'hindi': [1, 47, 48, 79], 'assamese': [17, 46, 48, 42]}
for l, L in LANGS:
    df = with_expl[l].set_index('id').loc[[i for i in CLEAN_IDS[l] if i in set(with_expl[l].id)]].reset_index()[['id', 'proverb_translit', 'literal_en', 'commentary']].copy()
    df['proverb_translit'] = df.proverb_translit.map(lambda s: cut(s, 60)); df['literal_en'] = df.literal_en.map(lambda s: cut(s, 110)); df['commentary'] = df.commentary.map(lambda s: cut(s, 150))
    table_image(df, f'{OUT}/data_{l}.png', [0.05, 0.22, 0.33, 0.40], title=f'{L} corpus: PanelB_16_{l}_proverbs.csv (sample rows)',
                wrap={'proverb_translit': 30, 'literal_en': 48, 'commentary': 60})
mag = [json.loads(x) for x in open('external/MAGPIE_filtered_split_random.jsonl', encoding='utf8')]
magdf = pd.DataFrame([{'sentence': m['context'][2], 'idiom': m['idiom'], 'label': {'i': 'idiomatic', 'l': 'literal'}.get(m['label'], m['label']), 'split': m['split']} for m in mag if m['label'] in ('i', 'l')])
sample = pd.concat([magdf[magdf.label == 'idiomatic'].head(3), magdf[magdf.label == 'literal'].head(3)])
sample['sentence'] = sample.sentence.map(lambda s: cut(s, 140))
table_image(sample, f'{OUT}/data_magpie.png', [0.6, 0.2, 0.1, 0.1], title='MAGPIE corpus: external/MAGPIE_filtered_split_random.jsonl (idiomatic and literal rows)', wrap={'sentence': 80, 'idiom': 22})

# ---------- 3. training-data screenshot (what the detector was trained on) ----------
train = magdf[magdf.split == 'training']
tr = pd.concat([train[train.label == 'idiomatic'].sample(3, random_state=7), train[train.label == 'literal'].sample(3, random_state=7)])[['sentence', 'idiom', 'label']]
tr['sentence'] = tr.sentence.map(lambda s: cut(s, 140))
templates = ['My grandmother used to say that {}', 'As the saying goes, {}', 'He looked at me and said: {}', 'In the end, {}', 'She reminded everyone that {}', 'It is well known that {}']
rng = np.random.default_rng(3)
def clean(s):
    s = re.sub(r'\s+', ' ', str(s)).strip().rstrip('.'); return s[0].lower() + s[1:] if s else s
lit = magdf[(magdf.label == 'literal')].sentence; lit = lit[lit.str.split().str.len().between(5, 25)]
stepb = []
for l, L in LANGS:
    pv = corpora[l].literal_en.iloc[rng.integers(0, len(corpora[l]))]
    stepb.append({'sentence': cut(rng.choice(templates).format(clean(pv)), 140), 'class': 'proverb', 'source': f'{L} corpus'})
    stepb.append({'sentence': cut(rng.choice(templates).format(clean(rng.choice(lit.values))), 140), 'class': 'plain', 'source': 'MAGPIE literal'})
table_image(tr, f'{OUT}/train_magpie.png', [0.64, 0.22, 0.14], title='Step A training data: MAGPIE training split (38,716 sentences), six sampled rows', wrap={'sentence': 88})
table_image(pd.DataFrame(stepb), f'{OUT}/train_stepb.png', [0.66, 0.12, 0.22], title='Step B data: proverbs and real literal sentences in the same carrier templates, six sampled rows', wrap={'sentence': 90})

# ---------- 4. record of idioms and proverbs ----------
rec = []
for l, L in LANGS:
    r = with_expl[l].set_index('id').loc[CLEAN_IDS[l][:2]].reset_index()
    for _, x in r.iterrows():
        rec.append({'type': f'{L} proverb', 'expression': cut(x.proverb_translit, 50), 'literal / sentence': cut(x.literal_en, 90), 'intended meaning / label': cut(x.commentary, 100)})
for _, x in pd.concat([magdf[magdf.label == 'idiomatic'].head(2), magdf[magdf.label == 'literal'].head(1)]).iterrows():
    rec.append({'type': 'English idiom (MAGPIE)', 'expression': x.idiom, 'literal / sentence': cut(x.sentence, 90), 'intended meaning / label': f'{x.label} usage'})
table_image(pd.DataFrame(rec), f'{OUT}/records.png', [0.17, 0.2, 0.32, 0.31], title='Records: six proverbs (two per corpus) and three MAGPIE idiom occurrences', wrap={'type': 20, 'expression': 24, 'literal / sentence': 42, 'intended meaning / label': 42})

# ---------- 5./6. success and failure cases (live models) ----------
if os.path.exists('report/PanelB_16_CCA3_v2_cases.json'):
    print('cases file exists, skipping model runs'); raise SystemExit(0)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import make_pipeline
from sentence_transformers import SentenceTransformer
labse = SentenceTransformer('sentence-transformers/LaBSE')
embed = lambda t: labse.encode(list(t), show_progress_bar=False, normalize_embeddings=True)
cases = {'reverse': [], 'idiom': [], 'llm': []}

# reverse retrieval: rerun the notebook's queries, collect rank-1 hits and misses
import importlib.util
spec = importlib.util.spec_from_file_location('v2', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'make_cca3_v2.py')); v2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v2)
for l, L in LANGS:
    df = with_expl[l]; D = embed(df.commentary)
    for q, tid in v2.SITUATIONS[l]:
        if tid not in set(df.id): continue
        sims = cosine_similarity(embed([q]), D)[0]; order = np.argsort(-sims); ids = df.id.values[order]
        rank = int(np.where(ids == tid)[0][0]) + 1
        top = df.iloc[order[0]]; tgt = df[df.id == tid].iloc[0]
        cases['reverse'].append({'language': L, 'query': q, 'rank': rank, 'target': cut(tgt.literal_en, 70), 'returned': cut(top.literal_en, 70), 'returned_meaning': cut(top.commentary, 80)})
rev = pd.DataFrame(cases['reverse'])

# idiom detection: the published two-class detector, correct and wrong test predictions
det = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, min_df=2), LogisticRegression(max_iter=3000, class_weight='balanced'))
det.fit(train.sentence, train.label)
test = magdf[magdf.split == 'test'].copy()
test['pred'] = det.predict(test.sentence); test['p_idiom'] = det.predict_proba(test.sentence)[:, list(det.classes_).index('idiomatic')]
test['len'] = test.sentence.str.split().str.len()
short = test[test.len.between(8, 18)]
ok = short[short.pred == short.label]; bad = short[short.pred != short.label]
pick = pd.concat([ok[ok.label == 'idiomatic'].sample(1, random_state=1), ok[ok.label == 'literal'].sample(1, random_state=1),
                  bad[bad.label == 'literal'].sample(1, random_state=1), bad[bad.label == 'idiomatic'].sample(1, random_state=1)])
for _, x in pick.iterrows():
    cases['idiom'].append({'sentence': x.sentence, 'idiom': x.idiom, 'true': x.label, 'predicted': x.pred, 'p_idiomatic': round(float(x.p_idiom), 2), 'outcome': 'success' if x.pred == x.label else 'failure'})

# LLM: Qwen on 12 Hindi + 12 Marathi proverbs, best and worst margins
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
torch.set_num_threads(4)
tok = AutoTokenizer.from_pretrained('Qwen/Qwen2.5-0.5B-Instruct'); tok.padding_side = 'left'
mdl = AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-0.5B-Instruct', dtype=torch.float32)
rows = []
for l, L in [('hindi', 'Hindi'), ('marathi', 'Marathi'), ('assamese', 'Assamese')]:
    b = with_expl[l].sample(8, random_state=11)
    prompts = [f'Explain the meaning of this proverb in one sentence: "{t}"' for t in b.literal_en]
    chats = [tok.apply_chat_template([{'role': 'user', 'content': p}], tokenize=False, add_generation_prompt=True) for p in prompts]
    enc = tok(chats, return_tensors='pt', padding=True)
    with torch.no_grad():
        gen = mdl.generate(**enc, max_new_tokens=48, do_sample=False)
    ans = [tok.decode(g[enc['input_ids'].shape[1]:], skip_special_tokens=True).strip() for g in gen]
    A = embed(ans); G = embed(b.commentary); C = G[np.random.default_rng(1).permutation(len(G))]
    for i, (_, x) in enumerate(b.iterrows()):
        rows.append({'language': L, 'proverb': cut(x.literal_en, 70), 'gold': cut(x.commentary, 90), 'answer': cut(ans[i], 110), 'margin': round(float((A[i] * G[i]).sum() - (A[i] * C[i]).sum()), 2)})
llm = pd.DataFrame(rows).sort_values('margin', ascending=False)
cases['llm'] = pd.concat([llm.head(2).assign(outcome='success'), llm.tail(2).assign(outcome='failure')]).to_dict('records')
cases['reverse'] = rev.to_dict('records')
json.dump(cases, open('report/PanelB_16_CCA3_v2_cases.json', 'w'), indent=1)
print('extras done:', len(rev), 'reverse queries,', len(cases['idiom']), 'idiom cases,', len(cases['llm']), 'llm cases')
