import json
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

M = {l: json.load(open(f'report/PanelB_16_CCA3_{l}_metrics.json')) for l in ['marathi', 'hindi', 'assamese']}
MEM = [('Sahish Nagulwar', '1032233310', 'Marathi', 'marathi'),
       ('Ibrahim Ansari', '1032233145', 'Hindi', 'hindi'),
       ('Chayan Raj Bharati', '1032233134', 'Assamese', 'assamese')]
SIT_N = {'marathi': 10, 'hindi': 8, 'assamese': 10}

doc = Document()
st = doc.styles['Normal']; st.font.name = 'Times New Roman'; st.font.size = Pt(10)
fignum = 0; tabnum = 0

def h1(t): doc.add_heading(t, level=1)
def h2(t): doc.add_heading(t, level=2)
def p(t, italic=False, center=False, bold=False):
    par = doc.add_paragraph()
    if center: par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = par.add_run(t); r.italic = italic; r.bold = bold
def bullet(t): doc.add_paragraph(t, style='List Bullet')
def numbered(t): doc.add_paragraph(t, style='List Number')
def eqd(m): return {k.split('_')[1]: v for k, v in m.items() if k.startswith('equivalence_')}
def caption(t):
    par = doc.add_paragraph(); par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = par.add_run(t); r.italic = True; r.font.size = Pt(9.5)
def fig(path, cap, inf, width=3.8):
    global fignum; fignum += 1
    par = doc.add_paragraph(); par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.add_run().add_picture(path, width=Inches(width))
    caption(f'Figure {fignum}: {cap}')
    ip = doc.add_paragraph(); r = ip.add_run('Inference: '); r.bold = True; ip.add_run(inf)
def table(rows, cap):
    global tabnum; tabnum += 1
    t = doc.add_table(rows=len(rows), cols=len(rows[0])); t.style = 'Table Grid'
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            c = t.rows[i].cells[j]; c.text = str(cell)
            if i == 0: c.paragraphs[0].runs[0].bold = True
    caption(f'Table {tabnum}: {cap}')

def f3(x): return f'{x:.3f}'

# ---------- Title ----------
p('School of Computer Science & Engineering, MIT-WPU', center=True)
p('Comprehensive Course Assessment 3 (CCA3) — Cloud Computing & Natural Language Processing', center=True, bold=True)
doc.add_heading('Four Follow-up Experiments on the Indian Proverb Corpora: Reverse Retrieval, Cross-Language Linking, Idiom Detection in Text, and an LLM Interpretation Benchmark', level=0)
p('Group 16 — Panel B', center=True, bold=True)
table([('Member', 'PRN', 'Language', 'Notebook')] + [(n, pr, L, f'PanelB_16_CCA3_{l}.ipynb') for n, pr, L, l in MEM],
      'Team roster and the notebook each member submits.')
p('')
p('Team problem statement: Develop a multilingual NLP framework that identifies Indian idioms and distinguishes their '
  'literal meaning from culturally intended figurative meaning across Indian languages, while modeling cultural context '
  'and linguistic variation.', italic=True)

# ---------- Abstract ----------
mr, hi, as_ = M['marathi'], M['hindi'], M['assamese']
h1('Abstract')
p('CCA1 built three annotated proverb corpora (545 Marathi, 344 Hindi, 103 Assamese) from public-domain books and showed that '
  'the intended meaning of a proverb is not recoverable from word overlap, that retrieval of that meaning collapses when the '
  'query crosses from English into the source language, and that a multilingual embedding model did not help on romanized '
  'text. CCA3 takes four of the extensions proposed in Plan A and implements all of them on all three corpora, one notebook '
  'per member. Reverse retrieval suggests a proverb for a plain description of a situation; cross-language linking finds '
  'proverbs in the other two corpora with the same intended meaning; an idiom detector is validated on MAGPIE, a corpus of '
  '48,395 real English sentences with figurative/literal labels, and then applied to each language; and a benchmark asks two '
  'open language models (Qwen2.5-0.5B-Instruct and FLAN-T5-base) for the meaning of each proverb and scores the answer '
  'against the compiler\'s explanation, with echo and random-explanation controls. '
  f'Results: reverse retrieval reaches Hit@5 of {mr["reverse_retrieval"]["labse"]["hit_at_5"]}/{hi["reverse_retrieval"]["labse"]["hit_at_5"]}/'
  f'{as_["reverse_retrieval"]["labse"]["hit_at_5"]} (Marathi/Hindi/Assamese, LaBSE) against random baselines near 0.02-0.07; the MAGPIE detector '
  f'scores {mr["magpie"]["acc"]} accuracy against a {mr["magpie"]["majority_acc"]} majority baseline; reciprocal linking yields '
  f'{mr["equivalence_hindi"]["candidates"]} Marathi-Hindi candidate pairs but none between Hindi and Assamese; and in every language the '
  'language models\' margin over a random explanation is smaller than the margin obtained by simply echoing the proverb '
  f'(for example Assamese: Qwen {as_["llm_benchmark"]["Qwen2.5-0.5B-Instruct / literal_en"]["margin"]:+.3f} against echo '
  f'{as_["llm_benchmark"]["echo baseline (literal translation)"]["margin"]:+.3f}), and is close to zero on romanized input.')

