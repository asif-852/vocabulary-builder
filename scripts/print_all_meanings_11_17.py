# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

words_11_to_17 = corpus[200:333]

print(f"{'#':<4} {'Word':<18} {'POS':<10} {'Meaning (Bn)':<35} {'Meaning (En)'}")
print("-" * 100)
for idx, w in enumerate(words_11_to_17, 201):
    m_bn = w['meaningBn'][:33]
    m_en = w['meaningEn'][:45]
    print(f"{idx:<4} {w['word']:<18} {w['partOfSpeech']:<10} {m_bn:<35} {m_en}")
