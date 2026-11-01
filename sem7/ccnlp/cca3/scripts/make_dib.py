"""Build the LCA3 mini-project data article on the Elsevier Data in Brief
template, keeping the template's own styles and section order."""
import copy, json, sys
from docx import Document
from docx.shared import Pt, Inches
from docx.oxml.ns import qn

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

import os
CCA3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CCA1 = os.path.join(os.path.dirname(CCA3), 'cca1')
TEMPLATE = f'{CCA3}/v3/data-in-brief-article-template.docx'
R = json.load(open(f'{CCA3}/report/PanelB_16_CCA3_v2_reverse_retrieval_metrics.json'))
I = json.load(open(f'{CCA3}/report/PanelB_16_CCA3_v2_idiom_detection_metrics.json'))
Q = json.load(open(f'{CCA3}/report/PanelB_16_CCA3_v2_llm_benchmark_metrics.json'))
rs = R['summary']; mg = I['magpie']; qb = Q['benchmark']
SR = json.load(open(f'{CCA3}/report/PanelB_16_CCA3_v2_sample_rows.json'))
LANGS = ['Marathi', 'Hindi', 'Assamese']

AUTHORS = 'Sahish Nagulwar, Ibrahim Ansari*, Chayan Raj Bharati'
AFFIL = ('School of Computer Science and Engineering, Dr. Vishwanath Karad MIT World Peace University, '
         'Survey No. 124, Paud Road, Kothrud, Pune 411038, Maharashtra, India')
EMAIL = 'ibrahim.ansari@mitwpu.edu.in (corresponding author); sahish.nagulwar@mitwpu.edu.in; chayan.bharati@mitwpu.edu.in'

REFS = [
    'A. Manwaring, Marathi Proverbs, Clarendon Press, Oxford, 1899. https://archive.org/details/marathiproverbs00manwgoog',
    'S.W. Fallon, A Dictionary of Hindustani Proverbs, Medical Hall Press, Banaras, 1886. https://archive.org/details/in.ernet.dli.2015.42145',
    'P.R. Gurdon, Some Assamese Proverbs, Assam Secretariat Printing Office, Shillong, 1896. https://archive.org/details/someassameseprov00gurdrich',
    'H. Haagsma, J. Bos, M. Nissim, MAGPIE: A large corpus of potentially idiomatic expressions, in: Proceedings of the 12th Language Resources and Evaluation Conference, 2020, pp. 279-287. https://github.com/hslh/magpie-corpus',
    'F. Feng, Y. Yang, D. Cer, N. Arivazhagan, W. Wang, Language-agnostic BERT sentence embedding, in: Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics, 2022, pp. 878-891.',
    'N. Reimers, I. Gurevych, Sentence-BERT: Sentence embeddings using Siamese BERT-networks, in: Proceedings of EMNLP-IJCNLP, 2019, pp. 3982-3992.',
    'H.W. Chung, L. Hou, S. Longpre, et al., Scaling instruction-finetuned language models, arXiv:2210.11416, 2022.',
    'Qwen Team, Qwen2.5 technical report, arXiv:2412.15115, 2024.',
    'M. Tan, J. Jiang, Does BERT understand idioms? A probing-based empirical study of BERT encodings of idioms, in: Proceedings of RANLP, 2021, pp. 1397-1407.',
    'V. Dankers, C. Lucas, I. Titov, Can transformer be too compositional? Analysing idiom processing in neural machine translation, in: Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics, 2022, pp. 3608-3626.',
    'C.C. Liu, F. Koto, T. Baldwin, I. Gurevych, Are multilingual LLMs culturally-diverse reasoners? An investigation into multicultural proverbs and sayings, in: Proceedings of NAACL, 2024.',
    'S. Khanuja, D. Bansal, S. Mehtani, et al., MuRIL: Multilingual representations for Indian languages, arXiv:2103.10730, 2021.',
    'D. Kakwani, A. Kunchukuttan, S. Golla, et al., IndicNLPSuite: Monolingual corpora, evaluation benchmarks and pre-trained multilingual language models for Indian languages, in: Findings of EMNLP, 2020, pp. 4948-4961.',
    'F. Pedregosa, G. Varoquaux, A. Gramfort, et al., Scikit-learn: Machine learning in Python, Journal of Machine Learning Research 12 (2011) 2825-2830.',
]


