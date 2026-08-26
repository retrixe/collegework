"""Assign one shared category scheme to all three corpora and write the
Excel workbooks required for submission.

Categories (same six for every language):
  Human Nature & Character, Society & Relationships, Nature & Animals,
  Livelihood & Agriculture, Fortune & Fate, Wisdom & Advice.

Marathi and Assamese are mapped from the labels the books already carry
(section headings / theme buckets). Fallon's Hindi dictionary is
alphabetical and has no labels, so its rows are assigned by keyword rules
over the literal translation and gloss; rows matching no rule are labelled
Uncategorised rather than forced into a class.
"""
import re
import pandas as pd

CATS = ['Human Nature & Character', 'Society & Relationships', 'Nature & Animals',
        'Livelihood & Agriculture', 'Fortune & Fate', 'Wisdom & Advice']

MARATHI_MAP = {
    'Ethical': 'Human Nature & Character',
    'The Body And Its Members': 'Human Nature & Character',
    'Health And Disease': 'Human Nature & Character',
    'Relationship': 'Society & Relationships',
    'Names': 'Society & Relationships',
    'Religious': 'Society & Relationships',
    'Trades And Professions': 'Society & Relationships',
    'The House': 'Society & Relationships',
    'Animals': 'Nature & Animals',
    'Nature': 'Nature & Animals',
    'Agriculture': 'Livelihood & Agriculture',
    'Food': 'Livelihood & Agriculture',
    'Money': 'Livelihood & Agriculture',
    'Unclassified': 'Uncategorised',
}
ASSAMESE_MAP = {
    'vanity_boasting': 'Human Nature & Character',
    'greed_selfishness': 'Human Nature & Character',
    'deceit_vice': 'Human Nature & Character',
    'folly_ignorance': 'Human Nature & Character',
    'domestic_life': 'Society & Relationships',
    'social_castes': 'Society & Relationships',
    'nature_animals': 'Nature & Animals',
    'fate_misfortune': 'Fortune & Fate',
    'wisdom_advice': 'Wisdom & Advice',
    'other': 'Uncategorised',
}
HINDI_RULES = [
    ('Nature & Animals', r'\b(dog|cat|cow|ox|bull|horse|donkey|ass|goat|elephant|tiger|lion|snake|bird|crow|'
                         r'fish|fly|flies|mouse|rat|camel|monkey|jackal|frog|tree|river|rain|water|sun|moon|'
                         r'wind|fire|stone|forest|jungle|flower|leaf|leaves|thorn|mango|neem)\b'),
    ('Livelihood & Agriculture', r'\b(field|crop|plough|harvest|grain|wheat|rice|corn|seed|farmer|kunbi|'
                                 r'money|rupee|paisa|pice|debt|loan|trade|shop|market|bazaar|sell|buy|wage|'
                                 r'work|labour|labor|bread|food|feast|hunger|salt|ghee|oil|cloth|weaver|potter|'
                                 r'blacksmith|barber|cook|beggar|rich|poor|wealth|poverty)\b'),
    ('Fortune & Fate', r'\b(fate|luck|fortune|destiny|god|heaven|misfortune|ruin|calamity|death|die|dead|'
                       r'grave|kismet|blessed|curse|cursed|disaster|doom)\b'),
    ('Society & Relationships', r'\b(wife|husband|mother|father|son|daughter|brother|sister|aunt|uncle|'
                                r'mother-in-law|daughter-in-law|family|friend|neighbour|neighbor|guest|host|'
                                r'king|raja|nawab|master|servant|slave|caste|brahman|brahmin|thakur|jat|'
                                r'village|marriage|married|wedding|widow|bride|child|children|woman|women)\b'),
    ('Wisdom & Advice', r'\b(said to|said of|advice|warn|warning|do not|don t|never|always|should|must|'
                        r'ought|lesson|teach|beware|caution|prudence|patience|haste|hasty)\b'),
    ('Human Nature & Character', r'\b(fool|foolish|folly|wise|wisdom|greed|greedy|proud|pride|vain|vanity|'
                                 r'boast|boasting|liar|lie|lies|cheat|thief|steal|coward|brave|lazy|idle|'
                                 r'miser|stingy|hypocrite|hypocrisy|shame|shameless|anger|angry|jealous|'
                                 r'envy|selfish|honest|honour|honor|cunning|clever|stupid|ignorant|impudent|'
                                 r'spendthrift|extravagant|drunk|glutton)\b'),
]


