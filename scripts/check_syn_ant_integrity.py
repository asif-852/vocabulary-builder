# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

words_11_17 = corpus[200:333]

all_issues = []

for idx, w in enumerate(words_11_17, 201):
    word = w['word']
    pos = w['partOfSpeech']
    syns = w.get('synonyms', [])
    ants = w.get('antonyms', [])
    
    # Check lengths
    if not syns:
        all_issues.append((idx, word, "Empty syns"))
    if not ants:
        all_issues.append((idx, word, "Empty ants"))
        
    # Check duplicates within lists
    if len(syns) != len(set(s.lower() for s in syns)):
        all_issues.append((idx, word, f"Duplicate in syns: {syns}"))
    if len(ants) != len(set(a.lower() for a in ants)):
        all_issues.append((idx, word, f"Duplicate in ants: {ants}"))
        
    # Check intersection between syns and ants
    overlap = set(s.lower() for s in syns).intersection(set(a.lower() for a in ants))
    if overlap:
        all_issues.append((idx, word, f"Overlap between syns and ants: {overlap}"))
        
    # Check if word itself is in syns or ants
    if word.lower() in [s.lower() for s in syns]:
        all_issues.append((idx, word, "Word itself in syns!"))
    if word.lower() in [a.lower() for a in ants]:
        all_issues.append((idx, word, "Word itself in ants!"))

print(f"Total list anomalies found: {len(all_issues)}")
for i in all_issues:
    print(" ", i)