class Filler:
    def __init__(self):
        self.doc = Document(TEMPLATE)
        self._strip_comments()
        self.body = self.doc.element.body
        # a bullet paragraph's properties, cloned from the template's own bullet list
        bullet_src = next(p for p in self.doc.paragraphs if p.text.startswith('Why are these data valuable'))
        self.bullet_pPr = copy.deepcopy(bullet_src._p.pPr)
        self._delete_instruction_page()
        for p in self.doc.paragraphs:
            if p.style.name == 'Heading 1' and p.text.startswith('SPECIFICATIONS TABLE'):
                self.set_text(p, 'SPECIFICATIONS TABLE')

    # ----- template cleanup -----
    def _strip_comments(self):
        for tag in ('commentRangeStart', 'commentRangeEnd'):
            for el in self.doc.element.body.findall('.//' + qn('w:' + tag)):
                el.getparent().remove(el)
        for el in self.doc.element.body.findall('.//' + qn('w:commentReference')):
            run = el.getparent(); run.getparent().remove(run)
        part = self.doc.part
        for rid, rel in list(part.rels.items()):
            if 'comments' in rel.reltype:
                del part.rels[rid]

    def _delete_instruction_page(self):
        first = next(p for p in self.doc.paragraphs if p.style.name == 'Heading 1' and p.text.strip() == 'ARTICLE INFORMATION')
        for child in list(self.body):
            if child is first._p:
                break
            if child.tag == qn('w:sectPr'):
                continue
            self.body.remove(child)

    # ----- helpers -----
    def heading(self, text):
        return next(p for p in self.doc.paragraphs if p.style.name == 'Heading 1' and p.text.strip() == text)

    def next_heading(self, h):
        found = False
        for p in self.doc.paragraphs:
            if p._p is h._p:
                found = True; continue
            if found and p.style.name == 'Heading 1':
                return p
        return None

    def clear_between(self, h, keep_labels=()):
        nxt = self.next_heading(h)
        el = h._p.getnext()
        while el is not None and (nxt is None or el is not nxt._p):
            n = el.getnext()
            if el.tag == qn('w:p'):
                txt = ''.join(t.text or '' for t in el.findall('.//' + qn('w:t'))).strip()
                if txt not in keep_labels:
                    self.body.remove(el)
            elif el.tag != qn('w:tbl') and el.tag != qn('w:sectPr'):
                self.body.remove(el)
            el = n

    def set_text(self, p, text, bold=False, italic=False, size=None):
        for r in list(p.runs):
            r._r.getparent().remove(r._r)
        r = p.add_run(text); r.bold = bold; r.italic = italic
        if size: r.font.size = Pt(size)
        return p

    def para_before(self, anchor, text, bold=False, italic=False, size=None, bullet=False):
        p = anchor.insert_paragraph_before('') if anchor is not None else self.doc.add_paragraph('')
        if bullet:
            if p._p.pPr is not None:
                p._p.remove(p._p.pPr)
            p._p.insert(0, copy.deepcopy(self.bullet_pPr))
        self.set_text(p, text, bold, italic, size)
        return p

    def inference_before(self, anchor, text):
        p = self.para_before(anchor, '')
        r = p.add_run('Inference: '); r.bold = True
        p.add_run(text)

    def figure_before(self, anchor, path, caption, width=5.0, inf=None):
        p = self.para_before(anchor, '')
        p.alignment = 1
        p.add_run().add_picture(path, width=Inches(width))
        c = self.para_before(anchor, caption, italic=True, size=9)
        c.alignment = 1
        if inf: self.inference_before(anchor, inf)

    def table_before(self, anchor, rows, caption, inf=None, size=9):
        cap = self.para_before(anchor, caption, italic=True, size=9)
        cap.alignment = 1
        t = self.doc.add_table(rows=len(rows), cols=len(rows[0]))
        t.style = self.doc.tables[0].style
        from docx.oxml import OxmlElement
        tblPr = t._tbl.tblPr
        borders = OxmlElement('w:tblBorders')
        for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
            e = OxmlElement(f'w:{edge}'); e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), '4'); e.set(qn('w:color'), '808080'); borders.append(e)
        tblPr.append(borders)
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                c = t.rows[i].cells[j]; c.text = str(cell)
                for pp in c.paragraphs:
                    for r in pp.runs:
                        r.font.size = Pt(size); r.bold = (i == 0)
        _merge_repeats(t, rows)
        if anchor is not None:
            anchor._p.addprevious(t._tbl)
        if inf: self.inference_before(anchor, inf)
        else: self.para_before(anchor, '')

    def fill_label(self, label, text):
        ps = self.doc.paragraphs
        i = next(k for k, p in enumerate(ps) if p.text.strip() == label)
        self.set_text(ps[i + 1], text)

    def fill_spec(self, row_label, text):
        t = self.doc.tables[0]
        for r in t.rows:
            if r.cells[0].text.strip().startswith(row_label):
                tcs = r._tr.findall('.//' + qn('w:tc'))
                if len(r.cells) == 1 and len(tcs) >= 2:
                    from docx.table import _Cell
                    right = _Cell(tcs[-1], t)
                    ps = tcs[-1].findall('.//' + qn('w:p'))
                    for extra in ps[1:]:
                        extra.getparent().remove(extra)
                    from docx.text.paragraph import Paragraph
                    self.set_text(Paragraph(ps[0], right), text)
                    return
                if len(r.cells) == 1:
                    cell = r.cells[0]
                    for extra in cell.paragraphs[1:]:
                        extra._p.getparent().remove(extra._p)
                    cell.add_paragraph(text)
                    return
                cell = r.cells[1]
                self.set_text(cell.paragraphs[0], text)
                for extra in cell.paragraphs[1:]:
                    extra._p.getparent().remove(extra._p)

    def fill_section(self, title, blocks):
        """blocks: list of ('p', text) | ('b', text) | ('fig', path, caption, width, inf) | ('tbl', rows, caption, inf, size)"""
        h = self.heading(title)
        self.clear_between(h)
        nxt = self.next_heading(h)
        for b in blocks:
            if b[0] == 'p': self.para_before(nxt, b[1])
            elif b[0] == 'b': self.para_before(nxt, b[1], bullet=True)
            elif b[0] == 'fig': self.figure_before(nxt, b[1], b[2], b[3] if len(b) > 3 else 5.0, b[4] if len(b) > 4 else None)
            elif b[0] == 'tbl': self.table_before(nxt, b[1], b[2], b[3] if len(b) > 3 else None, b[4] if len(b) > 4 else 9)


