import json, os, base64
import pandas as pd
import nbformat
from docx import Document

def _merge_repeats(t, rows, col=0):
    """Vertically merge consecutive equal cells in a column (used for the Language column)."""
    if not rows or str(rows[0][col]) != 'Language':
        return
    i = 1
    while i < len(rows):
        j = i
        while j + 1 < len(rows) and rows[j + 1][col] == rows[i][col]:
            j += 1
        if j > i:
            merged = t.cell(i, col).merge(t.cell(j, col))
            merged.text = str(rows[i][col])
            from docx.enum.table import WD_ALIGN_VERTICAL
            merged.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        i = j + 1
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

# ---------- export figures from the executed v2 notebooks ----------
for w in ['reverse_retrieval', 'idiom_detection', 'llm_benchmark']:
    nb = nbformat.read(f'PanelB_16_CCA3_v2_{w}.ipynb', as_version=4)
    d = f'report/figures/v2_{w}'; os.makedirs(d, exist_ok=True)
    i = 0
    for c in nb.cells:
        if c.cell_type != 'code': continue
        for o in c.get('outputs', []):
            if o.output_type == 'display_data' and 'image/png' in o.get('data', {}):
                i += 1
                open(f'{d}/fig{i}.png', 'wb').write(base64.b64decode(o['data']['image/png']))

R = json.load(open('report/PanelB_16_CCA3_v2_reverse_retrieval_metrics.json'))
I = json.load(open('report/PanelB_16_CCA3_v2_idiom_detection_metrics.json'))
Q = json.load(open('report/PanelB_16_CCA3_v2_llm_benchmark_metrics.json'))
CASES = json.load(open('report/PanelB_16_CCA3_v2_cases.json'))
SR = json.load(open('report/PanelB_16_CCA3_v2_sample_rows.json'))
LANGS = ['Marathi', 'Hindi', 'Assamese']
rs = R['summary']; qb = Q['benchmark']
def qget(L, s, k): return qb[f'{L}/{s}'][k]

doc = Document()
st = doc.styles['Normal']; st.font.name = 'Times New Roman'; st.font.size = Pt(10)
fignum = 0

def h1(t): doc.add_heading(t, level=1)
def h2(t): doc.add_heading(t, level=2)
def h3(t): doc.add_heading(t, level=3)
def p(t, italic=False, center=False, bold=False):
    par = doc.add_paragraph()
    if center: par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = par.add_run(t); r.italic = italic; r.bold = bold
def caption(t):
    par = doc.add_paragraph(); par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = par.add_run(t); r.italic = True; r.font.size = Pt(9.5)
FN = {}
def fig(path, name, inf=None, width=3.2, key=None):
    global fignum; fignum += 1
    if key: FN[key] = fignum
    par = doc.add_paragraph(); par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.add_run().add_picture(path, width=Inches(width))
    caption(f'Figure {fignum}: {name}')
    if inf:
        ip = doc.add_paragraph(); r = ip.add_run('Inference: '); r.bold = True; ip.add_run(inf)
    return fignum
TN = {}
tabnum = 0
def table(rows, cap=None, inf=None, key=None, size=None):
    global tabnum
    if cap:
        tabnum += 1
        if key: TN[key] = tabnum
        caption(f'Table {tabnum}: {cap}')
    t = doc.add_table(rows=len(rows), cols=len(rows[0])); t.style = 'Table Grid'
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            c = t.rows[i].cells[j]; c.text = str(cell)
            r = c.paragraphs[0].runs[0]
            if i == 0: r.bold = True
            if size: r.font.size = Pt(size)
    _merge_repeats(t, rows)
    if inf:
        ip = doc.add_paragraph(); r = ip.add_run('Inference: '); r.bold = True; ip.add_run(inf)
    else:
        doc.add_paragraph()

# ---------- Team information / problem statement ----------
p('School of Computer Science & Engineering, MIT-WPU', center=True)
p('CCA3 — Cloud Computing & Natural Language Processing — Panel B, Team 16', center=True, bold=True)
doc.add_heading('Mini Project: Literal and Intended Meaning of Indian Proverbs — Reverse Retrieval, Idiom Detection in Text, and a Language-Model Interpretation Benchmark on Marathi, Hindi and Assamese Corpora', level=0)
h1('Team information')
table([('Member', 'PRN'), ('Sahish Nagulwar', '1032233310'), ('Ibrahim Ansari', '1032233145'), ('Chayan Raj Bharati', '1032233134')])
p('The work is organised in three parts, each run on all three corpora: Part I, reverse retrieval of a proverb from a situation; Part II, idiom identification in running text; Part III, a language-model interpretation benchmark.')
h1('Problem statement')
p('Develop a multilingual NLP framework that identifies Indian idioms and distinguishes their literal meaning from culturally '
  'intended figurative meaning across Indian languages, while modeling cultural context and linguistic variation. CCA3 '
  'extends the CCA1 work on the Marathi, Hindi and Assamese proverb corpora with three follow-up experiments (Parts I to III), '
  'each run on all three corpora.', italic=True)