# ---------- 2 Keywords ----------
h1('Keywords')
p('Proverbs; figurative language; literal versus intended meaning; cross-lingual retrieval; sentence embeddings; LaBSE; '
  'idiom detection; MAGPIE; language-model evaluation; low-resource Indian languages; Marathi; Hindi; Assamese; '
  'public-domain corpora.')

# ---------- Introduction ----------
h1('1. Introduction')
p('CCA1 ended with three results and one open door. The results: a proverb shares no more vocabulary with its own '
  'explanation than with a random one; retrieval of the intended meaning works within English but drops sharply when the '
  'query is the romanized source text (P@1 0.347 to 0.120 for Assamese, 0.129 to 0.029 for Marathi, 0.081 to 0.024 for '
  'Hindi); and LaBSE, run zero-shot on that romanized text, stayed at the random baseline. The open door was the list of '
  'extensions in Plan A. CCA3 walks through four of them, chosen because they could be built on the CCA1 corpora and '
  'retrieval code without new data collection, and runs each one on all three languages so the results can be compared '
  'across the team.')
p('The four experiments are ordered by difficulty in every notebook. Reverse retrieval (Plan A 2.8) is the CCA1 retrieval '
  'machinery with the query direction swapped. Cross-language equivalence linking (2.4) compares explanations across '
  'corpora. Idiom identification in running text (2.5) needs a corpus of idioms in context, which exists for English and not '
  'for our languages, so the method is validated on the English corpus first. The language-model benchmark (2.7) needs '
  'generation, scoring and controls, and is the most involved. Each notebook saves its numbers to a metrics file; every '
  'figure and number in this report comes from those files.')

# ---------- 4 Survey ----------
h1('2. Literature survey')
h2('2.1 Idioms and figurative language in NLP')
p('The question of whether a potentially idiomatic expression is being used figuratively or literally in a given sentence is '
  'the standard form of the idiom-detection task. Haagsma, Bos and Nissim (2020) released MAGPIE, the largest corpus for it: '
  '56,622 sentences from the British National Corpus containing one of 1,756 idiom types, each annotated for figurative or '
  'literal usage with a sense-level confidence. Tan and Jiang (2021) probed BERT-style encoders on idiom usage and found that '
  'contextual representations carry a usable signal for figurative versus literal reading, while Dankers, Lucas and Titov '
  '(2022) showed that neural translation systems still tend to process idioms compositionally, translating them word by '
  'word. These results frame our Step A and Step B: a supervised detector over real sentences is a well-defined task with '
  'public data, and compositional processing of figurative text is the known failure mode.')
h2('2.2 Multilingual sentence embeddings and cross-lingual retrieval')
p('Reimers and Gurevych (2019) introduced sentence-level embeddings trained so that cosine similarity reflects meaning, which '
  'is the basis of every retrieval and linking step here. Feng et al. (2022) extended this across 109 languages with LaBSE, '
  'trained on translation pairs so that a sentence and its translation map to nearby vectors. For Indian languages, MuRIL '
  '(Khanuja et al., 2021) and the IndicNLPSuite models (Kakwani et al., 2020) are trained on native-script text, and both '
  'papers note the cost of transliteration and code-mixing. CCA1 observed that cost directly: LaBSE on 19th-century romanized '
  'Assamese was at chance. This survey point motivates evaluating both a lexical (TF-IDF) and a semantic (LaBSE) index in '
  'every experiment rather than assuming the semantic one wins.')
