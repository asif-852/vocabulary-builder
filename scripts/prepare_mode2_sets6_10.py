import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    gre = json.load(f)

for i in range(100, 200):
    item = gre[i]
    print(f"{item['id']}: {item['word']} ({item['partOfSpeech']}) - {item['meaningEn']} | {item['meaningBn']}")
