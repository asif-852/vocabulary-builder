import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    gre = json.load(f)

print(f"Total GRE words: {len(gre)}")

# Let's inspect words 1-200 and 201-333
for i, d in enumerate(gre):
    en = d.get('pronunciationEn', '')
    bn = d.get('pronunciationBn', '')
    # Check if English letters in bn
    has_eng_in_bn = bool(re.search(r'[a-zA-Z]', bn)) if bn else False
    # Check if bn is missing or equals en
    is_missing_bn = not bn or bn == en
    # Check if en has non-phonetic or raw word or ipa
    if has_eng_in_bn or is_missing_bn or not en:
        print(f"[{d['id']}] {d['word']}: EN='{en}' | BN='{bn}' | eng_in_bn={has_eng_in_bn} missing={is_missing_bn}")