h2('2.3 Language models and proverbs')
p('Instruction-tuned models such as FLAN-T5 (Chung et al., 2022) and Qwen2.5 (Qwen Team, 2024) can be asked directly for '
  'the meaning of a text. Recent work has started to test them on proverbs: Liu et al. (2024) built a multilingual proverbs '
  'and sayings benchmark and found that models reason better about proverbs in high-resource languages and about well-known '
  'sayings, which raises the question of memorisation versus understanding. Our benchmark is built with that concern in '
  'mind: the proverbs come from obscure 1890s compilations, and the scoring uses a random-explanation control and an echo '
  'baseline so that fluent restatement is not mistaken for interpretation.')
h2('2.4 Resources for the three languages')
p('The CCA1 corpora remain the only machine-readable proverb collections with literal translation and intended meaning for '
  'Marathi, Hindi and Assamese together (Manwaring, 1899; Fallon, 1886; Gurdon, 1896). No corpus of these proverbs in running '
  'text exists, and no cross-language equivalence resource links them, which is what sections 2.4 and 2.5 of the plan set out '
  'to address.')

# ---------- 5 Research gaps ----------
h1('3. Research gaps')
numbered('Idiom-in-context corpora exist for English (MAGPIE) but not for Marathi, Hindi or Assamese, so detection methods '
         'for these languages cannot be trained or tested on real usage.')
numbered('No resource links proverbs with the same intended meaning across Marathi, Hindi and Assamese; cross-language '
         'proverb work has been done for high-resource pairs only.')
numbered('Retrieval work on proverbs, including CCA1, runs from proverb to meaning; the reverse direction, from a described '
         'situation to a fitting proverb, has not been evaluated on these corpora.')
numbered('Language-model proverb benchmarks are dominated by well-known sayings, so memorisation and interpretation are '
         'confounded; obscure historical proverbs with gold explanations offer a cleaner test.')
numbered('Embedding and generative models expect native script; the behaviour of both on romanized historical text is '
         'documented for retrieval (CCA1) but not for generation.')

# ---------- 6 Objectives ----------
h1('4. Objectives')
numbered('Build a situation-to-proverb retrieval index on each corpus and measure it on hand-written situation queries '
         'against lexical, semantic and random baselines (addresses gap 3).')
numbered('Link proverbs across the three corpora by the meaning of their explanations, with reciprocal matching and a '
         'random-pair reference, and produce a verifiable candidate file (gap 2).')
numbered('Train and validate an idiom-usage detector on real English sentences, then test whether the recipe transfers to '
         'each language\'s proverbs (gap 1).')
numbered('Benchmark two open language models on proverb interpretation under literal-translation and romanized inputs, with '
         'controls that separate interpretation from restatement (gaps 4 and 5).')
numbered('Run all four on all three languages with one code path so the comparison across languages is fair.')

# ---------- 7 Outcomes ----------
h1('5. Outcomes')
bullet('Three executed notebooks (one per member) implementing all four experiments, with a live suggest() interface for '
       'reverse retrieval.')
bullet(f'Reverse retrieval working on all three corpora: Hit@5 of {max(mr["reverse_retrieval"]["tfidf"]["hit_at_5"], mr["reverse_retrieval"]["labse"]["hit_at_5"])}, '
       f'{max(hi["reverse_retrieval"]["tfidf"]["hit_at_5"], hi["reverse_retrieval"]["labse"]["hit_at_5"])} and '
       f'{max(as_["reverse_retrieval"]["tfidf"]["hit_at_5"], as_["reverse_retrieval"]["labse"]["hit_at_5"])} (Marathi, Hindi, Assamese) at best.')
bullet(f'Three cross-language candidate files for manual verification ({mr["equivalence_hindi"]["candidates"]} Marathi-Hindi, '
       f'{mr["equivalence_assamese"]["candidates"]} Marathi-Assamese, {hi["equivalence_assamese"]["candidates"]} Hindi-Assamese pairs after the reciprocal test), '
       'and a documented fix for the boilerplate-matching problem found on the first run.')
