"""Build the Assamese proverb corpus from P. R. Gurdon, 'Some Assamese Proverbs' (1896).

Source: https://archive.org/details/someassameseprov00gurdrich (public domain).
Reads the raw OCR text directly, splits it into numbered proverb entries,
and extracts per proverb: theme, romanized Assamese text, literal English
translation and the compiler's cultural commentary.

Usage: python PanelB_16_build_corpus.py <raw_ocr.txt> <output.csv>
"""
import csv
import re
import sys

ENGLISH_HINTS = {
    'the', 'a', 'an', 'of', 'to', 'and', 'is', 'are', 'was', 'were', 'he',
    'she', 'it', 'his', 'her', 'you', 'i', 'not', 'in', 'on', 'with', 'who',
    'has', 'have', 'one', 'but', 'for', 'that', 'this', 'they', 'there',
    'what', 'when', 'while', 'my', 'me', 'we', 'no', 'do', 'did', 'does',
    'by', 'from', 'as', 'at', 'be', 'been', 'will', 'would', 'if', 'even',
}
COMMENT_CUES = re.compile(
    r'\b(means|proverb|refers|is used|is said|is a |applied to|equivalent|'
    r'literally|alludes|saying|expression|common|reading)\b', re.I)


def english_ratio(line):
    words = re.findall(r"[A-Za-z']+", line.lower())
    if not words:
        return 0.0
    return sum(w in ENGLISH_HINTS for w in words) / len(words)


def clean(line):
    line = re.sub(r'[*^~|<>{}\[\]"]', '', line)
    line = re.sub(r'\s+', ' ', line)
    line = re.sub(r'\s+([,.;:!?])', r'\1', line)
    return line.strip(' -')


def classify_blocks(blocks):
    translit, translation, commentary = [], [], []
    for blk in blocks:
        joined = clean(' '.join(blk))
        if len(joined.split()) < 2:
            continue
        ratio = english_ratio(joined)
        if not translit and not translation and ratio < 0.22:
            translit.append(joined)
        elif not commentary and ratio >= 0.22 and not COMMENT_CUES.search(joined):
            translation.append(joined)
        elif translation or translit:
            commentary.append(joined)
    return ' '.join(translit), ' '.join(translation), ' '.join(commentary)


BUCKETS = [
    ('vanity_boasting', ['exagger', 'boast', 'conceit', 'false display',
                         'affectation', 'vanity', 'pride', 'egotism',
                         'importance', 'aiming too high']),
    ('deceit_vice', ['lying', 'thie', 'trick', 'excuse', 'blaming',
                     'toady', 'pitfall', 'trap', 'hypocrisy', 'cunning']),
    ('greed_selfishness', ['greed', 'selfish', 'stinginess', 'sponging',
                           'avarice', 'covet', 'improvidence', 'craving']),
    ('domestic_life', ['husband', 'wife', 'widow', 'women', 'mother',
                       'daughter', 'family', 'marriage', 'co-wife',
                       'shrew', 'relations', 'sleep']),
    ('social_castes', ['brahmin', 'bhakat', 'caste', 'dom', 'barber',
                       'goldsmith', 'oilman', 'weaver', 'priest', 'ahom',
                       'mariy', 'natja', 'porter', 'learned', 'village',
                       'poor', 'blind', 'one-eyed', 'lame']),
    ('folly_ignorance', ['ignoran', 'inattention', 'foolish', 'fool',
                         'stupid', 'impatience', 'idle', 'laziness',
                         'restless', 'discontent', 'ingratitude']),
    ('fate_misfortune', ['fate', 'misfortune', 'sin', 'punishment',
                         'ill-luck', 'irony', 'gone wrong', 'terrible']),
    ('wisdom_advice', ['advice', 'don', 'never', 'how ', 'evidence',
                       'tested', 'teach', 'nothing to do', 'waste',
                       'care', 'discriminating', 'use o']),
    ('nature_animals', ['dog', 'cat', 'tiger', 'elephant', 'crow', 'fish',
                        'betelnut', 'paddy', 'rain', 'weather', 'crop',
                        'mosquito', 'sparrow', 'cock', 'brinjal',
                        'jack fruit', 'tree', 'seluk', 'plough', 'seedling',
                        'oil', 'dheki', 'wood', 'sickle', 'grass', 'bone']),
]


def bucket(theme):
    t = theme.lower()
    for name, keys in BUCKETS:
        if any(k in t for k in keys):
            return name
    return 'other'


def is_garbage(s):
    if not s.strip():
        return False
    ascii_alpha = sum(c.isalpha() and ord(c) < 128 for c in s)
    other = sum(ord(c) >= 128 or c in '*^%#@~|<>{}[]' for c in s)
    return other > ascii_alpha * 0.6


def is_header(s):
    t = s.strip()
    if not t:
        return False
    if re.fullmatch(r'[0-9ivxlc .\-]+', t.lower()):
        return True
    letters = [c for c in t if c.isalpha()]
    return len(letters) > 3 and all(c.isupper() for c in letters)


def parse_entries(raw_path):
    """Split the OCR text into numbered proverb entries, each a list of blocks."""
    lines = open(raw_path, encoding='utf8', errors='ignore').read().split('\n')
    entries, cur = [], None
    for raw in lines:
        m = re.match(r'^\s*(\d{1,3})\.\s+([A-Z][A-Za-z, \'\-]+[a-z])[.,]?\s*$', raw)
        if m and int(m.group(1)) < 400:
            if cur:
                entries.append(cur)
            cur = {'num': int(m.group(1)), 'theme': m.group(2).strip(), 'lines': []}
        elif cur is not None:
            s = raw.rstrip()
            if is_garbage(s) or is_header(s):
                continue
            cur['lines'].append(s)
    if cur:
        entries.append(cur)

    out = []
    for e in entries:
        blocks, blk = [], []
        for s in e['lines']:
            if s.strip():
                blk.append(s.strip())
            elif blk:
                blocks.append(blk)
                blk = []
        if blk:
            blocks.append(blk)
        if len(blocks) < 2:
            continue
        out.append({'num': e['num'], 'theme': e['theme'], 'blocks': blocks[:6]})
    return out


def main():
    entries = parse_entries(sys.argv[1])
    print(f'{len(entries)} entries parsed from {sys.argv[1]}')
    rows = []
    for e in entries:
        translit, translation, commentary = classify_blocks(e['blocks'])
        if len(translit.split()) < 3 or len(translation.split()) < 3:
            continue
        theme = clean(e['theme'])
        rows.append({
            'id': len(rows) + 1,
            'book_no': e['num'],
            'theme': theme,
            'theme_bucket': bucket(theme),
            'proverb_translit': translit,
            'literal_en': translation,
            'commentary': commentary,
        })

    with open(sys.argv[2], 'w', newline='', encoding='utf8') as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print(f'{len(rows)} proverbs written to {sys.argv[2]}')


if __name__ == '__main__':
    main()
