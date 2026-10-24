import fitz
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Let's check overlap between GRE 333 and WordSmart 1 & 2
with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    gre = json.load(f)

with open('src/data/wordsmart1.json', 'r', encoding='utf-8') as f:
    ws1 = json.load(f)

with open('src/data/wordsmart2.json', 'r', encoding='utf-8') as f:
    ws2 = json.load(f)

ws_map = {}
for w in ws1:
    ws_map[w['word'].lower()] = ('ws1', w)
for w in ws2:
    ws_map[w['word'].lower()] = ('ws2', w)

overlap = 0
for d in gre[:200]:
    if d['word'].lower() in ws_map:
        overlap += 1

print(f"Overlap in first 200 GRE words with WordSmart: {overlap}/200")