bullet(f'An idiom-usage detector validated on real text ({mr["magpie"]["acc"]} accuracy, {mr["magpie"]["macro_f1"]} macro-F1 on the MAGPIE test split) '
       'and shown to transfer to all three languages\' proverbs in carrier sentences.')
bullet('A benchmark result that holds in all three languages: small open language models do not interpret these proverbs '
       'better than repeating them, and gain nothing from romanized input, which extends the CCA1 finding from retrieval to '
       'generation.')
bullet('Per-language metrics files and candidate CSVs, from which every number in this report is taken.')

# ---------- RQs ----------
h1('6. Research questions (one per member)')
for n, pr, L, l in MEM:
    bullet(f'RQ ({n}, {L}): On the {L} corpus, how far do the four extensions carry over from the CCA1 retrieval setting: '
           f'can a situation description retrieve the right proverb, do {L} proverbs have reciprocal meaning matches in the '
           f'other two corpora, does an idiom detector trained on real English sentences transfer to {L} proverbs in carrier '
           f'sentences, and does a small language model add anything beyond restating the proverb?')

# ---------- Contributions ----------
h1('7. Research contributions')
for n, pr, L, l in MEM:
    m = M[l]
    h2(f'7.{MEM.index((n, pr, L, l)) + 1} {n} ({L})')
    p(f'A notebook that implements all four extensions on the {L} corpus: a reverse-retrieval index over the {L} '
      f'explanations with a live suggest() interface and {SIT_N[l]} hand-written situation queries; a reciprocal '
      f'cross-language linking run against the other two corpora, with a candidate file for manual verification; an idiom '
      f'detector trained on 38,716 MAGPIE sentences and applied to {m[f"idiom_in_text_{l}"]["n"]} {L} test sentences; and a '
      f'60-proverb language-model benchmark with echo and random-explanation controls. The member also wrote the situation '
      f'queries for another member\'s language, so no one evaluated their own index on their own queries.')

# ---------- Methodology ----------
h1('8. Methodology')
h2('8.1 Shared design')
p('All three notebooks run the same code with the language as a parameter, so differences between languages are '
  'differences in the data, not in the method. LaBSE embeddings (normalized, cosine similarity) and TF-IDF are the two '
  'representations throughout, as in CCA1.')
bullet('Reverse retrieval (2.8). Index: every explanation in the corpus. Query: a one-sentence situation description '
       'written by a team member who did not build that index, each targeting one proverb; the descriptions avoid copying '
       'words from the explanation. Metrics: Hit@1, Hit@5, MRR for TF-IDF and LaBSE, against the random baseline.')
bullet('Equivalence linking (2.4). Explanations are stripped of compiler boilerplate ("the proverb means", "literally") before '
       'embedding, because a first run showed one generic explanation matching dozens of proverbs on that boilerplate. For '
       'each proverb the best match in each other corpus is found; a pair is a candidate only if it is a mutual best match '
       'and its similarity is at least 0.5. The similarity to a random pairing is the reference distribution. Candidates are '
       'written to a CSV with an empty verified column.')
bullet('Idiom identification in text (2.5). Step A: TF-IDF (word 1-2-grams) plus logistic regression trained on the MAGPIE '
       'training split (38,716 sentences) and tested on its test split (4,840), labels idiomatic versus literal usage. Step B: '
       'the same recipe on the language\'s proverbs placed in six carrier sentences, against real literal MAGPIE sentences in '
       'the same carriers, 5-fold cross-validation. Step B carries a stated register confound.')
bullet('Language-model benchmark (2.7). 60 proverbs with explanations (all 75 for Assamese sampled to 60; random sample for '
       'the others). Two models, Qwen2.5-0.5B-Instruct and FLAN-T5-base, prompted for a one-sentence meaning under two '
       'inputs: the literal translation and the romanized source text. Score: LaBSE similarity of the answer to the gold '
       'explanation; control: similarity to a random other explanation; margin = the difference. Echo baseline: the literal '
       'translation itself scored the same way.')
