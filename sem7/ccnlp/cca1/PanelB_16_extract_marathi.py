"""Build the Marathi proverb corpus from A. Manwaring, 'Marathi Proverbs' (1899).

Source: https://archive.org/details/marathiproverbs00manwgoog (public domain).
Entries: Devanagari line (OCR noise) -> romanized Marathi -> English literal
translation followed by the compiler's figurative explanation. Section page
headers (I. AGRICULTURE ... XII. ...) provide theme labels.
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
    'can', 'may', 'must', 'so', 'than', 'then', 'its', 'own', 'all',
}


def english_ratio(line):
    words = re.findall(r"[A-Za-z']+", line.lower())
    if not words:
        return 0.0
    return sum(w in ENGLISH_HINTS for w in words) / len(words)


def is_garbage(s):
    if not s.strip():
        return False
    ascii_alpha = sum(c.isalpha() and ord(c) < 128 for c in s)
    other = sum(ord(c) >= 128 or c in '*^%#@~|<>{}[]\\' for c in s)
    return other > max(ascii_alpha, 1) * 0.5


def clean(line):
    line = re.sub(r'[*^~|<>{}\[\]"]', '', line)
    line = re.sub(r'\s+', ' ', line)
    line = re.sub(r'\s+([,.;:!?])', r'\1', line)
    return line.strip(' -')


HEADER = re.compile(r'^\s*[IVXJl/]+\.?\s+([A-Z][A-Z &]{3,}?)\s*\d*\s*$')
NUMLINE = re.compile(r'^\s*\d{1,4}\s*$')


def main():
    lines = open(sys.argv[1], encoding='utf8', errors='ignore').read().split('\n')
    theme = 'Unknown'
    rows = []
    translit, body = None, []

    def trim_junk(text):
        out = []
        for w in text.split():
            alpha = sum(c.isalpha() and ord(c) < 128 for c in w)
            if re.fullmatch(r'\d{2,}.*', w) or alpha < len(w) * 0.6:
                break
            out.append(w)
        return ' '.join(out)

    def flush():
        nonlocal translit, body
        if translit and body:
            text = clean(' '.join(body))
            m = re.search(r'\.\s+(?=[A-Z(])', text)
            if m:
                literal, commentary = text[:m.start() + 1], text[m.end():]
            else:
                literal, commentary = text, ''
            commentary = trim_junk(commentary)
            if len(commentary.split()) < 3:
                commentary = ''
            if len(translit.split()) >= 3 and len(literal.split()) >= 3:
                t = re.sub(r'\s+[A-Za-z]$', '', theme).strip()
                rows.append({
                    'id': len(rows) + 1,
                    'theme': t.title(),
                    'theme_bucket': t.lower().replace(' ', '_'),
                    'proverb_translit': translit,
                    'literal_en': literal,
                    'commentary': commentary,
                })
        translit, body = None, []

    for raw in lines:
        s = raw.strip()
        h = HEADER.match(raw)
        if h:
            flush()
            theme = h.group(1).strip()
            continue
        if not s:
            continue
        if is_garbage(s) or NUMLINE.match(s):
            flush()
            continue
        c = clean(s)
        if not c:
            continue
        if translit is None:
            if english_ratio(c) < 0.25 and len(c.split()) >= 3 and c[0].isupper():
                translit = c
        else:
            body.append(c)
    flush()

    rows = [r for r in rows if r['theme'] != 'Unknown']
    with open(sys.argv[2], 'w', newline='', encoding='utf8') as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print(f'{len(rows)} proverbs written to {sys.argv[2]}')


if __name__ == '__main__':
    main()
