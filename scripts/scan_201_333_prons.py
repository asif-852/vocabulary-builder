import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)[200:]

print("Scanning words 201 to 333 in gre333.json...")
issues_201_333 = []
for i, d in enumerate(data):
    w = d['word']
    pos = d['partOfSpeech']
    pen = d.get('pronunciationEn', '')
    pbn = d.get('pronunciationBn', '')
    
    is_missing = not pen or not pbn
    has_eng_in_bn = bool(re.search(r'[a-zA-Z]', pbn))
    is_all_caps = pen.isupper() and len(pen) > 4
    
    if is_missing or has_eng_in_bn or is_all_caps:
        issues_201_333.append((201 + i, w, pos, pen, pbn))

print(f"Total words with broken/missing pronunciation in words 201-333: {len(issues_201_333)}")
for iss in issues_201_333[:20]:
    print(f"[{iss[0]}] {iss[1]} ({iss[2]}): EN='{iss[3]}' | BN='{iss[4]}'")
