# -*- coding: utf-8 -*-
"""
Validation script for Mode 2 Sentence Completion across Sets 1 to 10 (Words 1 to 200).
"""

import json
import re
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

print(f"Total Mode 2 questions to validate: {len(all_mode2)}")
assert len(all_mode2) == 200, f"Expected 200 entries, found {len(all_mode2)}"

errors = []
english_char_pattern = re.compile(r'[a-zA-Z]')

for idx in range(1, 201):
    if idx not in all_mode2:
        errors.append(f"Missing index {idx}")
        continue
    
    q = all_mode2[idx]
    expected_word = gre_data[idx - 1]['word']
    
    # Check blank
    if q['sentenceWithBlank'].count('_____') != 1:
        errors.append(f"[{idx} {expected_word}] sentenceWithBlank does not have exactly one '_____': {q['sentenceWithBlank']}")
    
    # Check sentence length (should be substantial, > 15 words)
    words_count = len(q['sentenceWithBlank'].split())
    if words_count < 15:
        errors.append(f"[{idx} {expected_word}] sentence too short ({words_count} words): {q['sentenceWithBlank']}")
        
    # Check options count
    if len(q['options']) != 5:
        errors.append(f"[{idx} {expected_word}] options count is {len(q['options'])} (expected 5)")
        
    # Check optionMeaningsBn count
    if len(q['optionMeaningsBn']) != 5:
        errors.append(f"[{idx} {expected_word}] optionMeaningsBn count is {len(q['optionMeaningsBn'])} (expected 5)")
        
    # Check correctIndex
    c_idx = q['correctIndex']
    if not (0 <= c_idx < 5):
        errors.append(f"[{idx} {expected_word}] invalid correctIndex: {c_idx}")
    else:
        chosen_opt = q['options'][c_idx]
        if chosen_opt.lower() != expected_word.lower():
            errors.append(f"[{idx} {expected_word}] correctIndex points to '{chosen_opt}', expected '{expected_word}'")
            
    # Check Title casing of options
    for opt in q['options']:
        if not opt[0].isupper():
            errors.append(f"[{idx} {expected_word}] option '{opt}' is not capitalized")
            
    # Check Bengali option meanings for English characters
    for m in q['optionMeaningsBn']:
        if english_char_pattern.search(m):
            errors.append(f"[{idx} {expected_word}] English characters in optionMeaningsBn: '{m}'")
            
    # Check Bengali sentence translation
    if not q['sentenceTranslationBn'] or len(q['sentenceTranslationBn'].strip()) < 10:
        errors.append(f"[{idx} {expected_word}] empty or short sentenceTranslationBn")
    elif english_char_pattern.search(q['sentenceTranslationBn']):
        errors.append(f"[{idx} {expected_word}] English characters in sentenceTranslationBn: '{q['sentenceTranslationBn']}'")
        
    # Check explanationEn
    if not q['explanationEn'] or len(q['explanationEn'].strip()) < 10:
        errors.append(f"[{idx} {expected_word}] empty or short explanationEn")

if errors:
    print(f"Validation FAILED with {len(errors)} errors:")
    for err in errors[:25]:
        print("  -", err)
    if len(errors) > 25:
        print(f"  ... and {len(errors) - 25} more errors")
    sys.exit(1)
else:
    print("SUCCESS: All 200 Mode 2 Sentence Completion questions strictly meet all 501-standard requirements!")
