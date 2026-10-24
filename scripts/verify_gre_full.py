# -*- coding: utf-8 -*-
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

assert len(data) == 333
print('Length check passed: 333 items.')

for i in range(200):
    item = data[i]
    sc = item['sentenceCompletion']
    assert sc['sentenceWithBlank'].count('_____') == 1, f"Item {i+1} blank error"
    assert len(sc['options']) == 5, f"Item {i+1} options len error"
    assert len(sc['optionMeaningsBn']) == 5, f"Item {i+1} meanings len error"
    assert sc['options'][sc['correctIndex']].lower() == item['word'].lower(), f"Item {i+1} word match error: {sc['options'][sc['correctIndex']]} vs {item['word']}"
    for opt in sc['options']:
        assert opt[0].isupper(), f"Item {i+1} option not title-cased: {opt}"
    for m in sc['optionMeaningsBn']:
        assert not re.search(r'[a-zA-Z]', m), f"Item {i+1} English in meaning: {m}"
    assert not re.search(r'[a-zA-Z]', sc['sentenceTranslationBn']), f"Item {i+1} English in translation"
    assert not re.search(r'[a-zA-Z]', item['pronunciationBn']), f"Item {i+1} English in pronunciationBn: {item['pronunciationBn']}"

print('SUCCESS: All 200 items in Sets 1 to 10 verified flawlessly!')
