"""Export the sample rows shown as tables in the reports (corpus rows, MAGPIE
rows, record table, training-data rows) and the situation-queries CSV.
Run from the cca3 folder. Output: report/PanelB_16_CCA3_v2_sample_rows.json and
report/PanelB_16_CCA3_v2_situation_queries.csv."""
import json, re, os, importlib.util
import numpy as np, pandas as pd

LANGS = [('marathi', 'Marathi'), ('hindi', 'Hindi'), ('assamese', 'Assamese')]
CLEAN = {'marathi': [13, 23, 68, 216], 'hindi': [1, 47, 48, 79], 'assamese': [17, 46, 48, 42]}  # hand-picked clean rows
corp = {l: pd.read_csv(f'../cca1/corpus/PanelB_16_{l}_proverbs.csv') for l, _ in LANGS}
we = {l: df[df.commentary.fillna('').str.len() > 20].reset_index(drop=True) for l, df in corp.items()}

def cut(s, n):
    s = re.sub(r'\s+', ' ', str(s)).strip(); return s if len(s) <= n else s[:n - 1] + '…'

out = {'corpus': {}, 'records': [], 'magpie': [], 'train_a': [], 'train_b': [], 'queries': []}
for l, L in LANGS:
    d = we[l].set_index('id').loc[[i for i in CLEAN[l] if i in set(we[l].id)]].reset_index()
    out['corpus'][L] = [[int(r.id), cut(r.proverb_translit, 60), cut(r.literal_en, 110), cut(r.commentary, 150)] for r in d.itertuples()]
    for r in d.head(2).itertuples():
        out['records'].append([f'{L} proverb', cut(r.proverb_translit, 50), cut(r.literal_en, 90), cut(r.commentary, 100)])
mag = [json.loads(x) for x in open('external/MAGPIE_filtered_split_random.jsonl', encoding='utf8')]
mdf = pd.DataFrame([{'sentence': m['context'][2], 'idiom': m['idiom'], 'label': {'i': 'idiomatic', 'l': 'literal'}.get(m['label'], m['label']), 'split': m['split']}
                    for m in mag if m['label'] in ('i', 'l')])
sample = pd.concat([mdf[mdf.label == 'idiomatic'].head(3), mdf[mdf.label == 'literal'].head(3)])
out['magpie'] = [[cut(r.sentence, 140), r.idiom, r.label, r.split] for r in sample.itertuples()]
for r in pd.concat([mdf[mdf.label == 'idiomatic'].head(2), mdf[mdf.label == 'literal'].head(1)]).itertuples():
    out['records'].append(['English idiom (MAGPIE)', r.idiom, cut(r.sentence, 90), f'{r.label} usage'])
train = mdf[mdf.split == 'training']
tr = pd.concat([train[train.label == 'idiomatic'].sample(3, random_state=7), train[train.label == 'literal'].sample(3, random_state=7)])
out['train_a'] = [[cut(r.sentence, 140), r.idiom, r.label] for r in tr.itertuples()]
templates = ['My grandmother used to say that {}', 'As the saying goes, {}', 'He looked at me and said: {}', 'In the end, {}', 'She reminded everyone that {}', 'It is well known that {}']
rng = np.random.default_rng(3)
def clean(s):
    s = re.sub(r'\s+', ' ', str(s)).strip().rstrip('.'); return s[0].lower() + s[1:] if s else s
lit = mdf[mdf.label == 'literal'].sentence; lit = lit[lit.str.split().str.len().between(5, 25)]
for l, L in LANGS:
    pv = corp[l].literal_en.iloc[rng.integers(0, len(corp[l]))]
    out['train_b'].append([cut(rng.choice(templates).format(clean(pv)), 140), 'proverb', f'{L} corpus'])
    out['train_b'].append([cut(rng.choice(templates).format(clean(rng.choice(lit.values))), 140), 'plain', 'MAGPIE literal'])
spec = importlib.util.spec_from_file_location('v2', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'make_cca3_v2.py'))
v2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v2)
rows = []
for l, L in LANGS:
    for q, tid in v2.SITUATIONS[l]:
        if tid in set(we[l].id):
            t = we[l][we[l].id == tid].iloc[0]
            rows.append({'language': L, 'situation': q, 'target_id': tid, 'target_proverb': t.proverb_translit, 'target_literal': t.literal_en})
pd.DataFrame(rows).to_csv('report/PanelB_16_CCA3_v2_situation_queries.csv', index=False)
out['queries'] = rows
json.dump(out, open('report/PanelB_16_CCA3_v2_sample_rows.json', 'w'), indent=1)
print('written sample rows json and situation queries csv:', len(rows), 'queries')
