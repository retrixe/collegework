"""Build the Hindi/Hindustani proverb corpus from S. W. Fallon,
'A Dictionary of Hindustani Proverbs' (1886).

Source: https://archive.org/details/in.ernet.dli.2015.42145 (public domain).
Entries: romanized Hindustani proverb (italic in print) -> English literal
translation -> parenthesized note giving the figurative sense / usage.
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
    'can', 'may', 'must', 'so', 'than', 'then', 'its', 'own', 'all', 'up',
    'out', 'over', 'your', 'man', 'still', 'yet', 'more', 'good',
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
    return other > max(ascii_alpha, 1) * 0.4


def clean(line):
    line = re.sub(r'[*^~|<>{}\[\]"]', '', line)
    line = re.sub(r'\b(Hin|Mah|Mar|Pan|P|E|H|M)\.\s*$', '', line)
    line = re.sub(r'\s+', ' ', line)
    line = re.sub(r'\s+([,.;:!?])', r'\1', line)
    return line.strip(' -')


def looks_translit(s):
    if english_ratio(s) >= 0.2:
        return False
    words = s.split()
    if not (3 <= len(words) <= 16):
        return False
    alpha = sum(c.isalpha() for c in s)
    return alpha >= len(s) * 0.6 and s[0].isupper()


def main():
    lines = open(sys.argv[1], encoding='utf8', errors='ignore').read().split('\n')
    rows = []
    i = 0
    while i < len(lines):
        s = clean(lines[i].strip())
        if s and not is_garbage(s) and looks_translit(s):
            translation, commentary = [], []
            j = i + 1
            while j < len(lines) and j < i + 8:
                t = clean(lines[j].strip())
                if not t:
                    if translation:
                        break
                    j += 1
                    continue
                if is_garbage(t) or looks_translit(t):
                    break
                if t.startswith('('):
                    while j < len(lines) and j < i + 12:
                        c = clean(lines[j].strip())
                        if c:
                            commentary.append(c.strip('() '))
                        if ')' in lines[j]:
                            break
                        j += 1
                    break
                if english_ratio(t) >= 0.25:
                    translation.append(t)
                j += 1
            literal = ' '.join(translation)
            comm = ' '.join(commentary)
            if (len(literal.split()) >= 4 and comm
                    and len(comm.split()) >= 3
                    and english_ratio(literal) >= 0.25
                    and english_ratio(comm) >= 0.2):
                rows.append({
                    'id': len(rows) + 1,
                    'theme': '',
                    'theme_bucket': '',
                    'proverb_translit': s,
                    'literal_en': literal,
                    'commentary': comm,
                })
            i = j
        i += 1

    with open(sys.argv[2], 'w', newline='', encoding='utf8') as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print(f'{len(rows)} proverbs written to {sys.argv[2]}')


if __name__ == '__main__':
    main()
