"""Per-member contribution extracts of the team report.

Pulls the paragraphs, tables and figures of each member's part (Part I/II/III)
out of the team report (same text, same figure and table numbers) into one
short document per member.
"""
import json, re
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
import pandas as pd

def _merge_repeats(t, rows, col=0):
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
            merged.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        i = j + 1

SRC = 'v3/PanelB_16_LCA3_MiniProject_Report.docx'
R = json.load(open('report/PanelB_16_CCA3_v2_reverse_retrieval_metrics.json'))
I = json.load(open('report/PanelB_16_CCA3_v2_idiom_detection_metrics.json'))
Q = json.load(open('report/PanelB_16_CCA3_v2_llm_benchmark_metrics.json'))
CASES = json.load(open('report/PanelB_16_CCA3_v2_cases.json'))
SR = json.load(open('report/PanelB_16_CCA3_v2_sample_rows.json'))
LANGS = ['Marathi', 'Hindi', 'Assamese']

MEMBERS = {
    'Sahish Nagulwar': {
        'prn': '1032233310', 'part': 'Part I', 'rq': 'RQ1', 'results_head': '2.6.1',
        'corpus_fig': '../cca1/report/figures/PanelB_16_category_distribution.png',
        'result_figs': [f'report/figures/v2_reverse_retrieval/fig{i}.png' for i in range(1, 7)],
        'fig_widths': [3.8, 3.8, 3.8, 5.2, 3.8, 3.8],
        'notebook': 'PanelB_16_CCA3_v2_reverse_retrieval.ipynb',
    },
    'Ibrahim Ansari': {
        'prn': '1032233145', 'part': 'Part II', 'rq': 'RQ2', 'results_head': '2.6.2',
        'corpus_fig': 'report/figures/v2_idiom_detection/fig1.png',
        'result_figs': [f'report/figures/v2_idiom_detection/fig{i}.png' for i in range(2, 7)],
        'fig_widths': [3.8, 3.8, 4.4, 5.4, 3.8],
        'notebook': 'PanelB_16_CCA3_v2_idiom_detection.ipynb',
    },
    'Chayan Raj Bharati': {
        'prn': '1032233134', 'part': 'Part III', 'rq': 'RQ3', 'results_head': '2.6.3',
        'corpus_fig': '../cca1/report/figures/PanelB_16_assamese_fig2.png',
        'result_figs': [f'report/figures/v2_llm_benchmark/fig{i}.png' for i in range(1, 6)],
        'fig_widths': [3.8, 3.8, 3.8, 5.2, 3.8],
        'notebook': 'PanelB_16_CCA3_v2_llm_benchmark.ipynb',
    },
}

src = Document(SRC)
paras = [(p.style.name, p.text) for p in src.paragraphs]
TABLE_RE = re.compile(r'^Table \d+: ')


def section_paras(h_prefix):
    out, on = [], False
    for style, text in paras:
        if style.startswith('Heading') and text.startswith(h_prefix):
            on = True; continue
        if on and style.startswith('Heading'):
            break
        if on:
            out.append((style, text))
    return out


def case_rows(name):
    if name == 'Sahish Nagulwar':
        revc = pd.DataFrame(CASES['reverse'])
        hits = revc[revc['rank'] == 1].head(3); misses = revc[revc['rank'] > 5].sort_values('rank', ascending=False).head(3)
        rows = [('Outcome', 'Language', 'Situation query', 'Target proverb (literal)', 'Returned first', 'Rank of target')]
        for _, r in hits.iterrows(): rows.append(('success', r.language, r.query, r.target, r.returned, r['rank']))
        for _, r in misses.iterrows(): rows.append(('failure', r.language, r.query, r.target, r.returned, r['rank']))
        return rows
    if name == 'Ibrahim Ansari':
        return [('Outcome', 'Sentence', 'Idiom', 'True', 'Predicted', 'P(idiomatic)')] + [
            (r['outcome'], r['sentence'], r['idiom'], r['true'], r['predicted'], r['p_idiomatic']) for r in CASES['idiom']]
    return [('Outcome', 'Language', 'Proverb (literal)', 'Recorded meaning', 'Model answer', 'Margin')] + [
        (r['outcome'], r['language'], r['proverb'], r['gold'], r['answer'], f"{r['margin']:+.2f}") for r in CASES['llm']]


def table_rows(name):
    rs = R['summary']
    if name == 'Sahish Nagulwar':
        return [('Language', 'Index', 'Hit@1', 'Hit@5', 'MRR')] + [
            (L, {'tfidf': 'TF-IDF', 'labse': 'LaBSE', 'random': 'Random'}[m], rs[f'{L}/{m}']['hit_at_1'], rs[f'{L}/{m}']['hit_at_5'], rs[f'{L}/{m}']['mrr'])
            for L in LANGS for m in ['tfidf', 'labse', 'random']]
    if name == 'Ibrahim Ansari':
        mg = I['magpie']
        return [('Set', 'Sentences', 'Accuracy', 'Macro-F1', 'Baseline'),
                ('MAGPIE test (Step A)', f'{mg["test"]:,}', mg['acc'], mg['macro_f1'], f'majority {mg["majority_acc"]}')] + [
            (f'{L} proverbs in carriers (Step B)', f'{I[f"step_b_{L.lower()}"]["n"]:,}', I[f'step_b_{L.lower()}']['acc'], I[f'step_b_{L.lower()}']['macro_f1'], 'chance 0.5') for L in LANGS]
    systems = ['Qwen2.5-0.5B / literal_en', 'Qwen2.5-0.5B / romanized', 'flan-t5-base / literal_en', 'flan-t5-base / romanized', 'echo baseline']
    return [('System',) + tuple(f'{L}: margin' for L in LANGS)] + [
        (s,) + tuple(f'{Q["benchmark"][f"{L}/{s}"]["margin"]:+.3f}' for L in LANGS) for s in systems]


