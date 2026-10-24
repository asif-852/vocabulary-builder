import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)[:200]

print("Scanning for broken Bengali spacing (orphan kars or split words)...")

# Orphan kars followed by space or preceded by space
broken_space_pattern = re.compile(r'[\u09BE-\u09CC]\s+[\u0985-\u09B9\u09CE\u09A4]')

found = []
for d in data:
    for i, ex in enumerate(d['examples']):
        bn = ex['bn']
        if broken_space_pattern.search(bn):
            found.append((d['id'], d['word'], f"ex{i+1}", bn))

print(f"Total found: {len(found)}")
for f in found:
    print(f"[{f[0]}] {f[1]} ({f[2]}): {f[3]}")
