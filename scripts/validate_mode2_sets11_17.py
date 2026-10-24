# -*- coding: utf-8 -*-
"""
Validation script for Mode 2 (Sentence Completion) - Sets 11 to 17 (Words 201 to 333).
"""

import json
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total words in gre333.json: {len(data)}")

subset = data[200:333]
assert len(subset) == 133, f"Expected 133 words, found {len(subset)}"

correct_index_counts = Counter()
pos_counts = Counter()

for i, item in enumerate(subset, start=201):
    w = item['word']
    pos = item.get('partOfSpeech', '')
    pos_counts[pos] += 1
    
    assert 'sentenceCompletion' in item, f"Word {i} ({w}) missing sentenceCompletion!"
    sc = item['sentenceCompletion']
    
    # Check sentence
    sent = sc.get('sentenceWithBlank', '')
    assert '_____' in sent, f"Word {i} ({w}) missing '_____' in sentenceWithBlank: {sent}"
    assert len(sent.split('_____')) == 2, f"Word {i} ({w}) has multiple blanks!"
    assert len(sent) > 50, f"Word {i} ({w}) sentence seems too short ({len(sent)} chars)"
    
    # Check options
    opts = sc.get('options', [])
    assert len(opts) == 5, f"Word {i} ({w}) does not have exactly 5 options: {opts}"
    assert len(set(opts)) == 5, f"Word {i} ({w}) has duplicate options: {opts}"
    
    # Check correctIndex
    c_idx = sc.get('correctIndex')
    assert isinstance(c_idx, int) and 0 <= c_idx < 5, f"Word {i} ({w}) invalid correctIndex: {c_idx}"
    correct_index_counts[c_idx] += 1
    
    # Check that correct option matches headword
    assert opts[c_idx].lower() == w.lower(), f"Word {i} ({w}) correct option '{opts[c_idx]}' does not match headword"
    
    # Check optionMeaningsBn
    meanings = sc.get('optionMeaningsBn', [])
    assert len(meanings) == 5, f"Word {i} ({w}) does not have 5 Bengali meanings: {meanings}"
    for m in meanings:
        assert isinstance(m, str) and len(m.strip()) > 0, f"Word {i} ({w}) empty Bengali option meaning"
        
    # Check explanationEn
    exp = sc.get('explanationEn', '')
    assert isinstance(exp, str) and len(exp.strip()) > 10, f"Word {i} ({w}) invalid explanationEn: {exp}"
    
    # Check sentenceTranslationBn
    trans = sc.get('sentenceTranslationBn', '')
    assert isinstance(trans, str) and len(trans.strip()) > 15, f"Word {i} ({w}) invalid sentenceTranslationBn: {trans}"

print("All 133 words in Sets 11-17 passed rigorous schema, structure, and content validation!")
print(f"Correct index distribution across the 133 questions:")
for idx in sorted(correct_index_counts.keys()):
    print(f"  Option {idx}: {correct_index_counts[idx]} times ({correct_index_counts[idx]/133*100:.1f}%)")

print("Parts of speech represented:")
for pos, count in pos_counts.most_common():
    print(f"  {pos}: {count}")
