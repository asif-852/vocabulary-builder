# -*- coding: utf-8 -*-
"""
Apply Mode 2 (Sentence Completion) for Sets 11 to 17 (Words 201 to 333) into gre333.json.
"""

import json
import sys
import os

sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

from scripts.mode2_set11 import SET_11
from scripts.mode2_set12 import SET_12
from scripts.mode2_set13 import SET_13
from scripts.mode2_set14 import SET_14
from scripts.mode2_set15 import SET_15
from scripts.mode2_set16 import SET_16
from scripts.mode2_set17 import SET_17

all_sets = {}
for s in [SET_11, SET_12, SET_13, SET_14, SET_15, SET_16, SET_17]:
    all_sets.update(s)

print(f"Total Mode 2 questions authored: {len(all_sets)}")
assert len(all_sets) == 133, f"Expected 133 questions, got {len(all_sets)}"

path = 'src/data/gre333.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Fix word 292 typo if present
for w in data:
    if w.get('word') == 'Secrete':
        if 'নিঃঃসরণ' in w.get('meaningBn', ''):
            w['meaningBn'] = w['meaningBn'].replace('নিঃঃসরণ', 'নিঃসরণ')
            print("Fixed typo in Secrete meaningBn")
    if w.get('word') == 'Sage':
        if w.get('meaningBn') == 'মহাজ্ঞানী ব্যক্তি':
            w['meaningBn'] = 'বিজ্ঞ বা প্রাজ্ঞ ব্যক্তি'
            print("Refined Sage meaningBn to reflect adjective/noun nuance")

applied_count = 0
for idx in range(200, 333):
    word_num = idx + 1
    item = data[idx]
    headword = item['word'].strip()
    
    assert word_num in all_sets, f"Missing question for word {word_num}: {headword}"
    q = all_sets[word_num]
    
    # Validation checks
    assert 'sentenceWithBlank' in q and '_____' in q['sentenceWithBlank'], f"Bad blank in {headword}"
    assert 'options' in q and len(q['options']) == 5, f"Options length not 5 in {headword}"
    assert 'correctIndex' in q and 0 <= q['correctIndex'] < 5, f"Bad correctIndex in {headword}"
    
    correct_opt = q['options'][q['correctIndex']].strip()
    assert correct_opt.lower() == headword.lower(), f"Option mismatch for {headword}: correct option is {correct_opt}"
    
    assert 'optionMeaningsBn' in q and len(q['optionMeaningsBn']) == 5, f"Bad optionMeaningsBn in {headword}"
    for bn in q['optionMeaningsBn']:
        assert bn and len(bn.strip()) > 0, f"Empty bn meaning in {headword}"
        
    assert 'explanationEn' in q and len(q['explanationEn'].strip()) > 0, f"Missing explanationEn in {headword}"
    assert 'sentenceTranslationBn' in q and len(q['sentenceTranslationBn'].strip()) > 0, f"Missing sentenceTranslationBn in {headword}"
    
    item['sentenceCompletion'] = q
    applied_count += 1

print(f"Successfully applied {applied_count} questions!")

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Saved updated gre333.json successfully!")
