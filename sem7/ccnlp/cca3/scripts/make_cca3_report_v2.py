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
def fig(path, name, inf=None, width=3.5, key=None):
    global fignum; fignum += 1
    if key: FN[key] = fignum
    par = doc.add_paragraph(); par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.add_run().add_picture(path, width=Inches(width))
    caption(f'Figure {fignum}: {name}')
    if inf:
        ip = doc.add_paragraph(); r = ip.add_run('Inference: '); r.bold = True; ip.add_run(inf)
    return fignum
def table(rows):
    t = doc.add_table(rows=len(rows), cols=len(rows[0])); t.style = 'Table Grid'
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            c = t.rows[i].cells[j]; c.text = str(cell)
            if i == 0: c.paragraphs[0].runs[0].bold = True
    _merge_repeats(t, rows)

# ---------- Team information / problem statement ----------
p('School of Computer Science & Engineering, MIT-WPU', center=True)
p('CCA3 — Cloud Computing & Natural Language Processing — Panel B, Team 16', center=True, bold=True)
doc.add_heading('Three Follow-up Experiments on the Indian Proverb Corpora: Reverse Retrieval, Idiom Detection in Text, and a Language-Model Interpretation Benchmark', level=0)
h1('Team information')
table([('Member', 'PRN', 'Research question / model'),
       ('Sahish Nagulwar', '1032233310', 'Reverse retrieval: situation to proverb (LaBSE and TF-IDF indexes)'),
       ('Ibrahim Ansari', '1032233145', 'Idiom identification in running text (detector trained on MAGPIE)'),
       ('Chayan Raj Bharati', '1032233134', 'Language-model interpretation benchmark (Qwen2.5-0.5B-Instruct, FLAN-T5-base)')])
