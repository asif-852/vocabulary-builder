import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

for filename in ['src/data/wordsmart1.json', 'src/data/wordsmart2.json']:
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Checking {filename} ({len(data)} words)...")
    count = 0
    for idx, w in enumerate(data):
        m = w.get('meaningEn', '')
        if any(k in m for k in ['; ;', ';;', ' - ', '- c.b', '- robert', '- bruce']):
            print(f"  [{idx+1}] {w['word']}: {m}")
            count += 1
    print(f"  Total issues in {filename}: {count}")
