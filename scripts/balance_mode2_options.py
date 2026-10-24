# -*- coding: utf-8 -*-
"""
Balance the correctIndex distribution for Mode 2 across Sets 11 to 17 (Words 201 to 333).
Distributes correctIndex evenly across 0, 1, 2, 3, 4 while keeping options and optionMeaningsBn in lockstep.
"""

import json
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

path = 'src/data/gre333.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Cycle pattern for balanced distribution
pattern = [0, 2, 4, 1, 3]

for i, idx in enumerate(range(200, 333)):
    word_num = idx + 1
    item = data[idx]
    sc = item['sentenceCompletion']
    
    old_c_idx = sc['correctIndex']
    target_c_idx = pattern[i % len(pattern)]
    
    pairs = list(zip(sc['options'], sc['optionMeaningsBn']))
    correct_pair = pairs[old_c_idx]
    distractor_pairs = [p for j, p in enumerate(pairs) if j != old_c_idx]
    
    # Place correct_pair at target_c_idx
    new_pairs = distractor_pairs[:target_c_idx] + [correct_pair] + distractor_pairs[target_c_idx:]
    
    new_options = [p[0] for p in new_pairs]
    new_meanings = [p[1] for p in new_pairs]
    
    assert new_options[target_c_idx].lower() == item['word'].lower()
    assert len(new_options) == 5
    assert len(new_meanings) == 5
    
    sc['options'] = new_options
    sc['optionMeaningsBn'] = new_meanings
    sc['correctIndex'] = target_c_idx

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Balanced options successfully!")
