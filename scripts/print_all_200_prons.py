import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    gre = json.load(f)[:200]

for d in gre:
    en_p = d.get('pronunciationEn')
    bn_p = d.get('pronunciationBn')
    print(f"{d['id']} {d['word']} ({d['partOfSpeech']}): {en_p} | {bn_p}")