h2('8.2 Per-member notes')
for n, pr, L, l in MEM:
    m = M[l]
    p(f'{n} ({L}): {SIT_N[l]} situation queries; {m["llm_benchmark_n"]} proverbs in the benchmark; '
      f'{m[f"idiom_in_text_{l}"]["n"]} sentences in the Step B detection set. '
      + ('The Assamese corpus is small enough that the benchmark uses nearly the whole corpus rather than a sample.' if l == 'assamese' else
         'The Fallon glosses are the shortest and noisiest explanations of the three corpora, which matters for linking.' if l == 'hindi' else
         'The Marathi explanations are one sentence each, which keeps the retrieval index compact but gives the embeddings little to work with.'))

# ---------- Data ----------
h1('9. Data')
p('The three CCA1 corpora are reused unchanged (`../cca1/corpus/PanelB_16_<language>_proverbs.csv`): 545 Marathi, 344 Hindi, '
  '103 Assamese proverbs, of which 338, 305 and 75 carry an explanation and form the retrieval indexes. One external '
  'corpus is added for Step A of the idiom detector: MAGPIE (Haagsma, Bos and Nissim, 2020), 48,395 English sentences from the '
  'British National Corpus in which a potentially idiomatic expression occurs, labelled by annotators as idiomatic (36,328) '
  'or literal (12,067), with a fixed training/development/test split. It is public, licensed for research, and stored under '
  '`external/`. The situation queries (28 across the three languages) were written by hand and are listed inside each notebook '
  'with their target proverb ids.')

# ---------- Results ----------
h1('10. Implementation')
p('Each member\'s notebook produces five figures, shown here in the order the experiments were run. Tables give the numbers '
  'behind them.')
for idx, (n, pr, L, l) in enumerate(MEM):
    m = M[l]; rr = m['reverse_retrieval']; q = m['llm_benchmark']
    eq = {k.split('_')[1]: v for k, v in m.items() if k.startswith('equivalence_')}
    h2(f'10.{idx + 1} {n} ({L})')
    # reverse retrieval
    table([('Index', 'Hit@1', 'Hit@5', 'MRR'),
           ('TF-IDF', rr['tfidf']['hit_at_1'], rr['tfidf']['hit_at_5'], rr['tfidf']['mrr']),
           ('LaBSE', rr['labse']['hit_at_1'], rr['labse']['hit_at_5'], rr['labse']['mrr']),
           ('Random', rr['random']['hit_at_1'], rr['random']['hit_at_5'], rr['random']['mrr'])],
          f'{L} reverse retrieval on {SIT_N[l]} situation queries.')
    better = 'LaBSE' if rr['labse']['mrr'] >= rr['tfidf']['mrr'] else 'TF-IDF'
    fig(f'report/figures/{l}/PanelB_16_CCA3_{l}_fig1.png',
        f'{L} reverse retrieval: Hit@1, Hit@5 and MRR for the lexical and semantic index against the random baseline.',
        f'Both indexes find the target proverb in the top five for {max(rr["tfidf"]["hit_at_5"], rr["labse"]["hit_at_5"])*100:.0f} percent of the '
        f'situations at best, against {rr["random"]["hit_at_5"]*100:.1f} percent by chance, so a plain description is enough to reach the '
        f'right proverb most of the time. {better} has the better MRR here ({max(rr["labse"]["mrr"], rr["tfidf"]["mrr"]):.3f}), '
        + ('which is expected when the situation and the explanation share concrete words.' if better == 'TF-IDF' else
           'which means the situations were matched on meaning rather than on shared words, as intended when they were written.'))
    # equivalence
    table([('Other corpus', 'Mean best similarity', 'Mean random similarity', 'Mutual best matches', 'Candidates (>= 0.5)')] +
          [(k.capitalize(), v['mean_best_similarity'], v['mean_random_similarity'], v['mutual_best_matches'], v['candidates']) for k, v in eq.items()],
          f'{L} cross-language equivalence linking.')
    tot = sum(v['candidates'] for v in eq.values())
    fig(f'report/figures/{l}/PanelB_16_CCA3_{l}_fig2.png',
        f'Similarity of each {L} explanation to its best match in the other corpus (blue) against a random pairing (red); the dashed line is the candidate threshold.',
        f'Best matches sit well above random pairings in both corpora (means of {", ".join(f3(v["mean_best_similarity"]) for v in eq.values())} '
        f'against {", ".join(f3(v["mean_random_similarity"]) for v in eq.values())}), but only {tot} pairs clear both the mutual-match test and the '
        'threshold. Meaning overlap across these books is real but rare, and the few candidates are what the manual verification should start from.')
    # magpie
    mg = m['magpie']
    fig(f'report/figures/{l}/PanelB_16_CCA3_{l}_fig3.png',
        'Figurative-versus-literal usage detection on the MAGPIE test split of real English sentences (identical in all three notebooks, since Step A does not depend on the language).',
        f'The detector reaches {mg["acc"]} accuracy and {mg["macro_f1"]} macro-F1 against a {mg["majority_acc"]} majority baseline on real text. '
        'Most errors are literal uses predicted as idiomatic, the direction expected when idiomatic uses outnumber literal ones three to one in training.')
    it = m[f'idiom_in_text_{l}']
    fig(f'report/figures/{l}/PanelB_16_CCA3_{l}_fig4.png',
        f'Detecting {L} proverbs placed in carrier sentences against real literal sentences in the same carriers ({it["n"]} sentences, 5-fold CV).',
        f'Accuracy is {it["acc"]} against 0.5 chance. The number is high partly because 1890s book English and modern BNC English differ in register, '
        'which the notebook states as a confound; the result shows the recipe transfers, and Step A remains the honest measure of detection on real text.')
    # llm
    rows = [('System', 'Similarity to own explanation', 'Similarity to random explanation (control)', 'Margin')]
    for k, v in q.items():
        rows.append((k.replace('-Instruct', ''), v['similarity_to_gold'], v['similarity_to_control'], f'{v["margin"]:+.3f}'))
    table(rows, f'{L} language-model benchmark on {m["llm_benchmark_n"]} proverbs.')
    echo = q['echo baseline (literal translation)']['margin']
    qlit = q['Qwen2.5-0.5B-Instruct / literal_en']['margin']; qrom = q['Qwen2.5-0.5B-Instruct / romanized']['margin']
    fig(f'report/figures/{l}/PanelB_16_CCA3_{l}_fig5.png',
        f'{L} benchmark: mean similarity of each system\'s answer to the compiler\'s explanation (blue) against the control (grey) for both inputs and the echo baseline.',
        f'With the literal translation as input, Qwen\'s margin over the control is {qlit:+.3f}, positive but below the echo baseline\'s {echo:+.3f}: the model '
        f'writes a plausible-sounding meaning that is no closer to the compiler\'s than the proverb itself. With romanized {L} as input the margin is '
        f'{qrom:+.3f}, so the model is guessing from unfamiliar text. FLAN-T5 answers are mostly fragments and score low in absolute terms.')