h1('Problem statement')
p('Develop a multilingual NLP framework that identifies Indian idioms and distinguishes their literal meaning from culturally '
  'intended figurative meaning across Indian languages, while modeling cultural context and linguistic variation. CCA3 '
  'extends the CCA1 work on the Marathi, Hindi and Assamese proverb corpora with three follow-up experiments, one per member, '
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
p('CCA3 follows the plan written after CCA1 and implements three of its extensions, one per member, each run on all three '
  'corpora with one shared code path so the languages can be compared fairly. The three were chosen because together they '
  'cover the three things a user would ask a proverb system to do: find a proverb for a situation (reverse retrieval), tell '
  'whether a sentence is using a proverb figuratively (idiom detection), and say what a proverb means (interpretation, here '
  'tested on language models). Each notebook ends in a plain function (suggest, is_figurative, explain) so the three '
  'experiments can be joined into one chatbot interface. A fourth planned extension, cross-language equivalence linking, was '
  'implemented in the first round of CCA3 notebooks but is left out of this report because its yield was too small to '
  'evaluate properly.')

# ---------- 2.1 RQs ----------
h2('2.1 Research questions')
p('RQ1 (Sahish Nagulwar): Given a plain description of a situation, can the right proverb be retrieved from the explanation '
  'index of each corpus, and does a semantic index (LaBSE) do better than a lexical one (TF-IDF)?')
p('RQ2 (Ibrahim Ansari): Can a detector that separates figurative from literal usage, trained on real English sentences, be '
  'built with the CCA1 recipe, and does it transfer to Marathi, Hindi and Assamese proverbs placed in running text?')
p('RQ3 (Chayan Raj Bharati): When a small open language model is asked what a proverb means, does its answer come closer to '
  'the compiler\'s recorded meaning than the proverb\'s own literal text does, and does that hold when the input is the '
  'romanized source language rather than English?')

# ---------- 2.2 Contributions ----------
h2('2.2 Research contributions')
p(f'Sahish Nagulwar: a situation-to-proverb retrieval index for each of the three corpora, a test set of {sum(R["n_queries"].values())} '
  'hand-written situation queries (written by members who did not build the index they test), an evaluation of lexical '
  'against semantic indexing on it, and the suggest() interface that returns proverbs with their literal translation and '
  'recorded meaning.')
p(f'Ibrahim Ansari: an idiom-usage detector trained on {I["magpie"]["train"]:,} real English sentences and tested on {I["magpie"]["test"]:,}, '
  'with per-class precision and recall and an analysis of the features it relies on; the transfer of the same recipe to '
  'the three proverb corpora in carrier sentences with real literal sentences as negatives; and the is_figurative() interface.')
p('Chayan Raj Bharati: a proverb-interpretation benchmark of 60 proverbs per language on which two open language models are '
  'scored under two input conditions, with a random-explanation control and an echo baseline that separate interpretation '
  'from restatement; per-proverb margin distributions; and the explain() interface, which shows the model\'s answer next to '
  'the recorded meaning.')

p('Shared: a terminal chatbot (PanelB_16_CCA3_chatbot.py) that routes each message to one of the three experiments and reports which one answered, with a language filter and a switch for the language model. It was built jointly and is credited to the team rather than to one member.')

# ---------- 2.3 Methodology ----------
h2('2.3 Methodology')
p('Sahish Nagulwar: for each corpus, the explanations of all proverbs with a recorded meaning (338 Marathi, 305 Hindi, 75 '
  'Assamese) are indexed twice, with TF-IDF (word level, English stop words removed) and with LaBSE sentence embeddings '
  '(normalized, cosine similarity). A query is a one-sentence situation description; the proverbs are ranked by the '
  'similarity of their explanation to it. Each query targets one proverb, and Hit@1, Hit@5 and mean reciprocal rank are '
  'computed against a random-ranking baseline. The descriptions avoid copying words from the explanation.')
p('Ibrahim Ansari: Step A trains TF-IDF over word unigrams and bigrams with logistic regression (balanced class weights) on '
  'the MAGPIE training split and tests on its test split, labels idiomatic versus literal usage. Step B applies the same '
  'recipe to each language: the proverbs (literal translations) are placed in six carrier sentences as positives, and real '
  'literal MAGPIE sentences are placed in the same carriers as negatives, under 5-fold cross-validation; the carriers cancel, '
  'so the classifier must decide from content. Step B carries a stated confound, since 1890s book English and modern BNC '
  'English differ in register, and Step A is treated as the honest number.')
p('Chayan Raj Bharati: 60 proverbs with explanations per language (random sample, seed 42). Qwen2.5-0.5B-Instruct and '
  'FLAN-T5-base are prompted for a one-sentence meaning, once with the literal translation and once with the romanized source '
  'text. The answer is scored by LaBSE similarity to the gold explanation; the control is its similarity to a random other '
  'explanation; the margin is the difference. The echo baseline scores the literal translation itself the same way. Both '
  'models run on CPU with greedy or two-beam decoding.')

fig('report/figures/extras/methodology.png', 'Methodology of CCA3: the three corpora and MAGPIE feed three experiments, one per member, whose functions are joined in the team chatbot; all numbers come from the saved metrics files.',
    'The three experiments share their inputs and their evaluation style but not their models, so a difference between them is a difference in task, not in data preparation.', width=5.0, key='method')

# ---------- 2.4 Corpora ----------
h2('2.4 Description of corpora')
p('Sahish Nagulwar: the three CCA1 corpora, reused unchanged. Each row has the romanized proverb, its literal English '
  'translation, the compiler\'s explanation of the intended meaning, and a theme label. Marathi (Manwaring, 1899; Clarendon '
  'Press) has 545 proverbs of which 338 carry an explanation of about 10 tokens; Hindi (Fallon, 1886; Medical Hall Press, '
  'Banaras) has 344 of which 305 carry a gloss of about 11 tokens; Assamese (Gurdon, 1896; Assam Secretariat Press) has 103 '
  'of which 75 carry a commentary of about 37 tokens. All three are public domain on the Internet Archive. The retrieval '
  'index is built on the explanation field, so the corpus for this experiment is effectively 718 short English texts, one per '
  'proverb, plus the 28 situation queries written for the test.')
p(f'Ibrahim Ansari: MAGPIE (Haagsma, Bos and Nissim, 2020), the largest public corpus of potentially idiomatic expressions in '
  f'context: {I["magpie_counts"]["idiomatic"] + I["magpie_counts"]["literal"]:,} sentences from the British National Corpus, each '
  f'containing one of about 1,700 idiom types, annotated as idiomatic ({I["magpie_counts"]["idiomatic"]:,}) or literal '
  f'({I["magpie_counts"]["literal"]:,}) usage, with genre labels and a fixed training/development/test split. It is distributed '
  'under a research licence (stored with the submission) and used here for Step A. For Step B the three proverb corpora '
  'supply the positives (every proverb\'s literal translation, two carrier sentences each) and MAGPIE\'s literal sentences of '
  '5 to 25 tokens supply the negatives, giving 2,180 Marathi, 1,376 Hindi and 412 Assamese test sentences.')
p('Chayan Raj Bharati: the same three corpora, restricted to proverbs with an explanation and sampled to 60 per language so '
  'that generation on CPU stays within minutes per model. For each sampled proverb two inputs are used: the literal English '
  'translation and the romanized source text as printed in the book. The gold text is the compiler\'s explanation. The '
  'Assamese sample covers 60 of its 75 explained proverbs; the Marathi and Hindi samples are about a fifth of theirs.')

h3('2.4.1 Corpus screenshots and statistical analysis')
fig('../cca1/report/figures/PanelB_16_category_distribution.png',
    'Sahish Nagulwar: number of proverbs per shared category and language in the three CCA1 corpora (from the CCA1 analysis).',
    'Society and human character dominate in all three corpora and nature imagery is third; the indexes therefore cover similar ground across languages, which is what lets one set of situation queries be written in the same style for all three.')
fig('report/figures/v2_idiom_detection/fig1.png',
    'Ibrahim Ansari: MAGPIE corpus analysis, usage-label counts and sentence lengths.',
    'Idiomatic uses outnumber literal ones three to one, so the majority baseline is 0.746 and the literal class is the hard one; sentences are mostly 15 to 30 tokens, far longer than the proverbs, which matters when the two are mixed in Step B.', width=4.6)
fig('../cca1/report/figures/PanelB_16_assamese_fig2.png',
    'Chayan Raj Bharati: token-length distributions of the Assamese proverb, its literal translation and its commentary (from the CCA1 analysis).',
    'The commentary is several times longer than the proverb itself, so an answer scored against it by similarity can only match part of it; this is why the benchmark uses a margin over a random explanation rather than the raw similarity.', width=4.6)

p('Screenshots of the data as used. Figures below show sample rows of each corpus file, a sample of MAGPIE rows, and a record table that places proverbs and idiom occurrences side by side.')
fig('report/figures/extras/data_marathi.png', 'Marathi corpus file, sample rows (romanized proverb, literal translation, recorded meaning).', None, width=5.0, key='data_mr')
fig('report/figures/extras/data_hindi.png', 'Hindi corpus file, sample rows.', None, width=5.0, key='data_hi')
fig('report/figures/extras/data_assamese.png', 'Assamese corpus file, sample rows.', None, width=5.0, key='data_as')
fig('report/figures/extras/data_magpie.png', 'MAGPIE rows: sentence, the idiom it contains, the annotated usage label and the split.', None, width=5.0, key='data_mag')
fig('report/figures/extras/records.png', 'Record of proverbs and idioms: two proverbs per corpus with literal translation and intended meaning, and three MAGPIE idiom occurrences with their usage label.',
    'A proverb record carries its meaning as free text written by the compiler, while an idiom record carries only a usage label; this is why proverb experiments are scored by similarity to a text and the idiom experiment by classification accuracy.', width=5.2, key='records')

# ---------- 2.5 Implementation ----------
h2('2.5 Implementation')
p('Sahish Nagulwar (PanelB_16_CCA3_v2_reverse_retrieval.ipynb): the notebook loads the three corpora, builds a TF-IDF '
  'vectorizer and a LaBSE embedding matrix over each corpus\'s explanations, and defines rank_ids(language, query, model), '
  'which returns proverb ids ordered by cosine similarity to the query. The 28 situation queries are scored for both indexes, '
  'and Hit@1, Hit@5 and MRR are tabulated with a random baseline computed from the index size. The suggest() function wraps '
  'rank_ids and returns the top proverbs with translation and meaning. Everything runs in about a minute on CPU.')
p('Ibrahim Ansari (PanelB_16_CCA3_v2_idiom_detection.ipynb): the notebook reads MAGPIE from JSON lines, keeps the idiomatic '
  'and literal rows, trains a scikit-learn pipeline (TfidfVectorizer with 1-2-grams, LogisticRegression with balanced class '
  'weights) on the training split and reports accuracy, macro-F1, per-class precision and recall, the confusion matrix and '
  'the strongest features on the test split. It then builds the Step B sets for each language with the carrier templates and '
  'runs 5-fold cross-validation with the same pipeline. The is_figurative() function returns the class probabilities for any '
  'sentence.')
p('Chayan Raj Bharati (PanelB_16_CCA3_v2_llm_benchmark.ipynb): the notebook loads the two models with the transformers '
  'library (Qwen through its chat template with left padding; FLAN-T5 as a sequence-to-sequence model), prompts each model '
  'in batches of eight for every sampled proverb under both inputs, embeds the answers with LaBSE, and computes the '
  'similarity to the gold explanation, the control similarity to a random explanation, and the margin per proverb. Results '
  'are aggregated per language and system, plotted as bars and per-proverb box plots, and five Hindi examples are printed with '
  'both models\' answers. The explain() function returns a model answer for any proverb.')

p('Data trained upon. Reverse retrieval and the language-model benchmark have no training step: the index is built directly from the explanations shown above, and the models are used as released. The idiom detector is the one trained component; the two figures below show rows of the data it was trained on.')
fig('report/figures/extras/train_magpie.png', 'Training data for Step A: six rows sampled from the MAGPIE training split of 38,716 sentences, with the idiom and the usage label the detector learns to predict.', None, width=5.0, key='train_a')
fig('report/figures/extras/train_stepb.png', 'Data for Step B: proverbs from the three corpora and real literal MAGPIE sentences placed in the same carrier templates, labelled proverb or plain.',
    'Both classes share the same six carrier phrases, so the detector cannot use the phrase as a shortcut and has to decide from the embedded content.', width=5.0, key='train_b')
p('Chatbot interface (team): a single Python script with no dependencies beyond those of the notebooks. At start-up it loads the three corpora, embeds every explanation and literal translation with LaBSE, and trains the idiom detector on the MAGPIE training split (about a minute in total). A message is routed by simple rules: the prefix figurative: sends the sentence to the detector, the prefix explain: or a question of the form what does ... mean sends the text to the interpreter, and anything else is treated as a situation and sent to reverse retrieval. The interpreter first looks the text up in the corpora (LaBSE similarity to the literal translations, plus a substring match on the romanized form) and, if a close entry exists, prints the recorded meaning; it then asks Qwen2.5-0.5B-Instruct for a one-sentence meaning, loaded on first use, and prints the similarity between the two. Commands /lang and /llm restrict the corpus and switch the model off or on. Every reply names the experiment that produced it. The figure below shows a real session.')
fig('report/figures/chatbot_transcript.png', 'A session with the team chatbot covering the three experiments: reverse retrieval in all languages and in Hindi only, idiom detection on a figurative and a literal sentence, and interpretation with the language model off and on.',
    'The situation query returns the intended Marathi proverb first at 0.54 similarity; the two detector calls show the literal minority-class weakness seen in Section 2.6.2 (the literal choir sentence is still scored idiomatic at 0.60); and the interpretation call reproduces the benchmark finding live, with the model\'s confident but wrong meaning scoring 0.14 against the recorded one, which is why the bot shows both.', width=6.2)

# ---------- 2.6 Results ----------
h2('2.6 Results')
h3('2.6.1 Sahish Nagulwar: reverse retrieval')
table([('Language', 'Index', 'Hit@1', 'Hit@5', 'MRR')] +
      [(L, m.upper() if m == 'tfidf' else m.capitalize(), rs[f'{L}/{m}']['hit_at_1'], rs[f'{L}/{m}']['hit_at_5'], rs[f'{L}/{m}']['mrr'])
       for L in LANGS for m in ['tfidf', 'labse', 'random']])
caption('Table: reverse retrieval on the hand-written situation queries (10 Marathi, 8 Hindi, 10 Assamese).')
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
    'The two corpora with longer explanations retrieve better; the one-sentence Marathi explanations give the index the least to match on.', key='rev_len')

