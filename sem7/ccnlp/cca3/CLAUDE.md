# CCA3 / LCA3 — Indian proverb corpora, follow-up experiments and chatbot

Course: Cloud Computing & Natural Language Processing, MIT-WPU, sem 7 (2026).
Panel B, Team 16. All submitted files are prefixed `PanelB_16_`.

| Member | PRN | CCA1 language | CCA3 part |
|---|---|---|---|
| Sahish Nagulwar | 1032233310 | Marathi | Part I, reverse retrieval |
| Ibrahim Ansari (repo owner, corresponding author) | 1032233145 | Hindi | Part II, idiom detection |
| Chayan Raj Bharati | 1032233134 | Assamese | Part III, language-model benchmark |

The reports refer to the parts as Part I/II/III, never by name (professor's
request). The team table in the report holds only names and PRNs.

## What happened, in order

1. **CCA1** (`../cca1/`): three proverb corpora extracted from public-domain
   books on the Internet Archive (Manwaring 1899 Marathi, Fallon 1886 Hindi,
   Gurdon 1896 Assamese). Each row: romanized proverb, literal English
   translation, compiler's recorded meaning, theme, one of six shared
   categories. Sizes 545 / 344 / 103 proverbs, of which 338 / 305 / 75 have a
   meaning. Finding: meaning cannot be read off the words, and LaBSE gives
   nothing on romanized text.
2. **CCA2 plans** (`PanelB_16_CCA2_PlanA.docx`, `PlanB.docx`): extension ideas.
   This folder was originally named cca2 and renamed to cca3.
3. **CCA3 round one** (`PanelB_16_CCA3_{marathi,hindi,assamese}.ipynb`,
   `report/PanelB_16_CCA3_Report.docx`): one notebook per language covering
   four ideas including cross-language equivalence linking. Keep these; the
   user asked that they are not deleted even though the report moved on.
4. **CCA3 v2** (`PanelB_16_CCA3_v2_*.ipynb`, `report/PanelB_16_CCA3_Report_v2.docx`):
   three ideas kept, one notebook per idea, each run on all three corpora.
   Equivalence linking dropped (too few pairs to evaluate). The v2 report
   follows the professor's sample report (`128-CCA1.pdf`, not committed).
   `report/PanelB_16_CCA3_contribution_*.docx` are per-member extracts.
5. **Chatbot** (`PanelB_16_CCA3_chatbot.py`): terminal chatbot joining the
   three parts. Commands: plain text = situation → proverbs; `figurative: ...`
   = two-class detector; `scan: ...` = three-class spotter over a paragraph;
   `explain: ...` or "what does ... mean" = corpus lookup plus Qwen answer;
   `/lang`, `/llm on|off`. Run from this folder with the cca1 venv.
6. **V3** (`v3/`): the LCA3 mini-project report in regular format and on the
   Elsevier Data in Brief template (`data-in-brief-article-template.docx`).
   The regular LCA3 report is the v2 report with names replaced by Part
   labels, screenshots replaced by real tables, captions above tables,
   inference lines under every table and figure, and passages flagged by
   Turnitin's AI detector rewritten. The data article lists only data files
   (corpus CSV/XLSX, raw OCR text, source PDFs, MAGPIE, situation queries),
   no results tables. A chatbot-specific report pair was made and then
   deleted at the user's request.

## Experiments and the numbers to remember

- Part I, reverse retrieval: TF-IDF and LaBSE indexes over the recorded
  meanings; 28 hand-written situation queries (10 Marathi, 8 Hindi, 10
  Assamese; `report/PanelB_16_CCA3_v2_situation_queries.csv`). LaBSE Hit@5
  0.5 / 0.75 / 0.7; MRR 0.518 / 0.68 / 0.429. TF-IDF wins for Assamese.
- Part II, idiom detection: Step A trains TF-IDF (1-2 grams) + logistic
  regression on MAGPIE (48,395 BNC sentences, 36,328 idiomatic / 12,067
  literal; split 38,716 / 4,839 / 4,840): 0.862 accuracy, 0.827 macro-F1 vs
  0.746 majority. Step B puts proverb translations and real literal MAGPIE
  sentences in the same six carrier templates (5-fold CV): 0.943 / 0.933 /
  0.913 on 2,180 / 1,376 / 412 sentences. Step B is inflated by the register
  gap (1890s English vs BNC); quote Step A.
- Part III, language-model benchmark: Qwen2.5-0.5B-Instruct and FLAN-T5-base,
  60 proverbs per language, literal_en vs romanized input, LaBSE similarity
  to the gold meaning minus similarity to a random meaning. The echo baseline
  (the proverb's own translation) beats every model in every language;
  romanized input gives margins near zero.

All numbers in the reports come from `report/PanelB_16_CCA3_v2_*_metrics.json`
and `report/PanelB_16_CCA3_v2_cases.json`; never type them by hand.

## Regenerating things

Run everything from this folder with the CCA1 venv:
`../cca1/.venv/bin/python scripts/<script>.py`. The venv has pandas,
scikit-learn, matplotlib, seaborn, nbformat, nbclient, sentence-transformers,
torch (CPU), transformers, python-docx, openpyxl. Models in the HF cache:
LaBSE (1.8 GB), Qwen2.5-0.5B-Instruct, flan-t5-base. MAGPIE lives in
`external/MAGPIE_filtered_split_random.jsonl` (gitignored, 47 MB; re-download
from https://github.com/hslh/magpie-corpus).

| Script | Produces |
|---|---|
| `scripts/make_cca3.py` | round-one per-language notebooks |
| `scripts/make_cca3_report.py` | `report/PanelB_16_CCA3_Report.docx` (v1) |
| `scripts/make_cca3_v2.py` | the three v2 notebooks (holds the SITUATIONS query dict); execute them with nbclient afterwards |
| `scripts/make_extras.py` | methodology diagram, screenshot PNGs, `cases.json` (runs the models; skips if cases.json exists) |
| `scripts/make_sample_rows.py` | `sample_rows.json` (rows for the tables) and the situation-queries CSV |
| `scripts/make_cca3_report_v2.py` | `report/PanelB_16_CCA3_Report_v2.docx` (older style: names, screenshots; kept as submitted) |
| `scripts/make_regular_lca3.py` | `v3/PanelB_16_LCA3_MiniProject_Report.docx` (current style) |
| `scripts/make_dib.py` | `v3/PanelB_16_LCA3_MiniProject_DataArticle.docx` |
| `scripts/make_contribs.py` | the three contribution docx, extracted from the LCA3 report by Part label |

Order when something upstream changes: notebooks → make_extras →
make_sample_rows → make_regular_lca3 → make_contribs → make_dib. PDFs are
made with `soffice --headless --convert-to pdf`; check page counts with
`pdfinfo` (regular report must stay at 20 pages or under; shrink figure widths
rather than cut content).

## Conventions the user has asked for

- Plain writing, no AI tells: no em dashes in prose, no "robust / pivotal /
  showcase / delve", no neat three-item parallel lists in every sentence.
  Turnitin flagged uniform rhythm; vary sentence length, use "we".
- Do not modify project files unless asked; the user demos from this folder.
- Keep the round-one notebooks and the v1/v2 reports; add new versions
  alongside instead of overwriting.
- Group is 16 (an early draft said 18). No DOI for the data article.
- Inference lines ("Inference: ...") under every figure and table, two or
  three lines each. Captions go above tables, below figures.
