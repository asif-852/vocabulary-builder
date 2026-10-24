import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for idx in range(200, 333):
    w = d[idx]
    i = w['indexInSource']
    word = w['word']
    pos = w['partOfSpeech']
    men = w['meaningEn']
    
    if pos == 'noun':
        if men.startswith('Characterized') or men.startswith('Tending to') or men.startswith('Having '):
            print(f"[{i}] {word} (noun): starts with adj participle: {men}")
