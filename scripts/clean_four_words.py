# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

for w in corpus:
    if w['word'] == 'Dogmatic':
        w['antonyms'] = ['flexible', 'tolerant', 'open-minded']
        print("Updated Dogmatic antonyms:", w['antonyms'])
    elif w['word'] == 'Euphemism':
        w['synonyms'] = ['understatement', 'softener', 'circumlocution']
        print("Updated Euphemism synonyms:", w['synonyms'])
    elif w['word'] == 'Felicitous':
        w['synonyms'] = ['apt', 'fitting', 'suitable']
        print("Updated Felicitous synonyms:", w['synonyms'])
    elif w['word'] == 'Insularity':
        w['antonyms'] = ['cosmopolitanism', 'openness', 'tolerance']
        print("Updated Insularity antonyms:", w['antonyms'])

with open('src/data/gre333.json', 'w', encoding='utf-8') as f:
    json.dump(corpus, f, ensure_ascii=False, indent=2)

print("Saved updates to gre333.json!")
