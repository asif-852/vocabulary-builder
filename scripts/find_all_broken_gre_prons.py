import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    gre = json.load(f)

print(f"Total GRE words: {len(gre)}")

broken_prons = []
for i, d in enumerate(gre):
    en = d.get('pronunciationEn', '')
    bn = d.get('pronunciationBn', '')
    w = d['word']
    
    # check if bn has English letters
    has_eng_in_bn = bool(re.search(r'[a-zA-Z]', bn))
    # check if en is just the capitalized word (for multi-syllable words)
    is_raw_caps = (en == w.upper() and len(w) > 4)
    # check if bn is just the word
    is_word_in_bn = (bn.lower() == w.lower())
    
    if has_eng_in_bn or is_raw_caps or is_word_in_bn:
        broken_prons.append((i+1, w, d['partOfSpeech'], en, bn))

print(f"Total broken pronunciations across all 333 GRE words: {len(broken_prons)}")
for b in broken_prons:
    print(f"[{b[0]}] {b[1]} ({b[2]}): EN='{b[3]}' | BN='{b[4]}'")
