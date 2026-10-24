# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

words_1_to_200 = corpus[:200]

print("=== CHECKING SYNONYMS[0] AND ANTONYMS[0] FOR WORDS 1 TO 200 ===")
oddities = []

for idx, w in enumerate(words_1_to_200, 1):
    word = w['word']
    pos = w['partOfSpeech']
    syns = w.get('synonyms', [])
    ants = w.get('antonyms', [])
    
    s0 = syns[0] if syns else ""
    a0 = ants[0] if ants else ""
    
    # Check if s0 or a0 is empty or has strange characters
    if not s0:
        oddities.append((idx, word, "EMPTY syn[0]"))
    if not a0:
        oddities.append((idx, word, "EMPTY ant[0]"))
        
    # Check if s0 == word or a0 == word
    if s0.lower() == word.lower():
        oddities.append((idx, word, f"syn[0] is target word itself! '{s0}'"))
    if a0.lower() == word.lower():
        oddities.append((idx, word, f"ant[0] is target word itself! '{a0}'"))
        
    # Check if s0 == a0
    if s0.lower() == a0.lower() and s0:
        oddities.append((idx, word, f"syn[0] equals ant[0]! '{s0}'"))
        
    # Check if s0 or a0 has multiple words (spaces) or commas
    if ' ' in s0:
        oddities.append((idx, word, f"syn[0] has spaces: '{s0}'"))
    if ' ' in a0:
        oddities.append((idx, word, f"ant[0] has spaces: '{a0}'"))
        
    if ',' in s0 or ';' in s0:
        oddities.append((idx, word, f"syn[0] has punctuation: '{s0}'"))
    if ',' in a0 or ';' in a0:
        oddities.append((idx, word, f"ant[0] has punctuation: '{a0}'"))

print(f"Total oddities found: {len(oddities)}")
for o in oddities:
    print(f"Set {(o[0]-1)//20 + 1}, Word {o[0]} ({o[1]}): {o[2]}")
