# -*- coding: utf-8 -*-
"""
Applies hand-curated Mode 3 data across Sets 11 to 17 (Words 201 to 333) to gre333.json.
"""

import json
import re
import sys
import os

sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

from scripts.curate_mode3_set11 import SET_11_CURATED
from scripts.curate_mode3_set12 import SET_12_CURATED
from scripts.curate_mode3_set13 import SET_13_CURATED
from scripts.curate_mode3_set14 import SET_14_CURATED
from scripts.curate_mode3_set15 import SET_15_CURATED
from scripts.curate_mode3_set16 import SET_16_CURATED
from scripts.curate_mode3_set17 import SET_17_CURATED

all_curated = {}
for s in [SET_11_CURATED, SET_12_CURATED, SET_13_CURATED, SET_14_CURATED, SET_15_CURATED, SET_16_CURATED, SET_17_CURATED]:
    all_curated.update(s)

print(f"Total curated entries: {len(all_curated)}")
assert len(all_curated) == 133, f"Expected 133 words, found {len(all_curated)}"

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

for idx in range(201, 334):
    target = corpus[idx - 1]
    word = target['word']
    assert idx in all_curated, f"Missing data for Word {idx} ({word})"
    
    entry = all_curated[idx]
    opts = entry['options']
    assert len(opts) == 6, f"Word {idx} ({word}) does not have 6 options"
    
    true_syns = [o for o in opts if o['isSynonym']]
    distractors = [o for o in opts if not o['isSynonym']]
    assert len(true_syns) == 3, f"Word {idx} ({word}) expected 3 true synonyms, got {len(true_syns)}"
    assert len(distractors) == 3, f"Word {idx} ({word}) expected 3 distractors, got {len(distractors)}"
    
    # Check no duplicate words among options
    opt_words = [o['word'].lower() for o in opts]
    assert len(set(opt_words)) == 6, f"Word {idx} ({word}) has duplicate option words: {opt_words}"
    
    # Check Bengali meanings
    for o in opts:
        bn = o.get('meaningBn', '').strip()
        assert bn, f"Word {idx} ({word}): option '{o['word']}' has empty Bengali meaning"
        assert not re.search(r'[a-zA-Z]', bn), f"Word {idx} ({word}): option '{o['word']}' contains English in Bengali: {bn}"
        assert 'বিপরীত' not in bn and 'placeholder' not in bn.lower(), f"Word {idx} ({word}): placeholder in {o['word']}"
        
    target['multiSynonyms'] = entry

with open('src/data/gre333.json', 'w', encoding='utf-8') as f:
    json.dump(corpus, f, ensure_ascii=False, indent=2)

print("Successfully applied hand-curated Mode 3 data to Sets 11-17 in gre333.json!")
