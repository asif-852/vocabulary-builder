import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)[:200]

for i, d in enumerate(data):
    w = d['word']
    pos = d['partOfSpeech']
    pen = d.get('pronunciationEn')
    pbn = d.get('pronunciationBn')
    
    # Check if either is None or empty
    if not pen or not pbn:
        print(f"MISSING: {i+1} {w} ({pos}): pen={pen}, pbn={pbn}")
        
    # Check if pbn has English characters
    import re
    if re.search(r'[a-zA-Z]', pbn):
        print(f"ENG IN PBN: {i+1} {w} ({pos}): {pbn}")
        
    # Check if pen has Bengali characters
    if re.search(r'[\u0980-\u09FF]', pen):
        print(f"BN IN PEN: {i+1} {w} ({pos}): {pen}")

print("Done scanning 1 to 200.")