def common_specs(F, kind):
    F.fill_spec('Subject', 'Computer Science: Artificial Intelligence; Arts and Humanities: Linguistics')
    F.fill_spec('Specific subject area', 'Natural language processing of figurative language: proverb and idiom corpora for Marathi, Hindi and Assamese, with retrieval, detection and language-model interpretation outputs.')
    F.fill_spec('Type of data', 'Table (CSV, XLSX). Raw and processed data.')
    F.fill_spec('Data collection',
        'Three public-domain proverb compilations (1886-1899) were downloaded as OCR text from the Internet Archive and segmented into entries. Blocks inside each entry were '
        'labelled as romanized proverb, literal English translation or recorded meaning by the share of common English function words, cleaned of OCR noise, and kept only if the '
        'proverb and translation were recoverable. Theme labels were taken from the books\' section headings and mapped to six shared categories. The MAGPIE corpus of English '
        'idiom usage was obtained from its public repository. Situation queries were written by hand by team members. Model outputs were produced on CPU with scikit-learn, '
        'LaBSE sentence embeddings, Qwen2.5-0.5B-Instruct and FLAN-T5-base.')
    F.fill_spec('Data source location',
        'Institution: Dr. Vishwanath Karad MIT World Peace University, Pune, Maharashtra, India. Primary sources: Internet Archive digitizations of Manwaring (1899), Fallon (1886) '
        'and Gurdon (1896) [1-3]; MAGPIE corpus, University of Groningen [4].')
    F.fill_spec('Data accessibility',
        'The data are supplied with the course submission (Google Classroom, Panel B, Team 16) in the folders listed under Data Description; they are not deposited in a public repository, in line with the course confidentiality requirement. '
        'Direct URLs to the primary sources: https://archive.org/details/marathiproverbs00manwgoog ; https://archive.org/details/in.ernet.dli.2015.42145 ; '
        'https://archive.org/details/someassameseprov00gurdrich ; MAGPIE: https://github.com/hslh/magpie-corpus (redistributed under its research licence, which is included).')
    F.fill_spec('Related research article', 'None. The data support the team\'s course reports CCA1 and CCA3 (Cloud Computing and Natural Language Processing, 2026), which are not published articles.')


