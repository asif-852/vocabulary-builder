# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

words_11_to_17 = corpus[200:333]

print(f"{'#':<4} {'Word':<18} {'Pronunciation (En)':<25} {'Pronunciation (Bn)'}")
print("-" * 75)
for idx, w in enumerate(words_11_to_17, 201):
    p_en = w.get('pronunciationEn', '')
    p_bn = w.get('pronunciationBn', '')
    # Check if p_en has no hyphen and word length > 4
    flag = ""
    if '-' not in p_en and len(w['word']) > 4 and not w['word'].lower().endswith('ed'):
        flag = " [NO HYPHEN]"
    print(f"{idx:<4} {w['word']:<18} {p_en:<25} {p_bn}{flag}")