# ---------- Performance ----------
h1('11. Performance')
h2('11.1 Cross-language comparison')
table([('Metric', 'Marathi', 'Hindi', 'Assamese')] + [
    ('Reverse retrieval Hit@5 (best index)',) + tuple(max(M[l]['reverse_retrieval']['tfidf']['hit_at_5'], M[l]['reverse_retrieval']['labse']['hit_at_5']) for _, _, _, l in MEM),
    ('Reverse retrieval MRR (best index)',) + tuple(max(M[l]['reverse_retrieval']['tfidf']['mrr'], M[l]['reverse_retrieval']['labse']['mrr']) for _, _, _, l in MEM),
    ('Equivalence candidates (total)',) + tuple(sum(v['candidates'] for v in eqd(M[l]).values()) for _, _, _, l in MEM),
    ('Qwen margin, literal input',) + tuple(f"{M[l]['llm_benchmark']['Qwen2.5-0.5B-Instruct / literal_en']['margin']:+.3f}" for _, _, _, l in MEM),
    ('Qwen margin, romanized input',) + tuple(f"{M[l]['llm_benchmark']['Qwen2.5-0.5B-Instruct / romanized']['margin']:+.3f}" for _, _, _, l in MEM),
    ('Echo baseline margin',) + tuple(f"{M[l]['llm_benchmark']['echo baseline (literal translation)']['margin']:+.3f}" for _, _, _, l in MEM),
], 'The four experiments side by side.')
p('Reverse retrieval works in all three languages, with Hindi and Assamese slightly ahead of Marathi because their '
  'explanations are longer and give the index more to match on. Equivalence linking is strongest between Marathi and Hindi, '
  'whose explanations are closest in length and style, and finds nothing between Hindi and Assamese, where the Fallon glosses '
  'are short and OCR-damaged. The benchmark result is uniform: in every language the echo baseline\'s margin is the largest, '
  'Qwen\'s literal-input margin is positive but smaller, and the romanized-input margin is near zero. A small open model given '
  'the literal translation produces fluent meanings that are no closer to the compiler\'s than the proverb text, and given '
  'romanized text it produces nothing useful. That is the CCA1 cross-lingual wall, now observed for a generative model.')
