# -*- coding: utf-8 -*-
import json
import sys
from nltk.corpus import wordnet as wn

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

words_11_17 = corpus[200:333]

pos_map = {
    'noun': {'n'},
    'verb': {'v'},
    'adjective': {'a', 's'},
    'adverb': {'r'}
}

print("=== CHECKING ALL SYNONYMS AND ANTONYMS FOR POS MATCH ===")
oddities = []

for idx, w in enumerate(words_11_17, 201):
    word = w['word']
    pos = w['partOfSpeech']
    expected_wn = pos_map.get(pos, set())
    
    for i, s in enumerate(w.get('synonyms', [])):
        s_clean = s.strip().lower()
        poses = set(x.pos() for x in wn.synsets(s_clean))
        if poses and not expected_wn.intersection(poses):
            oddities.append((idx, word, pos, f"syn[{i}]", s, list(poses)))
            
    for i, a in enumerate(w.get('antonyms', [])):
        a_clean = a.strip().lower()
        poses = set(x.pos() for x in wn.synsets(a_clean))
        if poses and not expected_wn.intersection(poses):
            oddities.append((idx, word, pos, f"ant[{i}]", a, list(poses)))

print(f"Total entries with POS mismatch in all syn/ant lists: {len(oddities)}")
for o in oddities:
    print(f"[{o[0]}] {o[1]} ({o[2]}): {o[3]} '{o[4]}' has POS {o[5]}")