p('Success and failure cases. Table below lists, from the 28 queries, the queries where the LaBSE index ranked the target first and the queries where it missed the top five, with what was returned instead.')
revc = pd.DataFrame(CASES['reverse'])
hits = revc[revc['rank'] == 1].head(3); misses = revc[revc['rank'] > 5].sort_values('rank', ascending=False).head(3)
rows = [('Outcome', 'Language', 'Situation query', 'Target proverb (literal)', 'Returned first', 'Rank of target')]
for _, r in hits.iterrows(): rows.append(('success', r.language, r.query, r.target, r.returned, r['rank']))
for _, r in misses.iterrows(): rows.append(('failure', r.language, r.query, r.target, r.returned, r['rank']))
table(rows); caption('Table: reverse-retrieval success and failure cases (LaBSE index).')
p('The failures share a pattern: the situation names a consequence (a trivial shortfall, a reckless spender) while the recorded meaning names a cause or a scene, so neither words nor embedding bring them together; the successes are the queries that paraphrase the recorded meaning closely.')

h3('2.6.2 Ibrahim Ansari: idiom identification in running text')
mg = I['magpie']; pc = mg['per_class']
table([('Set', 'Sentences', 'Accuracy', 'Macro-F1', 'Baseline'),
       ('MAGPIE test (Step A)', f'{mg["test"]:,}', mg['acc'], mg['macro_f1'], f'majority {mg["majority_acc"]}')] +
      [(f'{L} proverbs in carriers (Step B)', f'{I[f"step_b_{L.lower()}"]["n"]:,}', I[f'step_b_{L.lower()}']['acc'], I[f'step_b_{L.lower()}']['macro_f1'], 'chance 0.5') for L in LANGS])
