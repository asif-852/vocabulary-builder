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

print("=== CHECKING POS ALIGNMENT FOR SETS 11-17 (WORDS 201-333) ===")
pos_mismatches = []

for idx, w in enumerate(words_11_17, 201):
    word = w['word']
    pos = w['partOfSpeech']
    expected_wn = pos_map.get(pos, set())
    
    s0 = w['synonyms'][0] if w.get('synonyms') else None
    a0 = w['antonyms'][0] if w.get('antonyms') else None
    
    s0_poses = set(s.pos() for s in wn.synsets(s0)) if s0 else set()
    a0_poses = set(s.pos() for s in wn.synsets(a0)) if a0 else set()
    
    s0_ok = bool(expected_wn.intersection(s0_poses))
    a0_ok = bool(expected_wn.intersection(a0_poses))
    
    if not s0_ok:
        pos_mismatches.append((idx, word, pos, 'syn[0]', s0, list(s0_poses)))
    if not a0_ok:
        pos_mismatches.append((idx, word, pos, 'ant[0]', a0, list(a0_poses)))

print(f"Total potential POS mismatches: {len(pos_mismatches)}")
for m in pos_mismatches:
    print(f"Word {m[0]} '{m[1]}' ({m[2]}): {m[3]} '{m[4]}' has WordNet POS {m[5]}")
