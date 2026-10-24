# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

print(f"Total words in gre333: {len(corpus)}")

# Let's check words 1 to 200 (Sets 1 to 10)
words_1_to_200 = corpus[:200]

# Check synonyms and antonyms
empty_synonyms = []
empty_antonyms = []
single_synonyms = []
single_antonyms = []

for idx, w in enumerate(words_1_to_200, 1):
    syns = w.get('synonyms', [])
    ants = w.get('antonyms', [])
    
    if not syns:
        empty_synonyms.append((idx, w['word']))
    if not ants:
        empty_antonyms.append((idx, w['word']))

print(f"Words with EMPTY synonyms (out of 200): {len(empty_synonyms)}")
if empty_synonyms:
    print("Empty synonyms:", empty_synonyms)

print(f"Words with EMPTY antonyms (out of 200): {len(empty_antonyms)}")
if empty_antonyms:
    print("Empty antonyms:", empty_antonyms)