# ---------- 1 Abstract ----------
h1('1. Abstract')
p('CCA1 built three annotated proverb corpora (545 Marathi, 344 Hindi, 103 Assamese) from public-domain books and showed that '
  'the intended meaning of a proverb cannot be read off its words: retrieval of that meaning collapses when the query crosses '
  'from English into the source language, and a multilingual embedding model gave nothing on romanized text. CCA3 takes three '
  'of the extensions planned afterwards and runs each on all three corpora. Reverse retrieval suggests a proverb for a plain '
  'description of a situation, using TF-IDF and LaBSE indexes over the explanations. An idiom detector is trained and validated '
  'on MAGPIE, 48,395 real English sentences labelled for figurative or literal usage, and the recipe is applied to the three '
  'proverb corpora. A benchmark asks two open language models, Qwen2.5-0.5B-Instruct and FLAN-T5-base, for the meaning of each '
  'proverb and scores the answer against the compiler\'s explanation with a random-explanation control and an echo baseline. '
  f'Reverse retrieval reaches Hit@5 of {rs["Marathi/labse"]["hit_at_5"]}, {rs["Hindi/labse"]["hit_at_5"]} and {rs["Assamese/labse"]["hit_at_5"]} '
  f'(Marathi, Hindi, Assamese; LaBSE) against random baselines of 0.02 to 0.07. The detector scores {I["magpie"]["acc"]} accuracy on real '
  f'sentences against a {I["magpie"]["majority_acc"]} majority baseline and 0.91 to 0.94 on the proverb corpora. In every language the '
  'models\' margin over the control is smaller than the margin from simply repeating the proverb, and near zero on romanized input. '
  'The three experiments are joined in a terminal chatbot that answers a situation with proverbs, judges whether a sentence uses an idiom figuratively, and shows a model\'s interpretation next to the recorded meaning.')

# ---------- 2 Introduction ----------
h1('2. Introduction')
p('A proverb says one thing and means another. "Perpetual crops, perpetual poverty" is not about farming; it describes a '
  'farmer who stays poor because he keeps borrowing. Systems that read text compositionally get the words right and the '
  'meaning wrong, and the problem is sharper in Indian languages, where the stock of proverbs is large, regionally varied and '
  'thinly digitised. CCA1 addressed this by building corpora from colonial-era compilations that record the intended meaning '
  'next to the literal text (Manwaring, 1899; Fallon, 1886; Gurdon, 1896), and by measuring how far that meaning can be '
  'recovered. Three findings set up the present work: a proverb shares no more vocabulary with its own explanation than with '
  'a random one; retrieval of the intended meaning works within English but drops sharply with the romanized source text as '
  'the query (P@1 0.347 to 0.120 for Assamese, 0.129 to 0.029 for Marathi, 0.081 to 0.024 for Hindi); and LaBSE, run zero-shot '
  'on that romanized text, stayed at the random baseline.')
p('The mini project picks up the plan we wrote after CCA1 and builds three of the extensions in it. All three run on all '
  'three corpora through the same code, so a difference between languages is a difference in the data and not in the pipeline. '
  'Why these three? Put together they are what someone would actually want from a proverb tool. Give it a situation and get a '
  'proverb back. Paste a sentence and learn whether the proverb in it is meant figuratively. Ask what a proverb means and get an '
  'answer, which here we test on small language models. Each notebook ends in one function (suggest, is_figurative, explain), '
  'and the chatbot calls those three functions. We had also started a fourth extension, linking equivalent proverbs across the '
  'three languages, in the first round of notebooks. It found too few pairs to evaluate, so it is not in this report.')

# ---------- 2.1 RQs ----------
h2('2.1 Research questions')
p('RQ1 (Part I): Given a plain description of a situation, can the right proverb be retrieved from the explanation '
  'index of each corpus, and does a semantic index (LaBSE) do better than a lexical one (TF-IDF)?')
p('RQ2 (Part II): Can a detector that separates figurative from literal usage, trained on real English sentences, be '
  'built with the CCA1 recipe, and does it transfer to Marathi, Hindi and Assamese proverbs placed in running text?')
p('RQ3 (Part III): When a small open language model is asked what a proverb means, does its answer come closer to '
  'the compiler\'s recorded meaning than the proverb\'s own literal text does, and does that hold when the input is the '
  'romanized source language rather than English?')

# ---------- 2.2 Contributions ----------
h2('2.2 Research contributions')
p(f'Part I: a situation-to-proverb retrieval index for each of the three corpora, a test set of {sum(R["n_queries"].values())} '
  'hand-written situation queries (written by team members who did not build the index they test), an evaluation of lexical '
  'against semantic indexing on it, and the suggest() interface that returns proverbs with their literal translation and '
  'recorded meaning.')
