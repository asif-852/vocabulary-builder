import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)[:200]

print("=== CHECKING ALL VERBS ===")
verbs = [d for d in data if d['partOfSpeech'] == 'verb']
for v in verbs:
    w = v['word']
    ex1 = v['examples'][0]['en']
    ex2 = v['examples'][1]['en']
    # If the word itself appears as a noun (e.g. 'a <word>', 'the <word>', 'his <word>')
    print(f"[{v['id']}] {w}:")
    print(f"   1: {ex1}")
    print(f"   2: {ex2}")