caption('Table: detector results on real text and on the three proverb corpora.')
iv = 'report/figures/v2_idiom_detection'
fig(f'{iv}/fig2.png', 'Confusion matrix on the MAGPIE test split (4,840 real sentences).',
    f'Idiomatic uses are recognised at {pc["idiomatic"]["recall"]:.3f} recall and literal uses at {pc["literal"]["recall"]:.3f}; the main error is literal uses predicted as idiomatic, the direction expected when idiomatic examples outnumber literal ones three to one in training.', key='id_cm')
fig(f'{iv}/fig3.png', 'Precision, recall and F1 per class on MAGPIE; the dotted line is the majority-class accuracy.',
    f'The literal class has the lower precision ({pc["literal"]["precision"]:.3f}): about a third of the sentences flagged as literal are actually idiomatic, so a chatbot using this detector should report the probability rather than a hard label.', key='id_pr')
fig(f'{iv}/fig4.png', 'The strongest features for each class in the MAGPIE detector.',
    'Features on the literal side are concrete and physical, features on the idiomatic side are discourse and evaluation words; the detector is learning the register of figurative use, not the idioms themselves, which is why it can transfer to unseen proverbs.', width=4.4, key='id_feat')
fig(f'{iv}/fig5.png', 'Step B confusion matrices for Marathi, Hindi and Assamese proverbs in carrier sentences (5-fold cross-validation).',
    'Errors are few and balanced in all three languages; the smallest set (Assamese, 412 sentences) has the most, as expected from its size.', width=5.4, key='id_b')