p(f'Part II: an idiom-usage detector trained on {I["magpie"]["train"]:,} real English sentences and tested on {I["magpie"]["test"]:,}, '
  'with per-class precision and recall and an analysis of the features it relies on; the transfer of the same recipe to '
  'the three proverb corpora in carrier sentences with real literal sentences as negatives; and the is_figurative() interface.')
p('Part III: a proverb-interpretation benchmark of 60 proverbs per language on which two open language models are '
  'scored under two input conditions, with a random-explanation control and an echo baseline that separate interpretation '
  'from restatement; per-proverb margin distributions; and the explain() interface, which shows the model\'s answer next to '
  'the recorded meaning.')

p('Chatbot (team): a terminal chatbot (PanelB_16_CCA3_chatbot.py) that routes each message to one of the three experiments and reports which one answered, with a language filter and a switch for the language model.')

# ---------- 2.3 Methodology ----------
h2('2.3 Methodology')
p('Part I: for each corpus, the explanations of all proverbs with a recorded meaning (338 Marathi, 305 Hindi, 75 '
  'Assamese) are indexed twice, with TF-IDF (word level, English stop words removed) and with LaBSE sentence embeddings '
  '(normalized, cosine similarity). A query is a one-sentence situation description; the proverbs are ranked by the '
  'similarity of their explanation to it. Each query targets one proverb, and Hit@1, Hit@5 and mean reciprocal rank are '
  'computed against a random-ranking baseline. The descriptions avoid copying words from the explanation.')
p('Part II: Step A trains TF-IDF over word unigrams and bigrams with logistic regression (balanced class weights) on '
  'the MAGPIE training split and tests on its test split, labels idiomatic versus literal usage. Step B applies the same '
  'recipe to each language: the proverbs (literal translations) are placed in six carrier sentences as positives, and real '
  'literal MAGPIE sentences are placed in the same carriers as negatives, under 5-fold cross-validation; the carriers cancel, '
  'so the classifier must decide from content. Step B carries a stated confound, since 1890s book English and modern BNC '
  'English differ in register, and Step A is treated as the honest number.')
p('Part III: 60 proverbs with explanations per language (random sample, seed 42). Qwen2.5-0.5B-Instruct and '
  'FLAN-T5-base are prompted for a one-sentence meaning, once with the literal translation and once with the romanized source '
  'text. The answer is scored by LaBSE similarity to the gold explanation; the control is its similarity to a random other '
  'explanation; the margin is the difference. The echo baseline scores the literal translation itself the same way. Both '
  'models run on CPU with greedy or two-beam decoding.')

fig('report/figures/extras/methodology.png', 'Methodology of CCA3: the three corpora and MAGPIE feed three experiments (Parts I to III), whose functions are joined in the team chatbot; all numbers come from the saved metrics files.',
    'The three experiments share their inputs and their evaluation style but not their models, so a difference between them is a difference in task, not in data preparation.', width=5.0, key='method')

# ---------- 2.4 Corpora ----------
h2('2.4 Description of corpora')
p('Part I: the three CCA1 corpora, reused unchanged. Each row has the romanized proverb, its literal English '
  'translation, the compiler\'s explanation of the intended meaning, and a theme label. Marathi (Manwaring, 1899; Clarendon '
  'Press) has 545 proverbs of which 338 carry an explanation of about 10 tokens; Hindi (Fallon, 1886; Medical Hall Press, '
  'Banaras) has 344 of which 305 carry a gloss of about 11 tokens; Assamese (Gurdon, 1896; Assam Secretariat Press) has 103 '
  'of which 75 carry a commentary of about 37 tokens. All three are public domain on the Internet Archive. The retrieval '
  'index is built on the explanation field, so the corpus for this experiment is effectively 718 short English texts, one per '
  'proverb, plus the 28 situation queries written for the test.')
p(f'Part II: MAGPIE (Haagsma, Bos and Nissim, 2020), the largest public corpus of potentially idiomatic expressions in '
  f'context: {I["magpie_counts"]["idiomatic"] + I["magpie_counts"]["literal"]:,} sentences from the British National Corpus, each '
  f'containing one of about 1,700 idiom types, annotated as idiomatic ({I["magpie_counts"]["idiomatic"]:,}) or literal '
  f'({I["magpie_counts"]["literal"]:,}) usage, with genre labels and a fixed training/development/test split. It is distributed '
  'under a research licence (stored with the submission) and used here for Step A. For Step B the three proverb corpora '
  'supply the positives (every proverb\'s literal translation, two carrier sentences each) and MAGPIE\'s literal sentences of '
  '5 to 25 tokens supply the negatives, giving 2,180 Marathi, 1,376 Hindi and 412 Assamese test sentences.')
p('Part III: the same three corpora, restricted to proverbs with an explanation and sampled to 60 per language so '
  'that generation on CPU stays within minutes per model. For each sampled proverb two inputs are used: the literal English '
  'translation and the romanized source text as printed in the book. The gold text is the compiler\'s explanation. The '
  'Assamese sample covers 60 of its 75 explained proverbs; the Marathi and Hindi samples are about a fifth of theirs.')

