import json
import re
import sys
import string

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)[:200]

bengali_punctuation = "।?!,;:'\"-–—()[]{}’‘" + string.punctuation
valid_single_letter_words = {'ও', 'এ', 'বা'}

single_char_splits = []

for d in data:
    for i, ex in enumerate(d['examples']):
        bn = ex['bn']
        tokens = bn.split()
        for idx, tok in enumerate(tokens):
            clean_tok = tok.strip(bengali_punctuation)
            if len(clean_tok) == 1 and '\u0980' <= clean_tok <= '\u09FF':
                if clean_tok not in valid_single_letter_words:
                    single_char_splits.append((d['id'], d['word'], f"ex{i+1}", tokens[max(0, idx-1):idx+2], bn))

print(f"Single char splits in examples: {len(single_char_splits)}")
for s in single_char_splits:
    print(s)