def build(kind):
    F = Filler()
    doc = F.doc
    top = F.heading('ARTICLE INFORMATION')
    F.para_before(top, ('LCA3 mini project' if kind == 'lca3' else 'CCA3 chatbot') + ' — Cloud Computing & Natural Language Processing, Panel B, Team 16 (data article format, version 3)', bold=True)

    # ---------- article information ----------
    if kind == 'lca3':
        F.fill_label('Article title', 'Dataset of Marathi, Hindi and Assamese proverbs with literal translations and recorded meanings, with the situation queries and idiom-usage data of a mini project on figurative meaning')
    else:
        F.fill_label('Article title', 'Data and session records behind a terminal chatbot for Indian proverbs: retrieval indexes, idiom-detection training data and language-model interpretations')
    F.fill_label('Authors', AUTHORS)
    F.fill_label('Affiliations', AFFIL)
    F.fill_label('Corresponding author’s email address and Twitter handle', EMAIL)
    F.fill_label('Keywords', 'proverbs; figurative meaning; idiom detection; cross-lingual retrieval; sentence embeddings; low-resource languages; OCR corpora' + ('' if kind == 'lca3' else '; conversational interface'))
    abstract_common = (
        'The data describe three machine-readable proverb corpora built from public-domain compilations: 545 Marathi proverbs from Manwaring (1899), 344 Hindi proverbs from '
        'Fallon (1886) and 103 Assamese proverbs from Gurdon (1896). Each record holds the proverb as romanized in the book, its literal English translation, the compiler\'s '
        'explanation of the intended meaning, the book\'s own theme label and one of six shared categories. The corpora were extracted from Internet Archive OCR text with a '
        'rule-based pipeline that labels blocks by their share of English function words, cleans OCR noise and keeps only entries with a recoverable proverb and translation; the '
        'raw OCR text and the extraction scripts are included so every row can be traced back to a line of the source. ')
    if kind == 'lca3':
        abstract = abstract_common + (
            'Alongside the corpora, the dataset holds the data used by the mini project built on them: 28 hand-written situation queries with their target proverbs, '
            'for situation-to-proverb retrieval with TF-IDF and LaBSE indexes, and the MAGPIE corpus of 48,395 English sentences with idiomatic or literal usage labels, on which '
            'an idiom-usage detector was trained before being applied to the proverbs. The corpora can be reused for figurative-language research in three '
            'under-resourced Indian languages, for cross-lingual meaning alignment, and as a test of whether language models interpret obscure proverbs or merely restate them.')
    else:
        abstract = abstract_common + (
            'The dataset is organised around the terminal chatbot that uses these corpora. It holds the retrieval indexes the chatbot builds at start-up (LaBSE and TF-IDF '
            'vectors over 718 recorded meanings), the 28 situation queries used to test the suggest function, the MAGPIE-derived training data of the two idiom-usage detectors '
            '(a two-class detector reported in the course work and a three-class spotter with a plain-sentence class for running text), the 24-proverb sample on which the '
            'interpretation function was checked, success and failure case records for each function, and complete session transcripts of scripted conversations. The chatbot '
            'script itself is included. The data can be reused to rebuild or extend the chatbot, to compare conversational access to proverb meaning across the three '
            'languages, and to study where retrieval, detection and generation fail on historical romanized text.')
    F.fill_label('Abstract', abstract)
    common_specs(F, kind)

    # ---------- value of the data ----------
    value = [
        ('b', 'They are the only machine-readable proverb collections for Marathi, Hindi and Assamese together that pair each proverb with its literal translation and its intended meaning, written by the original compilers; nothing comparable exists for these three languages in one schema.'),
        ('b', 'Researchers in figurative-language processing, cross-lingual semantics and low-resource Indian-language NLP can reuse the corpora directly as supervision: the recorded meaning is a gold explanation, which is rare for proverbs.'),
        ('b', 'The proverbs come from obscure nineteenth-century books, so they are unlikely to be in language-model training data; the benchmark material lets others test interpretation rather than memorisation.'),
        ('b', 'The raw OCR text and the extraction scripts make every row traceable, so the corpora can be corrected and extended (native-script recovery, modern dictionaries) by anyone.'),
    ]
    F.fill_section('VALUE OF THE DATA', value)

    # ---------- background ----------
    bg = [
        ('p', 'A proverb says one thing and means another: "perpetual crops, perpetual poverty" is not about farming but about a farmer who stays poor because he keeps borrowing. '
              'Systems that read text compositionally get the words right and the meaning wrong, and the problem is sharper in Indian languages, where the stock of proverbs is large, '
              'regionally varied and thinly digitised. The team problem statement for the course asked for a multilingual framework that identifies Indian idioms and separates their '
              'literal meaning from the culturally intended one. The first project (CCA1) built the three corpora from colonial-era compilations that record the intended meaning next to '
              'the literal text [1-3], and measured that a proverb shares no more vocabulary with its own explanation than with a random one, that retrieval of the meaning collapses when '
              'the query is the romanized source text, and that a multilingual embedding model [5] gave nothing on that romanized text.'),
    ]
    if True:
        bg.append(('p', 'The mini project (LCA3) extended that work with three experiments run on all three corpora with one shared code path: situation-to-proverb retrieval, idiom-usage detection '
                        'validated on a real English corpus [4] and transferred to the proverbs, and a language-model interpretation benchmark with controls that separate interpretation from '
                        'restatement [7,8,11]. This article describes the corpora and the query and training data those experiments used.'))
    F.fill_section('BACKGROUND', bg)

    # ---------- data description ----------
    corpus_rows = [('Language (source)', 'Proverbs', 'With recorded meaning', 'Mean tokens: proverb / translation / meaning', 'Theme labels'),
                   ('Marathi (Manwaring 1899)', 545, 338, '4.9 / 21.9 / 10.2', '13 book sections'),
                   ('Hindi (Fallon 1886)', 344, 305, '6.7 / 10.0 / 11.4', 'none (alphabetical dictionary)'),
                   ('Assamese (Gurdon 1896)', 103, 75, '9.2 / 26.7 / 36.7', '10 theme buckets from subject headings')]
    files_common = [
        ('cca1/corpus/PanelB_16_<lang>_proverbs.csv', 'One row per proverb: id, theme, theme_bucket, proverb_translit, literal_en, commentary (three files).'),
        ('cca1/corpus/PanelB_16_<lang>_categorised.csv', 'The same rows with the shared six-way category and the basis for it.'),
        ('cca1/corpus/PanelB_16_<lang>_corpus.xlsx', 'Excel workbook per language: cleaned corpus, counts by category, and the full raw OCR text as a sheet.'),
        ('cca1/corpus/PanelB_16_<lang>_*_raw.txt', 'Unedited OCR text of each book as downloaded (395 KB, 1.5 MB, 179 KB).'),
        ('cca1/corpus/source_pdfs/', 'The three scanned books (PDF, 44 MB in total).'),
        ('cca1/PanelB_16_extract_marathi.py, _extract_hindi.py, _build_corpus.py, _categorize.py', 'Extraction and categorisation scripts; raw text in, CSV out.'),
        ('cca3/external/MAGPIE_filtered_split_random.jsonl (+ licence)', '48,395 English sentences with idiomatic/literal usage labels and a fixed split [4]; obtained from its public repository.'),
    ]
    if kind == 'lca3':
        files = files_common + [
            ('cca3/report/PanelB_16_CCA3_v2_situation_queries.csv', 'The 28 hand-written situation queries (10 Marathi, 8 Hindi, 10 Assamese) with the id, romanized text and literal translation of the target proverb.'),
        ]
    else:
        files = files_common + [
            ('cca3/PanelB_16_CCA3_chatbot.py', 'The chatbot: builds the indexes and detectors at start-up, routes messages, loads the language model on first use.'),
            ('cca3/PanelB_16_CCA3_v2_*.ipynb', 'The three notebooks whose functions the chatbot wraps (suggest, is_figurative, explain).'),
            ('cca3/report/PanelB_16_CCA3_v2_cases.json', 'Success and failure records for each function: query ranks, detector predictions, model answers with margins.'),
            ('cca3/report/figures/chatbot_transcript.png', 'Rendered transcript of a scripted session covering all three functions.'),
            ('cca3/report/PanelB_16_CCA3_v2_*_metrics.json', 'Metrics of the three back-end functions as evaluated in the notebooks.'),
        ]
    dd = [
        ('p', 'The dataset is organised in two folders of the course repository, cca1 (corpora and extraction code) and cca3 (the situation queries and the MAGPIE corpus used in the experiments). Table 1 summarises the three corpora and Table 2 lists every data file.'),
        ('tbl', corpus_rows, 'Table 1. The three proverb corpora.',
         'The three corpora differ by an order of magnitude in size and in how long the recorded meaning is: Marathi meanings are one sentence, Assamese commentaries run to several, which affects how much text a retrieval index has to match against.'),
        ('tbl', [('File or folder', 'Content')] + files, 'Table 2. Data files in the dataset (<lang> stands for marathi, hindi or assamese).',
         'Every processed file can be traced back to a raw OCR file and a scanned page through the extraction scripts, so a doubtful row can be checked against the book.'),
        ('p', 'Each corpus row carries six fields. Tables 3 to 5 show sample rows from each corpus file as they appear in the CSV, Figure 1 shows the shared category distribution, Table 6 shows rows of the MAGPIE file, and Table 7 places proverb records next to MAGPIE idiom records to make the two record types concrete.'),
    ] + [
        ('tbl', [('id', 'Romanized proverb', 'Literal translation', 'Recorded meaning')] + [tuple(r) for r in SR['corpus'][L]], f'Table {3 + i}. {L} corpus file, sample rows.',
         {'Marathi': 'The recorded meaning is a single sentence and the translation is often longer than it, so the Marathi index has the least text to match a situation against.',
          'Hindi': 'Fallon writes short literal glosses and a meaning of similar length; the romanized line is the longest field, and it is the one multilingual models cannot read.',
          'Assamese': 'Gurdon\'s commentaries run to several sentences and carry concrete nouns, which is why a lexical index does comparatively well on this corpus.'}[L], 8.5)
        for i, L in enumerate(LANGS)
    ] + [
        ('fig', f'{CCA1}/report/figures/PanelB_16_category_distribution.png', 'Figure 1. Number of proverbs per shared category and language.', 4.8,
         'Society and human character dominate in all three corpora and nature imagery is third, so the three collections cover similar ground and can be queried in the same style.'),
        ('tbl', [('Sentence', 'Idiom', 'Usage label', 'Split')] + [tuple(r) for r in SR['magpie']], 'Table 6. MAGPIE rows: sentence, the idiom it contains, the annotated usage label and the split.',
         'The same idiom string appears with both labels, so the label depends on the surrounding sentence and not on the idiom; this is the property a usage detector has to learn.', 8.5),
        ('tbl', [('Record type', 'Expression', 'Literal translation or context', 'Meaning or usage label')] + [tuple(r) for r in SR['records']], 'Table 7. Records: two proverbs per corpus with literal translation and intended meaning, and three MAGPIE idiom occurrences with their usage label.',
         'A proverb record carries its meaning as free text written by the compiler, while an idiom record carries only a usage label; this is why proverb experiments are scored by similarity to a text and the idiom experiment by classification accuracy.', 8.5),
    ]
    F.fill_section('DATA DESCRIPTION', dd)

    # ---------- methods ----------
    meth = [
        ('p', 'Corpus construction. The OCR text of each book was downloaded from the Internet Archive [1-3]. The text was split into entries (numbered entries for Gurdon, section page-headers and entry breaks for Manwaring, romanized-line detection for Fallon). Inside each entry, every block was scored by the fraction of its words that are common English function words: a low share marks the romanized proverb, a high share in the first block marks the literal translation, and later high-share blocks, parenthesised notes or blocks with cue phrases such as "said of" mark the recorded meaning. Stray symbols were removed, junk tails trimmed and garbage lines dropped. An entry was kept only if the proverb and the translation each had at least three recoverable words; Fallon entries also had to pass an English-ratio check on translation and gloss. This is why the corpora are smaller than the books (Marathi about 1,900 printed, 545 kept; Hindi 449 candidates, 344 kept; Assamese 218 parsed, 103 kept): damaged entries were dropped rather than patched. Theme labels come from the books\' own section headings, and a keyword map assigns one of six shared categories (human nature, society, nature and animals, livelihood, fortune and fate, wisdom) with the basis recorded per row. Figure 2 shows the pipeline.'),
        ('fig', f'{CCA1}/report/figures/PanelB_16_flowchart_pipeline.png', 'Figure 2. From scanned book to usable corpus; the counts beside the red box are entries found against entries kept.', 4.4,
         'Most of the loss happens at the acceptance rule, not at OCR: entries were dropped whenever the proverb or the translation could not be recovered, so the kept rows are clean at the cost of coverage.'),
        ('p', 'Representations. Two representations are used throughout: TF-IDF vectors (scikit-learn [14], English stop words removed, sublinear term frequency) and LaBSE sentence embeddings [5,6], normalised so that the dot product is the cosine similarity. Both run on CPU.'),
        ('p', 'Situation-to-proverb retrieval. For each corpus the recorded meanings of all proverbs that have one (338, 305 and 75) are indexed with both representations. A query is a one-sentence situation description written by a team member who did not build that index, targeting one proverb and avoiding the words of its recorded meaning; 10 Marathi, 8 Hindi and 10 Assamese queries were written. Proverbs are ranked by the similarity of their recorded meaning to the query, and Hit@1, Hit@5 and mean reciprocal rank are computed against a random-ranking baseline.'),
        ('p', 'Idiom-usage detection. Step A trains TF-IDF over word unigrams and bigrams with logistic regression (balanced class weights) on the MAGPIE training split (38,716 sentences) and tests on its test split (4,840), labels idiomatic versus literal usage [4]. Step B applies the same recipe to each language: the proverbs (literal translations) are placed in six carrier sentences as positives and real literal MAGPIE sentences of 5 to 25 tokens are placed in the same carriers as negatives, under 5-fold cross-validation, so the carriers cancel and the classifier decides from content.'),
        ('p', 'Interpretation benchmark. 60 proverbs with recorded meanings per language (random sample, seed 42) are given to Qwen2.5-0.5B-Instruct [8] and FLAN-T5-base [7] with the prompt "Explain the meaning of this proverb in one sentence", once with the literal translation and once with the romanized source text. The answer is scored by LaBSE similarity to the recorded meaning; the control is its similarity to a random other recorded meaning; the margin is the difference. The echo baseline scores the literal translation itself the same way. Greedy decoding for Qwen (chat template, left padding), two-beam decoding for FLAN-T5, 48 new tokens, batches of eight.'),
    ]
    meth.append(('fig', f'{CCA3}/report/figures/extras/methodology.png', 'Figure 3. Design of the three experiments on the three corpora.', 4.8,
                 'The three experiments share their inputs and their evaluation style but not their models, so a difference between them is a difference in task, not in data preparation.'))
    F.fill_section('EXPERIMENTAL DESIGN, MATERIALS AND METHODS', meth)

    # ---------- limitations ----------
    lim = [
        ('b', 'OCR noise. The books were printed between 1886 and 1899 and the OCR text carries character errors in many translations and meanings; rows were kept whenever the fields were recoverable, so noisy rows are present. The raw text is included so that they can be corrected.'),
        ('b', 'Romanization. The proverbs are in the books\' nineteenth-century romanization, not native script, which is the main reason multilingual models perform poorly on them; native-script recovery is the next step.'),
        ('b', 'Size. The Assamese corpus has 103 proverbs (75 with meanings), the smallest of the three; the situation query sets have 8 to 10 items per language, so retrieval scores carry wide uncertainty.'),
        ('b', 'Idiom detection is English-only. MAGPIE is an English corpus; the proverbs reach the detector through their English translations, and the carrier-sentence data differ in register from modern English, which inflates the Step B scores.'),
        ('b', 'The language models are small (0.5 and 0.25 billion parameters) and were run on CPU; the famous-versus-obscure split of the benchmark needs a frequency source and was not run.'),
    ]
    F.fill_section('LIMITATIONS', lim)

    F.fill_section('ETHICS STATEMENT', [
        ('p', 'The work did not involve human subjects, animal experiments or data collected from social media platforms. The primary sources are books published between 1886 and 1899 that are in the public domain; the MAGPIE corpus is redistributed under its research licence, which is included with the data. The authors have read and follow the ethical requirements for publication in Data in Brief.'),
    ])
    F.fill_section('CRediT AUTHOR STATEMENT', [
        ('p', 'Sahish Nagulwar: Data curation (Marathi corpus), Investigation (situation-to-proverb retrieval), Software, Visualization, Writing - original draft. '
              'Ibrahim Ansari: Data curation (Hindi corpus), Investigation (idiom-usage detection), Software (extraction pipeline), Visualization, Writing - original draft. '
              'Chayan Raj Bharati: Data curation (Assamese corpus), Investigation (interpretation benchmark), Validation, Visualization, Writing - review and editing. All authors wrote the situation queries for a language other than their own.'),
    ])
    F.fill_section('ACKNOWLEDGEMENTS', [
        ('p', 'The authors thank Dr. Suja Panickar, course instructor for Cloud Computing and Natural Language Processing, for the problem statement and the review of the course reports. This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.'),
    ])
    F.fill_section('DECLARATION OF COMPETING INTERESTS', [
        ('p', 'The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.'),
    ])
    F.fill_section('REFERENCES', [('p', f'[{i + 1}] {r}') for i, r in enumerate(REFS)])

    out = f'{CCA3}/v3/PanelB_16_LCA3_MiniProject_DataArticle.docx'
    doc.save(out)
    print('written', out)


if __name__ == '__main__':
    import os
    os.makedirs(f'{CCA3}/v3', exist_ok=True)
    build('lca3')
