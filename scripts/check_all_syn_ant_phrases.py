# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

words_11_17 = corpus[200:333]

# Check all syn and ant arrays for phrases or definitions
phrase_syns = []
phrase_ants = []
for idx, w in enumerate(words_11_17, 201):
    for i, s in enumerate(w.get('synonyms', [])):
        if ' ' in s or '-' in s or len(s.split()) > 1:
            phrase_syns.append((idx, w['word'], f"syn[{i}]", s))
    for i, a in enumerate(w.get('antonyms', [])):
        if ' ' in a or '-' in a or len(a.split()) > 1:
            phrase_ants.append((idx, w['word'], f"ant[{i}]", a))

print("Multi-word or hyphenated in ALL synonyms:")
for x in phrase_syns:
    print(" ", x)
print("Multi-word or hyphenated in ALL antonyms:")
for x in phrase_ants:
    print(" ", x)
