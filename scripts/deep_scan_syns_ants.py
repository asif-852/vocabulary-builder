# -*- coding: utf-8 -*-
"""
Detailed check of synonyms and antonyms for all 200 words in Sets 1 to 10.
"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

for idx in range(1, 201):
    w = corpus[idx - 1]
    word = w['word']
    pos = w['partOfSpeech']
    syns = w.get('synonyms', [])
    ants = w.get('antonyms', [])
    
    # Are there any empty elements in syns or ants?
    for s in syns:
        if not s.strip():
            print(f"Word {idx} ({word}): Empty synonym in list!")
    for a in ants:
        if not a.strip():
            print(f"Word {idx} ({word}): Empty antonym in list!")
            
    # Check syns[0] and ants[0]
    s0 = syns[0]
    a0 = ants[0]
    
    # Check if s0 or a0 is the same as word
    if s0.lower() == word.lower():
        print(f"Word {idx} ({word}): syn[0] == word ('{s0}')")
    if a0.lower() == word.lower():
        print(f"Word {idx} ({word}): ant[0] == word ('{a0}')")

print("Detailed scan complete!")