h2('11.2 Limitations')
bullet('The situation query sets are small (8 to 10 per language); the hit rates have wide uncertainty and should be read as '
       'a demonstration, not a benchmark.')
bullet('Equivalence candidates still need the manual verification pass; the similarity ranks them and does not decide them.')
bullet('Step B of the detector is confounded by register, as stated; a real in-context corpus for these languages would remove it.')
bullet('The language models are small (0.5B and 0.25B parameters) and run on CPU; larger models may interpret better, but the '
       'controls would apply to them unchanged. The famous-versus-obscure split proposed in Plan A needs a frequency source '
       'and is left for later.')
bullet('Native-script recovery (Plan A 2.1) remains the precondition for both the embedding and the generative models to '
       'contribute on the source-language text.')


# ---------- Discussion ----------
h1('12. Discussion')
for idx, (n, pr, L, l) in enumerate(MEM):
    m = M[l]; rr = m['reverse_retrieval']; q = m['llm_benchmark']
    eq = {k.split('_')[1]: v for k, v in m.items() if k.startswith('equivalence_')}
    h2(f'12.{idx + 1} {n} ({L})')
    best5 = max(rr['tfidf']['hit_at_5'], rr['labse']['hit_at_5'])
    cands = ', '.join(f'{v["candidates"]} with {k.capitalize()}' for k, v in eq.items())
    echo = q['echo baseline (literal translation)']['margin']; qlit = q['Qwen2.5-0.5B-Instruct / literal_en']['margin']
    body = (f'Reverse retrieval is the clearest success on {L}: with {SIT_N[l]} situations written by another member, the target proverb is in the '
            f'top five for {best5*100:.0f} percent of them, which makes the suggest() demo usable as it stands. Equivalence linking produced '
            f'{cands} candidate pairs after the reciprocal test; the drop from best-match similarity to candidate count shows how much of the '
            'raw similarity was shared wording rather than shared meaning, and the verification file is the next step. ')
    if l == 'hindi':
        body += ('The zero Hindi-Assamese count is the Fallon glosses again: they are short, often a single clause, and OCR-damaged, so the '
                 'embeddings have too little to match on. ')
    if l == 'assamese':
        body += ('The Assamese explanations are long ethnographic notes, and the matches they attract are often on secondary content '
                 '(a place, an object) rather than the proverb\'s point, which is why the threshold and the mutual test were needed. ')
    if l == 'marathi':
        body += ('Marathi links best with Hindi, the two corpora whose explanations are closest in length and style. ')
    body += (f'The idiom detector transfers from MAGPIE to the {L} proverbs with the register caveat. The benchmark result is the one to carry '
             f'forward: a small instruction-tuned model, given the literal translation, scores a margin of {qlit:+.3f} over a random explanation '
             f'while the echo baseline scores {echo:+.3f}, so the model adds nothing the proverb text did not already contain, and on romanized '
             f'{L} it adds nothing at all. This is the CCA1 cross-lingual wall observed for a generative model instead of a retrieval one.')
    p(body)

# ---------- Conclusion ----------
h1('13. Conclusion')
p('Four Plan A extensions were implemented on all three corpora with one shared code path. Two worked as intended: reverse '
  'retrieval turns the CCA1 index into a usable situation-to-proverb tool, and the idiom detector, validated on 48,395 real '
  'English sentences, transfers to the proverbs. One produced a modest, honest yield: reciprocal cross-language linking finds '
  f'{mr["equivalence_hindi"]["candidates"]} Marathi-Hindi pairs, {mr["equivalence_assamese"]["candidates"]} Marathi-Assamese pairs and no Hindi-Assamese pairs '
  'that pass both tests, and it took a boilerplate-stripping and mutual-match fix to get even that far, because raw similarity '
  'was matching the compilers\' phrasing. One is a clear negative result with the same shape as CCA1: two small open language '
  'models do not interpret the proverbs better than repeating them, and the romanized source text gives them nothing, in every '
  'language. The practical conclusion for the team framework is unchanged from CCA1 and now rests on more evidence: native-script '
  'recovery (Plan A 2.1) is the precondition for the multilingual and generative models to contribute, and the famous-versus-obscure '
  'split of the benchmark should be run once a frequency source for well-known proverbs is available.')

