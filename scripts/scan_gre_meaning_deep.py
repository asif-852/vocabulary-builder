import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for idx, w in enumerate(data):
    m = w['meaningEn']
    # Check for author names, citations, semicolons with spaces, parentheses
    if any(k in m.lower() for k in ['burton', 'bliven', 'diamant', 'davis', 'woolf', 'scott', 'butler', 'nordhoff', 'quote', 'author']):
        print(f"Citation found: [{idx+1}] {w['word']}: {m}")
    elif ';' in m and len(m.split(';')) > 3:
        print(f"Many semicolons: [{idx+1}] {w['word']}: {m}")
    elif m.startswith('(') and ')' in m:
        print(f"Parenthetical start: [{idx+1}] {w['word']}: {m}")
