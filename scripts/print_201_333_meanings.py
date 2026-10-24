import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

for i in range(200, 333):
    w = corpus[i]
    print(f"[{i+1}] {w['word']} ({w['partOfSpeech']}): {w['meaningEn']}")