# ---------- Submitted files ----------
h1('14. Submitted files')
p('Report: PanelB_16_CCA3_Report.docx (this document).')
p('Code: PanelB_16_CCA3_marathi.ipynb (Sahish Nagulwar), PanelB_16_CCA3_hindi.ipynb (Ibrahim Ansari), '
  'PanelB_16_CCA3_assamese.ipynb (Chayan Raj Bharati), all executed with outputs. The CCA1 corpora and extraction scripts are '
  'reused from the CCA1 submission.')
p('Data: the three CCA1 corpus CSVs (reused); external/MAGPIE_filtered_split_random.jsonl (48,395 rows, public, with its '
  'licence file); the situation query sets inside each notebook.')
p('Generated files: report/PanelB_16_CCA3_<language>_metrics.json (all numbers in this report), '
  'report/PanelB_16_CCA3_<language>_equivalence_candidates.csv (candidate pairs with an empty verified column for manual '
  'checking), and the figure images under report/figures/.')
p('Earlier documents: PanelB_16_CCA2_PlanA.docx and PanelB_16_CCA2_PlanB.docx, the plans this work follows.')

# ---------- References ----------
h1('References')
for ref in [
    'Chung, H. W., Hou, L., Longpre, S., et al. (2022). Scaling instruction-finetuned language models. arXiv:2210.11416.',
    'Dankers, V., Lucas, C., & Titov, I. (2022). Can transformer be too compositional? Analysing idiom processing in neural machine translation. Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics, 3608-3626.',
    'Fallon, S. W. (1886). A dictionary of Hindustani proverbs. Banaras: Medical Hall Press. https://archive.org/details/in.ernet.dli.2015.42145',
    'Feng, F., Yang, Y., Cer, D., Arivazhagan, N., & Wang, W. (2022). Language-agnostic BERT sentence embedding. Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics, 878-891.',
    'Gurdon, P. R. (1896). Some Assamese proverbs. Shillong: Assam Secretariat Printing Office. https://archive.org/details/someassameseprov00gurdrich',
    'Haagsma, H., Bos, J., & Nissim, M. (2020). MAGPIE: A large corpus of potentially idiomatic expressions. Proceedings of the 12th Language Resources and Evaluation Conference, 279-287.',
    'Kakwani, D., Kunchukuttan, A., Golla, S., et al. (2020). IndicNLPSuite: Monolingual corpora, evaluation benchmarks and pre-trained multilingual language models for Indian languages. Findings of EMNLP 2020, 4948-4961.',
    'Khanuja, S., Bansal, D., Mehtani, S., et al. (2021). MuRIL: Multilingual representations for Indian languages. arXiv:2103.10730.',
    'Liu, C. C., Koto, F., Baldwin, T., & Gurevych, I. (2024). Are multilingual LLMs culturally-diverse reasoners? An investigation into multicultural proverbs and sayings. Proceedings of NAACL 2024.',
    'Manwaring, A. (1899). Marathi proverbs. Oxford: Clarendon Press. https://archive.org/details/marathiproverbs00manwgoog',
    'Qwen Team (2024). Qwen2.5 technical report. arXiv:2412.15115.',
    'Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using Siamese BERT-networks. Proceedings of EMNLP-IJCNLP 2019, 3982-3992.',
    'Tan, M., & Jiang, J. (2021). Does BERT understand idioms? A probing-based empirical study of BERT encodings of idioms. Proceedings of RANLP 2021, 1397-1407.',
]:
    doc.add_paragraph(ref)

doc.save('report/PanelB_16_CCA3_Report.docx')
print('report written:', fignum, 'figures,', tabnum, 'tables')
