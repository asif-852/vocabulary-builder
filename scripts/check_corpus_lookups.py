# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

corpus_map = {w['word'].lower(): w for w in corpus}

words_11_17 = corpus[200:333]

print("=== CHECKING CORPUS LOOKUP FOR SYN0 AND ANT0 ===")
not_in_corpus_syn = []
not_in_corpus_ant = []

for idx, w in enumerate(words_11_17, 201):
    s0 = w['synonyms'][0] if w.get('synonyms') else ""
    a0 = w['antonyms'][0] if w.get('antonyms') else ""
    
    if s0 and s0.lower() not in corpus_map:
        not_in_corpus_syn.append((idx, w['word'], s0))
    if a0 and a0.lower() not in corpus_map:
        not_in_corpus_ant.append((idx, w['word'], a0))

print(f"syn[0] not in gre333 corpus: {len(not_in_corpus_syn)}")
for x in not_in_corpus_syn[:10]:
    print(" ", x)
print(f"ant[0] not in gre333 corpus: {len(not_in_corpus_ant)}")
for x in not_in_corpus_ant[:10]:
    print(" ", x)