h3('2.4.1 Corpus screenshots and statistical analysis')
fig('../cca1/report/figures/PanelB_16_category_distribution.png',
    'Part I: number of proverbs per shared category and language in the three CCA1 corpora (from the CCA1 analysis).',
    'Society and human character dominate in all three corpora and nature imagery is third; the indexes therefore cover similar ground across languages, which is what lets one set of situation queries be written in the same style for all three.')
fig('report/figures/v2_idiom_detection/fig1.png',
    'Part II: MAGPIE corpus analysis, usage-label counts and sentence lengths.',
    'Idiomatic uses outnumber literal ones three to one, so the majority baseline is 0.746 and the literal class is the hard one; sentences are mostly 15 to 30 tokens, far longer than the proverbs, which matters when the two are mixed in Step B.', width=4.6)
fig('../cca1/report/figures/PanelB_16_assamese_fig2.png',
    'Part III: token-length distributions of the Assamese proverb, its literal translation and its commentary (from the CCA1 analysis).',
    'Gurdon\'s commentary is usually several times longer than the proverb. An answer scored by similarity against it can only ever cover part of that text, so raw similarity would be low for everyone. That is the reason the benchmark reports a margin over a random explanation instead.', width=4.6)

p('What the data looks like. The next tables show a few rows from each corpus file, a few MAGPIE rows, and one table that puts proverb records and idiom records side by side so the two can be compared.')
for L in LANGS:
    table([('id', 'Romanized proverb', 'Literal translation', 'Recorded meaning')] + [tuple(r) for r in SR['corpus'][L]],
          cap=f'{L} corpus file, sample rows.', size=8.5, key=f'data_{L}',
          inf={'Marathi': 'The recorded meaning is a single sentence and the translation is often longer than it, so the Marathi index has the least text to match a situation against.',
               'Hindi': 'Fallon writes short literal glosses and a meaning of similar length; the romanized line is the longest field, which the models cannot read.',
               'Assamese': 'Gurdon\'s commentaries run to several sentences and carry concrete nouns, which is why the lexical index does comparatively well on this corpus.'}[L])
table([('Sentence', 'Idiom', 'Usage label', 'Split')] + [tuple(r) for r in SR['magpie']],
      cap='MAGPIE rows: sentence, the idiom it contains, the annotated usage label and the split.', size=8.5, key='data_mag',
      inf='The same idiom string appears with both labels, so the label depends on the surrounding sentence and not on the idiom; this is the property the detector has to learn.')
table([('Record type', 'Expression', 'Literal translation or context', 'Meaning or usage label')] + [tuple(r) for r in SR['records']],
      cap='Record of proverbs and idioms: two proverbs per corpus with literal translation and intended meaning, and three MAGPIE idiom occurrences with their usage label.', size=8.5, key='records',
      inf='A proverb record carries its meaning as free text written by the compiler, while an idiom record carries only a usage label; this is why proverb experiments are scored by similarity to a text and the idiom experiment by classification accuracy.')

# ---------- 2.5 Implementation ----------
h2('2.5 Implementation')
p('Part I (PanelB_16_CCA3_v2_reverse_retrieval.ipynb): the notebook loads the three corpora, builds a TF-IDF '
  'vectorizer and a LaBSE embedding matrix over each corpus\'s explanations, and defines rank_ids(language, query, model), '
  'which returns proverb ids ordered by cosine similarity to the query. The 28 situation queries are scored for both indexes, '
  'and Hit@1, Hit@5 and MRR are tabulated with a random baseline computed from the index size. The suggest() function wraps '
  'rank_ids and returns the top proverbs with translation and meaning. The whole notebook takes about a minute on a laptop CPU.')
p('Part II (PanelB_16_CCA3_v2_idiom_detection.ipynb): the notebook reads the MAGPIE file line by line and drops everything '
  'except the rows labelled idiomatic or literal. On the training split it fits a scikit-learn pipeline, a TfidfVectorizer over '
  'unigrams and bigrams followed by LogisticRegression with balanced class weights. On the test split it prints accuracy and '
  'macro-F1, precision and recall for each class, the confusion matrix, and the features with the largest weights. After that it '
  'builds the Step B sets, one per language, from the carrier templates and runs the same pipeline under 5-fold cross-validation. '
  'is_figurative() takes any sentence and returns the two class probabilities.')
p('Part III (PanelB_16_CCA3_v2_llm_benchmark.ipynb): the notebook loads the two models with the transformers '
  'library (Qwen through its chat template with left padding; FLAN-T5 as a sequence-to-sequence model), prompts each model '
  'in batches of eight for every sampled proverb under both inputs, embeds the answers with LaBSE, and computes the '
  'similarity to the gold explanation, the control similarity to a random explanation, and the margin per proverb. Results '
  'are aggregated per language and system, plotted as bars and per-proverb box plots, and five Hindi examples are printed with '
  'both models\' answers. The explain() function returns a model answer for any proverb.')