for name, cfg in MEMBERS.items():
    part = cfg['part']
    doc = Document()
    st = doc.styles['Normal']; st.font.name = 'Times New Roman'; st.font.size = Pt(10.5)

    def p(t, bold=False, italic=False, center=False, size=None):
        par = doc.add_paragraph()
        if center: par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = par.add_run(t); r.bold = bold; r.italic = italic
        if size: r.font.size = Pt(size)
    def h(t, lvl=1): doc.add_heading(t, level=lvl)
    def caption(t):
        par = doc.add_paragraph(); par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = par.add_run(t); r.italic = True; r.font.size = Pt(9.5)
    def inference(t):
        par = doc.add_paragraph(); r = par.add_run('Inference: '); r.bold = True; par.add_run(t[len('Inference: '):])
    def figure(path, cap, inf, width):
        par = doc.add_paragraph(); par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.add_run().add_picture(path, width=Inches(width)); caption(cap)
        if inf: inference(inf)
    def table(rows, cap, size=None):
        caption(cap)
        t = doc.add_table(rows=len(rows), cols=len(rows[0])); t.style = 'Table Grid'
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                c = t.rows[i].cells[j]; c.text = str(cell)
                r = c.paragraphs[0].runs[0]
                if i == 0: r.bold = True
                if size: r.font.size = Pt(size)
        _merge_repeats(t, rows)

    def emit(block, figs=None, widths=None, tables=None):
        """Replay a run of report paragraphs: figures, tables (with their inference lines) and text."""
        fi = ti = 0
        for s, t in block:
            if t.startswith('Figure ') and figs is not None and fi < len(figs):
                figure(figs[fi], t, None, widths[fi]); fi += 1
            elif TABLE_RE.match(t) and tables is not None and ti < len(tables):
                table(tables[ti], t, size=8.5); ti += 1
            elif t.startswith('Inference:'):
                inference(t)
            elif t.strip():
                p(t)
        return fi

    p('CCA3 — Cloud Computing & Natural Language Processing — Panel B, Team 16', center=True, bold=True)
    doc.add_heading(f'Individual contribution to the team report: {name} ({cfg["prn"]})', level=0)
    p(f'This document collects the sections of the team report (PanelB_16_LCA3_MiniProject_Report.docx) that belong to {part}, '
      f'the part contributed by {name}. The text, tables and figures are the same as in the team report, and figure and table '
      f'numbers are kept as in the team report so the two documents can be read side by side. The code for this contribution is {cfg["notebook"]}.', italic=True)

    h('Research question')
    p(next(t for s, t in section_paras('2.1') if t.startswith(f'{cfg["rq"]} ({part})')))
    h('Research contribution')
    p(next(t for s, t in section_paras('2.2') if t.startswith(f'{part}:')))
    h('Methodology')
    p(next(t for s, t in section_paras('2.3') if t.startswith(f'{part}:')))
    h('Description of corpora')
    p(next(t for s, t in section_paras('2.4 ') if t.startswith(f'{part}:')))
    h('Corpus analysis', 2)
    caps = section_paras('2.4.1')
    for i, (s, t) in enumerate(caps):
        if t.startswith('Figure ') and f'{part}:' in t:
            inf = caps[i + 1][1] if i + 1 < len(caps) and caps[i + 1][1].startswith('Inference:') else None
            figure(cfg['corpus_fig'], t, inf, 4.6)
    h('Implementation')
    p(next(t for s, t in section_paras('2.5') if t.startswith(f'{part} (')))
    if name == 'Ibrahim Ansari':
        impl = section_paras('2.5')
        keep = [k for k, (s_, t) in enumerate(impl) if TABLE_RE.match(t) and ('Training data for Step A' in t or 'Data for Step B' in t)]
        block = []
        for k in keep:
            block.append(impl[k])
            if k + 1 < len(impl) and impl[k + 1][1].startswith('Inference:'): block.append(impl[k + 1])
        emit(block, tables=[[('Sentence', 'Idiom', 'Label')] + [tuple(r) for r in SR['train_a']],
                            [('Carrier sentence', 'Label', 'Source')] + [tuple(r) for r in SR['train_b']]])
    h('Results')
    res = section_paras(cfg['results_head'])
    tabs = [case_rows(name) if 'success' in t else table_rows(name) for s, t in res if TABLE_RE.match(t)]
    fi = emit(res, cfg['result_figs'], cfg['fig_widths'], tabs)
    h('Discussion')
    p(next(t for s, t in section_paras('2.7') if t.startswith(f'{part}:')))

    out = f'report/PanelB_16_CCA3_contribution_{name.split()[0]}.docx'
    doc.save(out)
    print('written', out, '| result figures', fi, '| tables', len(tabs))
