# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

# Fix word 267 (Qualified)
w267 = corpus[266]
print(f"Before: [{w267['word']}] {w267['meaningBn']}, syns={w267['synonyms']}, ants={w267['antonyms']}")
w267['meaningBn'] = 'শর্তসাপেক্ষ বা সীমিত'
w267['synonyms'] = ['conditional', 'limited', 'restricted', 'guarded']
w267['antonyms'] = ['unconditional', 'absolute', 'unlimited', 'categorical']
print(f"After: [{w267['word']}] {w267['meaningBn']}, syns={w267['synonyms']}, ants={w267['antonyms']}")

with open('src/data/gre333.json', 'w', encoding='utf-8') as f:
    json.dump(corpus, f, ensure_ascii=False, indent=2)

print("Updated Qualified in gre333.json!")