p('Data trained upon. Reverse retrieval and the language-model benchmark have no training step: the index is built directly from the explanations shown above, and the models are used as released. The idiom detector is the one trained component; the two tables below show rows of the data it was trained on.')
table([('Sentence', 'Idiom', 'Label')] + [tuple(r) for r in SR['train_a']],
      cap='Training data for Step A: six rows sampled from the MAGPIE training split of 38,716 sentences, with the idiom and the usage label the detector learns to predict.', size=8.5, key='train_a',
      inf='The detector sees whole sentences, not the idiom alone, so the words around the idiom are what it learns from.')
table([('Carrier sentence', 'Label', 'Source')] + [tuple(r) for r in SR['train_b']],
      cap='Data for Step B: proverbs from the three corpora and real literal MAGPIE sentences placed in the same carrier templates, labelled proverb or plain.', size=8.5, key='train_b',
      inf='Both classes share the same six carrier phrases, so the detector cannot use the phrase as a shortcut and has to decide from the embedded content.')
p('Chatbot interface (team): a single Python script with no dependencies beyond those of the notebooks. At start-up it loads the three corpora, embeds every explanation and literal translation with LaBSE, and trains the idiom detector on the MAGPIE training split (about a minute in total). A message is routed by simple rules: the prefix figurative: sends the sentence to the detector, the prefix explain: or a question of the form what does ... mean sends the text to the interpreter, and anything else is treated as a situation and sent to reverse retrieval. The interpreter first looks the text up in the corpora (LaBSE similarity to the literal translations, plus a substring match on the romanized form) and, if a close entry exists, prints the recorded meaning; it then asks Qwen2.5-0.5B-Instruct for a one-sentence meaning, loaded on first use, and prints the similarity between the two. Commands /lang and /llm restrict the corpus and switch the model off or on. Each reply says which of the three parts answered it. The figure below is a real session, not a mock-up.')
fig('report/figures/chatbot_transcript.png', 'A session with the team chatbot covering the three experiments: reverse retrieval in all languages and in Hindi only, idiom detection on a figurative and a literal sentence, and interpretation with the language model off and on.',
    'The situation query returns the intended Marathi proverb first at 0.54 similarity; the two detector calls show the literal minority-class weakness seen in Section 2.6.2 (the literal choir sentence is still scored idiomatic at 0.60); and the interpretation call reproduces the benchmark finding live, with the model\'s confident but wrong meaning scoring 0.14 against the recorded one, which is why the bot shows both.', width=6.2)

# ---------- 2.6 Results ----------
h2('2.6 Results')
h3('2.6.1 Part I: reverse retrieval')
table([('Language', 'Index', 'Hit@1', 'Hit@5', 'MRR')] +
      [(L, {'tfidf': 'TF-IDF', 'labse': 'LaBSE', 'random': 'Random'}[m], rs[f'{L}/{m}']['hit_at_1'], rs[f'{L}/{m}']['hit_at_5'], rs[f'{L}/{m}']['mrr'])
       for L in LANGS for m in ['tfidf', 'labse', 'random']],
      cap='Reverse retrieval on the hand-written situation queries (10 Marathi, 8 Hindi, 10 Assamese).',
      inf='Both indexes are far above the random baseline in every language; LaBSE has the higher MRR for Marathi and Hindi and TF-IDF for Assamese.')
rv = 'report/figures/v2_reverse_retrieval'
for i, L in enumerate(LANGS):
    b = 'LaBSE' if rs[f'{L}/labse']['mrr'] >= rs[f'{L}/tfidf']['mrr'] else 'TF-IDF'
    fig(f'{rv}/fig{i + 1}.png', f'{L} reverse retrieval: Hit@1, Hit@5 and MRR for the TF-IDF and LaBSE indexes against the random baseline.',
        f'The target proverb is in the top five for {max(rs[f"{L}/tfidf"]["hit_at_5"], rs[f"{L}/labse"]["hit_at_5"])*100:.0f} percent of the queries at best, '
        f'against {rs[f"{L}/random"]["hit_at_5"]*100:.1f} percent by chance; {b} has the better MRR ({max(rs[f"{L}/labse"]["mrr"], rs[f"{L}/tfidf"]["mrr"]):.3f}).', key=f'rev_{L}')
fig(f'{rv}/fig4.png', 'Rank of the target proverb for every situation query, by language and index; points left of the dashed line are top-5 hits.',
    'Misses are not near misses: when an index fails it tends to rank the target far down the list, which means the failed queries describe the situation in a way the explanation does not, rather than the index being slightly off.', width=5.2)
