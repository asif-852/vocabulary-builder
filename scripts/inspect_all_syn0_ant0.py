# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

print(f"{'#':<4} {'Word':<18} {'POS':<10} {'Synonym[0] (Mode 4 Answer)':<22} {'Antonym[0] (Mode 5 Answer)':<22}")
print("-" * 80)
for idx in range(1, 201):
    w = corpus[idx - 1]
    word = w['word']
    pos = w['partOfSpeech']
    s0 = w['synonyms'][0] if w['synonyms'] else "NONE"
    a0 = w['antonyms'][0] if w['antonyms'] else "NONE"
    print(f"{idx:<4} {word:<18} {pos:<10} {s0:<22} {a0:<22}")
