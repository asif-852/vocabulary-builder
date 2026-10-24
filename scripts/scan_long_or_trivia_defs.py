# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

for idx, w in enumerate(corpus[200:333], 201):
    m = w['meaningEn']
    # Check if length > 120 or contains weird historical/latin trivia
    if len(m) > 90 or any(kw in m.lower() for kw in ['roman', 'carthaginian', 'latin', 'greek', 'specifically', 'especially having']):
        print(f"[{idx}: {w['word']}] -> {m}")
