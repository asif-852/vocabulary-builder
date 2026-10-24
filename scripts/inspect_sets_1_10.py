import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)[:200]

print(f"Loaded {len(data)} items.")

missing_word_in_ex = []
corrupt_chars = []
placeholder_ants = []
pos_mismatches = []

corrupt_regex = re.compile(r'([া-ৌ])\1|সতক|সৌন্দয|পদমযাদা|মিিত|দ্ব্যথ|িমুখী|ংং')

for d in data:
    wid = d['id']
    w = d['word'].lower()
    pos = d.get('partOfSpeech', '')
    
    # Check examples
    for i, ex in enumerate(d.get('examples', [])):
        en = ex.get('en', '')
        bn = ex.get('bn', '')
        if w not in en.lower():
            missing_word_in_ex.append((wid, w, i+1, en))
        if corrupt_regex.search(bn):
            corrupt_chars.append((wid, w, f"ex{i+1}_bn", corrupt_regex.findall(bn), bn))
            
    # Check meaningBn
    mbn = d.get('meaningBn', '')
    if corrupt_regex.search(mbn):
        corrupt_chars.append((wid, w, "meaningBn", corrupt_regex.findall(mbn), mbn))
        
    # Check antonyms
    for ant in d.get('antonyms', []):
        if 'ant-' in ant or ant.strip() == '':
            placeholder_ants.append((wid, w, ant))
            
print(f"Missing target word in examples: {len(missing_word_in_ex)}")
for m in missing_word_in_ex[:5]:
    print("  ", m)

print(f"Corrupt chars found: {len(corrupt_chars)}")
for c in corrupt_chars[:10]:
    print("  ", c)

print(f"Placeholder antonyms: {len(placeholder_ants)}")
for p in placeholder_ants[:5]:
    print("  ", p)
