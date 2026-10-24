# -*- coding: utf-8 -*-
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

fixes = {
    'সমস্যাাবহুল বা সেহজনক': 'সমস্যাবহুল বা সন্দেহজনক',
    'সমস্যাা': 'সমস্যা',
    'সেহজনক': 'সন্দেহজনক',
    'সেহপ্রবণ': 'সন্দেহপ্রবণ',
    'সেহ': 'সন্দেহ',
}

changes = 0
for idx, w in enumerate(corpus):
    orig = w['meaningBn']
    new_bn = orig
    for k, v in fixes.items():
        if k in new_bn:
            new_bn = new_bn.replace(k, v)
    if new_bn != orig:
        print(f"Fixing [{w['word']}]: {orig} -> {new_bn}")
        w['meaningBn'] = new_bn
        changes += 1

# Check for double vowel signs across all entries
vowel_pattern = re.compile(r'[\u09BE\u09BF\u09C0\u09C1\u09C2\u09C7\u09C8\u09CB\u09CC]{2,}')
for idx, w in enumerate(corpus):
    matches = vowel_pattern.findall(w['meaningBn'])
    if matches:
        print(f"Warning: double vowel in [{w['word']}]: {w['meaningBn']}")

if changes > 0:
    with open('src/data/gre333.json', 'w', encoding='utf-8') as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)
    print(f"Updated {changes} entries in src/data/gre333.json")
else:
    print("No fixes needed.")
