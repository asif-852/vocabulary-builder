import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

datasets = [
    ('GRE 333', 'src/data/gre333.json'),
    ('WordSmart 1', 'src/data/wordsmart1.json'),
    ('WordSmart 2', 'src/data/wordsmart2.json'),
]

for name, path in datasets:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print(f"\n=== VERIFYING {name} ({len(data)} words) ===")
    
    eng_in_bn = []
    missing_en = []
    missing_bn = []
    raw_caps_en = []
    
    for i, d in enumerate(data):
        w = d['word']
        pen = d.get('pronunciationEn', '').strip()
        pbn = d.get('pronunciationBn', '').strip()
        
        if not pen:
            missing_en.append((i+1, w))
        elif pen.isupper() and len(pen) > 4:
            raw_caps_en.append((i+1, w, pen))
            
        if not pbn:
            missing_bn.append((i+1, w))
        elif re.search(r'[a-zA-Z]', pbn):
            eng_in_bn.append((i+1, w, pbn))
            
    print(f"  - English characters inside Bangla pronunciation: {len(eng_in_bn)}")
    print(f"  - Missing English pronunciation: {len(missing_en)}")
    print(f"  - Raw all-caps unformatted English pronunciation: {len(raw_caps_en)}")
    print(f"  - Missing Bangla pronunciation: {len(missing_bn)}")
    
    if eng_in_bn:
        print(f"    Examples: {eng_in_bn[:3]}")
    if raw_caps_en:
        print(f"    Examples: {raw_caps_en[:3]}")
