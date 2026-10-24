import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)[:200]

print("=== CHECKING ALL 200 WORDS IN SETS 1-10 ===")
# Let's check for any anomalies in pron_en and pron_bn
for d in data:
    en = d.get('pronunciationEn', '')
    bn = d.get('pronunciationBn', '')
    w = d['word']
    pos = d['partOfSpeech']
    
    # Are syllables matched? Count hyphens in en vs bn
    h_en = en.count('-')
    h_bn = bn.count('-')
    
    if h_en != h_bn:
        print(f"[{d['id']}] {w} ({pos}): HYPHEN MISMATCH -> EN({h_en})='{en}' vs BN({h_bn})='{bn}'")
