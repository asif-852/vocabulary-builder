import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)[:200]

print("=== SETS 1 TO 10 PRONUNCIATIONS REVIEW ===")
for d in data:
    en = d['pronunciationEn']
    bn = d['pronunciationBn']
    w = d['word']
    
    # Are there any single syllable words where en is identical to word?
    if en.upper() == w.upper():
        print(f"IDENTICAL TO WORD: [{d['id']}] {w} -> EN='{en}' | BN='{bn}'")