fig(f'{iv}/fig6.png', 'Detection accuracy on the three proverb corpora (Step B) next to the real-text result (Step A).',
    'Step B accuracies of 0.91 to 0.94 are higher than Step A because of the register difference between 1890s book English and modern BNC sentences; the honest estimate of real-text detection is the Step A bar.', key='id_bar')

p('Success and failure cases from the MAGPIE test split, with the detector\'s probability of idiomatic usage.')
rows = [('Outcome', 'Sentence', 'Idiom', 'True', 'Predicted', 'P(idiomatic)')]
for r in CASES['idiom']: rows.append((r['outcome'], r['sentence'], r['idiom'], r['true'], r['predicted'], r['p_idiomatic']))
table(rows); caption('Table: idiom-detection success and failure cases.')
p('The failures are the two directions the matrix predicts: a literal sentence with vivid wording read as idiomatic, and an idiom in quotation marks inside a plain report read as literal. Both are cases where the register cue the detector relies on points the wrong way.')

h3('2.6.3 Chayan Raj Bharati: language-model interpretation benchmark')
systems = ['Qwen2.5-0.5B / literal_en', 'Qwen2.5-0.5B / romanized', 'flan-t5-base / literal_en', 'flan-t5-base / romanized', 'echo baseline']
rows = [('System',) + tuple(f'{L}: margin' for L in LANGS)]
for s in systems:
    rows.append((s,) + tuple(f'{qget(L, s, "margin"):+.3f}' for L in LANGS))
