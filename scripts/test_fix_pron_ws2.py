import json
import re
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from test_fix_pron import fix_bengali_pronunciation

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/wordsmart2.json', 'r', encoding='utf-8') as f:
    ws2 = json.load(f)

still_bad = 0
for w in ws2:
    fixed = fix_bengali_pronunciation(w.get('pronunciationBn', ''), w.get('pronunciationEn', ''))
    if re.search(r'[a-zA-Z]', fixed):
        still_bad += 1
        print(f"Still bad: {w['word']} -> orig: {w.get('pronunciationBn')} | fixed: {fixed}")

print(f"WS2 fixed! Remaining bad: {still_bad}/{len(ws2)}")
