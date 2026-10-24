import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)[:200]

print("=== CHECKING ALL ADJECTIVES ===")
adjs = [d for d in data if d['partOfSpeech'] == 'adjective']
for a in adjs:
    w = a['word']
    ex1 = a['examples'][0]['en']
    ex2 = a['examples'][1]['en']
    # If used without modifying a noun or as a predicate adjective (is/was/seems/remains <word>)
    # Let's inspect
    print(f"[{a['id']}] {w}:")
    print(f"   1: {ex1}")
    print(f"   2: {ex2}")