def hindi_category(row):
    text = f"{row.literal_en} {row.commentary}".lower().replace("'", ' ')
    scores = {}
    for cat, pat in HINDI_RULES:
        n = len(re.findall(pat, text))
        if n:
            scores[cat] = n
    if not scores:
        return 'Uncategorised', ''
    best = max(scores, key=lambda c: (scores[c], -[c for c, _ in HINDI_RULES].index(c)))
    hits = sorted(set(re.findall(dict(HINDI_RULES)[best], text)))[:4]
    return best, ', '.join(hits)


def build():
    mr = pd.read_csv('corpus/PanelB_16_marathi_proverbs.csv')
    hi = pd.read_csv('corpus/PanelB_16_hindi_proverbs.csv')
    as_ = pd.read_csv('corpus/PanelB_16_assamese_proverbs.csv')

    mr['category'] = mr.theme.map(MARATHI_MAP).fillna('Uncategorised')
    mr['category_basis'] = 'book section: ' + mr.theme
    as_['category'] = as_.theme_bucket.map(ASSAMESE_MAP).fillna('Uncategorised')
    as_['category_basis'] = 'book heading: ' + as_.theme
    hc = hi.apply(hindi_category, axis=1, result_type='expand')
    hi['category'] = hc[0]
    hi['category_basis'] = 'keyword rule: ' + hc[1]
    hi = hi.drop(columns=['theme', 'theme_bucket'])

    for name, df in [('marathi', mr), ('hindi', hi), ('assamese', as_)]:
        df.to_csv(f'corpus/PanelB_16_{name}_categorised.csv', index=False)

    cols = ['language', 'id', 'category', 'category_basis', 'proverb_translit', 'literal_en', 'commentary']
    mr['language'] = 'Marathi'; hi['language'] = 'Hindi'; as_['language'] = 'Assamese'
    all_ = pd.concat([mr[cols], hi[cols], as_[cols]], ignore_index=True)

    summary = pd.crosstab(all_.category, all_.language).reindex(CATS + ['Uncategorised'])
    summary['Total'] = summary.sum(axis=1)
    summary.loc['Total'] = summary.sum()

    with pd.ExcelWriter('corpus/PanelB_16_all_corpora_categorised.xlsx', engine='openpyxl') as xw:
        summary.to_excel(xw, sheet_name='Category summary')
        pd.DataFrame({
            'Category': CATS + ['Uncategorised'],
            'What it covers': [
                'Vices and virtues of individuals: vanity, greed, deceit, folly, courage, honesty',
                'Family, marriage, caste, master and servant, kings, village life, religion',
                'Animals, plants, weather, water, fire and other natural imagery',
                'Farming, crops, food, money, debt, trades and work',
                'Luck, destiny, God, death, calamity',
                'Proverbs that give a rule, warning or piece of practical advice',
                'Rows the sources or rules could not place with confidence',
            ],
            'Marathi basis': ['Manwaring section headings, mapped'] * 6 + ['book "Unclassified" section'],
            'Hindi basis': ['keyword rules over literal text + gloss'] * 6 + ['no rule matched'],
            'Assamese basis': ['Gurdon subject headings, bucketed then mapped'] * 6 + ['bucket "other"'],
        }).to_excel(xw, sheet_name='Category scheme', index=False)
        all_.to_excel(xw, sheet_name='All rows', index=False)
        for name, df in [('Marathi', mr), ('Hindi', hi), ('Assamese', as_)]:
            df.drop(columns=['language']).to_excel(xw, sheet_name=name, index=False)

    for name, df, raw in [('marathi', mr, 'PanelB_16_marathi_manwaring1899_raw.txt'),
                          ('hindi', hi, 'PanelB_16_hindi_fallon1886_raw.txt'),
                          ('assamese', as_, 'PanelB_16_assamese_gurdon1896_raw.txt')]:
        with pd.ExcelWriter(f'corpus/PanelB_16_{name}_corpus.xlsx', engine='openpyxl') as xw:
            df.drop(columns=['language']).to_excel(xw, sheet_name='Cleaned corpus', index=False)
            df.groupby('category').size().rename('proverbs').to_frame().to_excel(xw, sheet_name='By category')
            lines = open(f'corpus/{raw}', encoding='utf8', errors='ignore').read().split('\n')
            pd.DataFrame({'line_no': range(1, len(lines) + 1), 'raw_ocr_text': lines}).to_excel(
                xw, sheet_name='Raw OCR text', index=False)
    print(summary.to_string())


if __name__ == '__main__':
    build()
