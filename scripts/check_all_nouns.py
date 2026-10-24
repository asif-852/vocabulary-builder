import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)[:200]

print("=== CHECKING ALL NOUNS ===")
nouns = [d for d in data if d['partOfSpeech'] == 'noun']
for n in nouns:
    w = n['word']
    ex1 = n['examples'][0]['en']
    ex2 = n['examples'][1]['en']
    print(f"[{n['id']}] {w}:")
    print(f"   1: {ex1}")
    print(f"   2: {ex2}")
