# -*- coding: utf-8 -*-
"""
Applies the upgraded 501-standard Mode 2 Sentence Completion questions
to the first 200 words (Sets 1 to 10) in src/data/gre333.json.
"""

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('scripts')

from mode2_data_sets_1_to_5 import MODE2_SETS_1_TO_5
from mode2_data_sets_6_to_10 import MODE2_SETS_6_TO_10

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    gre_data = json.load(f)

all_mode2 = {}
all_mode2.update(MODE2_SETS_1_TO_5)
all_mode2.update(MODE2_SETS_6_TO_10)

print(f"Applying {len(all_mode2)} Mode 2 questions to gre333.json...")

for idx in range(1, 201):
    entry = all_mode2[idx]
    target_item = gre_data[idx - 1]
    
    # Ensure word matches
    expected_word = target_item['word']
    chosen_opt = entry['options'][entry['correctIndex']]
    assert chosen_opt.lower() == expected_word.lower(), f"Mismatch at {idx}: {chosen_opt} vs {expected_word}"
    
    # Update sentenceCompletion field
    target_item['sentenceCompletion'] = {
        'sentenceWithBlank': entry['sentenceWithBlank'],
        'options': entry['options'],
        'correctIndex': entry['correctIndex'],
        'optionMeaningsBn': entry['optionMeaningsBn'],
        'explanationEn': entry['explanationEn'],
        'sentenceTranslationBn': entry['sentenceTranslationBn']
    }

# Save updated gre333.json
with open('src/data/gre333.json', 'w', encoding='utf-8') as f:
    json.dump(gre_data, f, ensure_ascii=False, indent=2)

print("SUCCESS: Updated first 200 words (Sets 1 to 10) in src/data/gre333.json!")