fig(f'{rv}/fig5.png', 'Mean reciprocal rank by language and index; dotted lines are the random baselines.',
    'LaBSE leads for Marathi and Hindi and TF-IDF leads for Assamese, where the long Gurdon commentaries share concrete words with the situations; both are an order of magnitude above random in every language.', key='rev_mrr')
fig(f'{rv}/fig6.png', 'LaBSE Hit@5 against the mean length of the indexed explanations.',
    'Retrieval is better for the two corpora whose explanations are longer. Marathi explanations are a single sentence, so the index simply has less text to match a query against.', key='rev_len')

p('Success and failure cases. Out of the 28 queries, the table below picks the ones where LaBSE put the target proverb first, and the ones where the target did not make the top five at all, along with what came back first instead.')
revc = pd.DataFrame(CASES['reverse'])
hits = revc[revc['rank'] == 1].head(3); misses = revc[revc['rank'] > 5].sort_values('rank', ascending=False).head(3)
rows = [('Outcome', 'Language', 'Situation query', 'Target proverb (literal)', 'Returned first', 'Rank of target')]
for _, r in hits.iterrows(): rows.append(('success', r.language, r.query, r.target, r.returned, r['rank']))
for _, r in misses.iterrows(): rows.append(('failure', r.language, r.query, r.target, r.returned, r['rank']))
table(rows, cap='Reverse-retrieval success and failure cases (LaBSE index).', size=8.5,
      inf='There is a pattern in the misses. The query describes an outcome, say a small shortfall or someone who spends recklessly, while the compiler\'s note describes a cause or paints a scene. Nothing in the words or in the embedding links the two. The hits are the queries that happen to paraphrase the recorded meaning quite closely.')

h3('2.6.2 Part II: idiom identification in running text')
mg = I['magpie']; pc = mg['per_class']
table([('Set', 'Sentences', 'Accuracy', 'Macro-F1', 'Baseline'),
       ('MAGPIE test (Step A)', f'{mg["test"]:,}', mg['acc'], mg['macro_f1'], f'majority {mg["majority_acc"]}')] +
      [(f'{L} proverbs in carriers (Step B)', f'{I[f"step_b_{L.lower()}"]["n"]:,}', I[f'step_b_{L.lower()}']['acc'], I[f'step_b_{L.lower()}']['macro_f1'], 'chance 0.5') for L in LANGS],
      cap='What the detector scores on real sentences and on the three proverb corpora.',
      inf='Step A on real sentences is the honest number; the higher Step B scores partly reflect the register gap between 1890s book English and modern sentences.')
iv = 'report/figures/v2_idiom_detection'
fig(f'{iv}/fig2.png', 'Confusion matrix on the MAGPIE test split (4,840 real sentences).',
    f'Recall is {pc["idiomatic"]["recall"]:.3f} for idiomatic uses and {pc["literal"]["recall"]:.3f} for literal ones. Most of the mistakes go one way: literal sentences called idiomatic. That is what you would expect when the training data has three idiomatic examples for every literal one.', key='id_cm')
fig(f'{iv}/fig3.png', 'Precision, recall and F1 per class on MAGPIE; the dotted line is the majority-class accuracy.',
    f'Precision is lower on the literal side ({pc["literal"]["precision"]:.3f}). Roughly one in three sentences the detector calls literal is in fact idiomatic. A chatbot built on it should therefore show the probability and not just a label.', key='id_pr')
fig(f'{iv}/fig4.png', 'Features with the largest weights on each side of the MAGPIE detector.',
    'The literal side is full of concrete, physical words. The idiomatic side is mostly discourse and evaluation words. In other words the detector has picked up the register in which people use figurative language, not a list of idioms, and that is what lets it work on proverbs it has never seen.', width=4.4, key='id_feat')
fig(f'{iv}/fig5.png', 'Step B confusion matrices for Marathi, Hindi and Assamese proverbs in carrier sentences (5-fold cross-validation).',
    'Errors are few and balanced in all three languages; the smallest set (Assamese, 412 sentences) has the most, as expected from its size.', width=5.4, key='id_b')
fig(f'{iv}/fig6.png', 'Detection accuracy on the three proverb corpora (Step B) next to the real-text result (Step A).',
    'Step B accuracies of 0.91 to 0.94 are higher than Step A because of the register difference between 1890s book English and modern BNC sentences; the honest estimate of real-text detection is the Step A bar.', key='id_bar')

p('Success and failure cases from the MAGPIE test split, with the detector\'s probability of idiomatic usage.')
rows = [('Outcome', 'Sentence', 'Idiom', 'True', 'Predicted', 'P(idiomatic)')]
for r in CASES['idiom']: rows.append((r['outcome'], r['sentence'], r['idiom'], r['true'], r['predicted'], r['p_idiomatic']))
table(rows, cap='Idiom-detection success and failure cases.', size=8.5,
      inf='The failures are the two directions the matrix predicts: a literal sentence with vivid wording read as idiomatic, and an idiom in quotation marks inside a plain report read as literal. Both are cases where the register cue the detector relies on points the wrong way.')