table(rows)
caption('Table: mean margin (similarity to the gold explanation minus similarity to a random explanation) per system and language, 60 proverbs each.')
qv = 'report/figures/v2_llm_benchmark'
for i, L in enumerate(LANGS):
    ql = qget(L, 'Qwen2.5-0.5B / literal_en', 'margin'); qr = qget(L, 'Qwen2.5-0.5B / romanized', 'margin'); e = qget(L, 'echo baseline', 'margin')
    fig(f'{qv}/fig{i + 1}.png', f'{L}: mean similarity of each system\'s answer to the compiler\'s explanation (blue) against the control (grey), for both inputs and the echo baseline.',
        f'With the literal translation as input Qwen\'s margin is {ql:+.3f}, below the echo baseline\'s {e:+.3f}; with romanized {L} it is {qr:+.3f}. '
        'The model writes a fluent meaning that is no closer to the recorded one than the proverb text itself, and gets nothing from the source-language form.', key=f'llm_{L}')
fig(f'{qv}/fig4.png', 'Per-proverb margin distributions for the Qwen conditions and the echo baseline, by language.',
    'The echo baseline sits above zero for most proverbs in every language, the literal-input Qwen condition straddles zero with a wide spread, and the romanized condition is centred on zero; the model helps for some proverbs and hurts for as many.', width=5.2, key='llm_box')
fig(f'{qv}/fig5.png', 'Mean margin per system across the three languages; the echo baseline is the bar each model has to beat.',
    'The ordering is the same in all three languages: echo first, then the literal-input models, then the romanized-input models near zero. The CCA1 cross-lingual wall holds for generative models.', key='llm_margin')

