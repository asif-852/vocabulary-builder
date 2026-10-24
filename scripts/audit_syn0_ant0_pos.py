# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

corpus_map = {w['word'].lower(): w for w in corpus}

print("Checking Sets 1 to 10 (Words 1 to 200):")
print("1. Words where syn[0] has spaces or punctuation")
print("2. Words where ant[0] has spaces or punctuation")
print("3. Words where syn[0] or ant[0] is in corpus but has different POS")

issues = []
for idx in range(1, 201):
    w = corpus[idx - 1]
    word = w['word']
    pos = w['partOfSpeech']
    s0 = w['synonyms'][0]
    a0 = w['antonyms'][0]
    
    if ' ' in s0 or ',' in s0 or '-' in s0:
        issues.append(f"Word {idx} ({word}): syn[0] is '{s0}'")
    if ' ' in a0 or ',' in a0 or '-' in a0:
        issues.append(f"Word {idx} ({word}): ant[0] is '{a0}'")
        
    if s0.lower() in corpus_map:
        c_pos = corpus_map[s0.lower()]['partOfSpeech']
        if c_pos != pos:
            issues.append(f"Word {idx} ({word}, {pos}): syn[0] '{s0}' in corpus has POS '{c_pos}'")
            
    if a0.lower() in corpus_map:
        c_pos = corpus_map[a0.lower()]['partOfSpeech']
        if c_pos != pos:
            issues.append(f"Word {idx} ({word}, {pos}): ant[0] '{a0}' in corpus has POS '{c_pos}'")

print(f"Total issues found: {len(issues)}")
for i in issues:
    print("  -", i)
