# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
data = json.load(open('src/data/gre333.json', encoding='utf-8'))

words_11_17 = data[200:333]

same_letter_clump = []
arf_clump = []

for w in words_11_17:
    dists = [o['word'] for o in w['multiSynonyms']['options'] if not o['isSynonym']]
    first_letters = [d[0].upper() for d in dists]
    
    # Check if all 3 distractors have distinct initial letters
    if len(set(first_letters)) < 3:
        same_letter_clump.append((w['word'], dists))
        
    # Check if distractors are dominated by A, R, or F (e.g. 2 or more from {A, R, F})
    arf_count = sum(1 for ch in first_letters if ch in {'A', 'R', 'F'})
    if arf_count >= 2:
        arf_clump.append((w['word'], dists))

print(f"Distractor clumps with duplicate starting letters: {len(same_letter_clump)}")
for item in same_letter_clump:
    print(" ", item)
    
print(f"Distractor clumps with 2+ letters from {{A, R, F}}: {len(arf_clump)}")
for item in arf_clump:
    print(" ", item)
