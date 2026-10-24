import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)[80:150]

for d in data:
    if d['partOfSpeech'] == 'adjective':
        print(f"[{d['id']}] {d['word']}:")
        print(f"   1: {d['examples'][0]['en']}")
        print(f"   2: {d['examples'][1]['en']}")