h3('2.6.3 Part III: language-model interpretation benchmark')
systems = ['Qwen2.5-0.5B / literal_en', 'Qwen2.5-0.5B / romanized', 'flan-t5-base / literal_en', 'flan-t5-base / romanized', 'echo baseline']
rows = [('System',) + tuple(f'{L}: margin' for L in LANGS)]
for s in systems:
    rows.append((s,) + tuple(f'{qget(L, s, "margin"):+.3f}' for L in LANGS))
table(rows, cap='Mean margin (similarity to the gold explanation minus similarity to a random explanation) per system and language, 60 proverbs each.',
      inf='The echo baseline has the largest margin in every language, so neither model adds meaning beyond what the proverb text already carries; romanized input gives margins near zero.')
qv = 'report/figures/v2_llm_benchmark'
for i, L in enumerate(LANGS):
    ql = qget(L, 'Qwen2.5-0.5B / literal_en', 'margin'); qr = qget(L, 'Qwen2.5-0.5B / romanized', 'margin'); e = qget(L, 'echo baseline', 'margin')
    fig(f'{qv}/fig{i + 1}.png', f'{L}: mean similarity of each system\'s answer to the compiler\'s explanation (blue) against the control (grey), for both inputs and the echo baseline.',
        f'With the literal translation as input Qwen\'s margin is {ql:+.3f}, below the echo baseline\'s {e:+.3f}; with romanized {L} it is {qr:+.3f}. '
        'The model writes a fluent meaning that is no closer to the recorded one than the proverb text itself, and gets nothing from the source-language form.', key=f'llm_{L}')
fig(f'{qv}/fig4.png', 'Per-proverb margin distributions for the Qwen conditions and the echo baseline, by language.',
    'For most proverbs, in every language, the echo baseline is above zero. Qwen with the literal translation as input is spread widely on both sides of zero, and with romanized input it sits on zero. So the model helps on some proverbs and hurts on about as many.', width=5.2, key='llm_box')
fig(f'{qv}/fig5.png', 'Mean margin for each system over the three languages. The echo baseline is the bar a model has to clear.',
    'The order never changes across the three languages. Echo comes first, the models with literal input next, and the models with romanized input last, close to zero. The wall CCA1 ran into on romanized text is still there when the model generates instead of retrieves.', key='llm_margin')

p('Success and failure cases. We drew a fresh sample of 24 proverbs, gave Qwen2.5-0.5B-Instruct the literal translations, and kept the answers with the highest and the lowest margins.')
rows = [('Outcome', 'Language', 'Proverb (literal)', 'Recorded meaning', 'Model answer', 'Margin')]
for r in CASES['llm']: rows.append((r['outcome'], r['language'], r['proverb'], r['gold'], r['answer'], f"{r['margin']:+.2f}"))
table(rows, cap='Best and worst answers from the language model.', size=8.5,
      inf='The good answers come from proverbs whose literal text already reads like a general rule; a paraphrase of it lands close to what the compiler wrote. The bad ones come from proverbs built around one concrete image, a fried bird, a vegetable out of season. There the model explains the image and misses the point, and it does so with full confidence.')

# ---------- 2.7 Discussion ----------
h2('2.7 Discussion')
def bestidx(L): return 'LaBSE' if rs[f'{L}/labse']['mrr'] >= rs[f'{L}/tfidf']['mrr'] else 'TF-IDF'
p(f'Part I: Figures {FN["rev_Marathi"]} to {FN["rev_len"]} give a positive answer to RQ1 for all three corpora. Write a situation in everyday words '
  f'and the target proverb turns up in the top five for {rs["Hindi/labse"]["hit_at_5"]*100:.0f} percent of the Hindi queries and '
  f'{max(rs["Assamese/labse"]["hit_at_5"], rs["Assamese/tfidf"]["hit_at_5"])*100:.0f} percent of the Assamese ones. Chance would give under 7 percent. '
  f'That is good enough to use as a suggestion tool. For Marathi and Hindi the semantic index wins (Figure {FN["rev_mrr"]}). We expected this, '
  'because the queries were written to avoid the words of the explanation. For Assamese the lexical index wins instead, and the reason '
  f'is Gurdon: his commentaries are long and full of concrete nouns, which gives TF-IDF something to match. Figure {FN["rev_len"]} links '
  'retrieval quality to explanation length, and that is the most useful thing the chatbot can take from Part I. The shorter the '
  'recorded meaning, the more a suggestion has to lean on the semantic index. One caveat. The query sets are small, so the hit rates '
  'carry wide uncertainty and should be read as a demonstration, not as a benchmark.')
