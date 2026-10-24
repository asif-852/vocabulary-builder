# -*- coding: utf-8 -*-
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

violations = []
distractor_counts = {}

for idx in range(1, 334):
    w = corpus[idx - 1]
    word = w['word']
    pos = w['partOfSpeech']
    ms = w.get('multiSynonyms')
    
    if not ms or 'options' not in ms:
        violations.append(f"Word {idx} ({word}): Missing multiSynonyms")
        continue
        
    opts = ms['options']
    if len(opts) != 6:
        violations.append(f"Word {idx} ({word}): Expected 6 options, got {len(opts)}")
        continue
        
    true_syns = [o for o in opts if o['isSynonym']]
    false_dist = [o for o in opts if not o['isSynonym']]
    
    if len(true_syns) != 3:
        violations.append(f"Word {idx} ({word}): Expected 3 true synonyms, got {len(true_syns)}")
    if len(false_dist) != 3:
        violations.append(f"Word {idx} ({word}): Expected 3 distractors, got {len(false_dist)}")
        
    # Check for relations
    t_syns = set(s.lower() for s in w.get('synonyms', []))
    t_syns.add(word.lower())
    t_ants = set(a.lower() for a in w.get('antonyms', []))
    
    for d in false_dist:
        d_word = d['word']
        d_lower = d_word.lower()
        distractor_counts[d_word] = distractor_counts.get(d_word, 0) + 1
        
        if d_lower in t_syns:
            violations.append(f"Word {idx} ({word}): Distractor '{d_word}' is a synonym!")
        if d_lower in t_ants:
            violations.append(f"Word {idx} ({word}): Distractor '{d_word}' is an antonym!")
        if d_lower in {'abate', 'aberrant'}:
            violations.append(f"Word {idx} ({word}): Distractor '{d_word}' is an overused banned word!")
            
    # Check Bengali meanings
    for o in opts:
        bn = o.get('meaningBn', '').strip()
        if not bn:
            violations.append(f"Word {idx} ({word}): Option '{o['word']}' has empty Bengali meaning")
        if re.search(r'[a-zA-Z]', bn):
            violations.append(f"Word {idx} ({word}): Option '{o['word']}' has English characters in Bengali meaning: {bn}")
        if 'বিপরীত' in bn or 'placeholder' in bn.lower():
            violations.append(f"Word {idx} ({word}): Option '{o['word']}' has placeholder meaning: {bn}")

print(f"Total violations found: {len(violations)}")
if violations:
    for v in violations[:15]:
        print("  -", v)
else:
    print("ALL 333 WORDS PERFECTLY PASS MODE 3 RIGOROUS VERIFICATION!")
    print(f"Total unique distractors used: {len(distractor_counts)}")
    print(f"Max distractor reuse count: {max(distractor_counts.values())}")