p('Success and failure cases: Qwen2.5-0.5B-Instruct answers with the highest and lowest margins on a fresh sample of 24 proverbs (literal-translation input).')
rows = [('Outcome', 'Language', 'Proverb (literal)', 'Recorded meaning', 'Model answer', 'Margin')]
for r in CASES['llm']: rows.append((r['outcome'], r['language'], r['proverb'], r['gold'], r['answer'], f"{r['margin']:+.2f}"))
table(rows); caption('Table: language-model success and failure cases.')
p('The successes are proverbs whose literal text already states a general rule, so a paraphrase lands near the recorded meaning; the failures are proverbs built on a specific image (a fried bird, an out-of-season vegetable) where the model explains the image rather than the point, confidently and wrongly.')

# ---------- 2.7 Discussion ----------
h2('2.7 Discussion')
def bestidx(L): return 'LaBSE' if rs[f'{L}/labse']['mrr'] >= rs[f'{L}/tfidf']['mrr'] else 'TF-IDF'
p(f'Sahish Nagulwar: the results in Figures {FN["rev_Marathi"]} to {FN["rev_len"]} answer RQ1 positively for all three corpora. A situation written in ordinary '
  f'words retrieves the target proverb in the top five for {rs["Hindi/labse"]["hit_at_5"]*100:.0f} percent of the Hindi queries and '
  f'{max(rs["Assamese/labse"]["hit_at_5"], rs["Assamese/tfidf"]["hit_at_5"])*100:.0f} percent of the Assamese ones, with random baselines under 7 percent, '
  f'so the index is usable as a suggestion tool. The semantic index is better for Marathi and Hindi (Figure {FN["rev_mrr"]}), which is the '
  'result the queries were designed to produce, since they avoid the explanation\'s words; the lexical index wins for Assamese '
  f'because Gurdon\'s long commentaries carry enough concrete nouns to match on. Figure {FN["rev_len"]} ties retrieval quality to explanation '
  'length, which is the clearest guidance for the chatbot: the shorter the recorded meaning, the more the suggestion depends '
  'on the semantic index. The test sets are small, so the hit rates have wide uncertainty and the figures should be read as a '
  'demonstration rather than a benchmark.')
p(f'Ibrahim Ansari: Figure {FN["id_cm"]} and Figure {FN["id_pr"]} show that the CCA1 recipe, TF-IDF features with logistic regression, separates '
  f'figurative from literal usage in real sentences at {mg["acc"]} accuracy against a {mg["majority_acc"]} majority baseline, with '
  f'the literal minority class as the weak point ({pc["literal"]["precision"]:.3f} precision). Figure {FN["id_feat"]} explains why the detector '
  'transfers: it relies on the register of figurative use, evaluation and discourse words against concrete physical ones, not '
  f'on memorised idioms, so unseen Marathi, Hindi and Assamese proverbs are caught by the same cues (Figures {FN["id_b"]} and {FN["id_bar"]}). The '
  'Step B numbers are inflated by the register gap between the 1890s translations and modern BNC sentences and are reported '
  'with that caveat; the real-text figure is the one to quote. RQ2 is answered: the recipe works on real text and transfers, '
  'and the remaining gap is a corpus of our languages\' proverbs in genuine running text.')
p(f'Chayan Raj Bharati: Figures {FN["llm_Marathi"]} to {FN["llm_margin"]} answer RQ3 in the negative, consistently. In all three languages the echo baseline has '
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
p('Three extensions of the CCA1 work were implemented on all three proverb corpora with one shared code path, one per member. '
  'Sahish Nagulwar built situation-to-proverb retrieval and showed it finds the right proverb in the top five for most '
  'hand-written situations in every language, with the semantic index ahead where explanations are short. Ibrahim Ansari '
  'built an idiom-usage detector on 48,395 real English sentences, reached 0.862 accuracy against a 0.746 baseline, showed that '
  'it works from the register of figurative use, and transferred it to the three proverb corpora. Chayan Raj Bharati built a '
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

doc.save('report/PanelB_16_CCA3_Report_v2.docx')
print('v2 report written:', fignum, 'figures')