p(f'Part II: Figures {FN["id_cm"]} and {FN["id_pr"]} show that the CCA1 recipe, TF-IDF features with logistic regression, does separate '
  f'figurative from literal usage in real sentences: {mg["acc"]} accuracy against a majority baseline of {mg["majority_acc"]}. Its weak '
  f'spot is the literal class, the minority, at {pc["literal"]["precision"]:.3f} precision. Figure {FN["id_feat"]} is the reason the detector '
  'transfers at all. What it has learned is the register of figurative use, evaluation and discourse words on one side and concrete '
  'physical words on the other, rather than a stock of idioms. Proverbs from Marathi, Hindi and Assamese that it has never seen trigger '
  f'the same cues (Figures {FN["id_b"]} and {FN["id_bar"]}). The Step B numbers come with a caveat we have stated already: 1890s translations '
  'and modern BNC sentences differ in register, and that gap inflates the scores, so the real-text number is the one to quote. RQ2 is '
  'answered. The recipe works on real text and it carries over. What is still missing is a corpus of our languages\' proverbs inside '
  'genuine running text.')
p(f'Part III: Figures {FN["llm_Marathi"]} to {FN["llm_margin"]} answer RQ3 in the negative, consistently. In all three languages the echo baseline has '
  f'the largest margin (Marathi {qget("Marathi", "echo baseline", "margin"):+.3f}, Hindi {qget("Hindi", "echo baseline", "margin"):+.3f}, '
  f'Assamese {qget("Assamese", "echo baseline", "margin"):+.3f}); a small instruction-tuned model given the literal translation produces a '
  'fluent meaning that is no closer to the compiler\'s than the proverb itself, and given the romanized source text its margin '
  f'is near zero (Figure {FN["llm_margin"]}). The per-proverb distributions in Figure {FN["llm_box"]} show this is not an average hiding a bimodal result: the '
  'literal-input condition helps about as often as it hurts. This is the CCA1 finding, that romanized historical text is '
  'opaque to pretrained models, now observed for generation as well as retrieval. Larger models may interpret better, but the '
  'controls would apply unchanged, and the chatbot therefore shows the model\'s answer next to the recorded meaning rather '
  'than in place of it.')

# ---------- 2.8 Conclusion ----------
h2('2.8 Conclusion')
p('Three extensions of the CCA1 work were implemented on all three proverb corpora with one shared code path. '
  'Part I built situation-to-proverb retrieval and showed it finds the right proverb in the top five for most '
  'hand-written situations in every language, with the semantic index ahead where explanations are short. Part II '
  'built an idiom-usage detector on 48,395 real English sentences, reached 0.862 accuracy against a 0.746 baseline, showed that '
  'it works from the register of figurative use, and transferred it to the three proverb corpora. Part III built a '
  'benchmark with controls that separate interpretation from restatement and found that two small open language models do '
  'not beat the proverb\'s own text in any language, and gain nothing from romanized input. Each experiment ends in a '
  'function, and the team chatbot joins the three into one interface that reports the recorded meaning alongside any model answer. The practical conclusion is the same as CCA1\'s '
  'and now rests on more evidence: native-script recovery is the precondition for embedding and generative models to '
  'contribute on the source-language text.')

# ---------- 2.9 References ----------
h2('2.9 References')
for ref in [
    'Chung, H. W., Hou, L., Longpre, S., et al. (2022). Scaling instruction-finetuned language models. arXiv:2210.11416.',
    'Fallon, S. W. (1886). A dictionary of Hindustani proverbs. Banaras: Medical Hall Press. Corpus source: https://archive.org/details/in.ernet.dli.2015.42145',
    'Feng, F., Yang, Y., Cer, D., Arivazhagan, N., & Wang, W. (2022). Language-agnostic BERT sentence embedding. Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics, 878-891.',
    'Gurdon, P. R. (1896). Some Assamese proverbs. Shillong: Assam Secretariat Printing Office. Corpus source: https://archive.org/details/someassameseprov00gurdrich',
    'Haagsma, H., Bos, J., & Nissim, M. (2020). MAGPIE: A large corpus of potentially idiomatic expressions. Proceedings of the 12th Language Resources and Evaluation Conference, 279-287. Corpus: https://github.com/hslh/magpie-corpus',
    'Liu, C. C., Koto, F., Baldwin, T., & Gurevych, I. (2024). Are multilingual LLMs culturally-diverse reasoners? An investigation into multicultural proverbs and sayings. Proceedings of NAACL 2024.',
    'Manwaring, A. (1899). Marathi proverbs. Oxford: Clarendon Press. Corpus source: https://archive.org/details/marathiproverbs00manwgoog',
    'Qwen Team (2024). Qwen2.5 technical report. arXiv:2412.15115.',
    'Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using Siamese BERT-networks. Proceedings of EMNLP-IJCNLP 2019, 3982-3992.',
    'Tan, M., & Jiang, J. (2021). Does BERT understand idioms? A probing-based empirical study of BERT encodings of idioms. Proceedings of RANLP 2021, 1397-1407.',
]:
    doc.add_paragraph(ref)

doc.save('v3/PanelB_16_LCA3_MiniProject_Report.docx')
print('v2 report written:', fignum, 'figures')
