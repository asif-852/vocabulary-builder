import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', encoding='utf-8') as f:
    gre = json.load(f)

set1_10 = [w for w in gre if w['setNumber'] <= 10]

# Inspect how sentences are formed in GRE 333
for s_idx in range(1, 11):
    words = [w for w in set1_10 if w['setNumber'] == s_idx]
    print(f"\n================ SET {s_idx} ================")
    for w in words[:3]:
        print(f"#{w['indexInSource']} {w['word']} ({w['partOfSpeech']})")
        print(f"  Meaning EN: {w['meaningEn']}")
        print(f"  Meaning BN: {w['meaningBn']}")
        print(f"  Synonyms: {', '.join(w['synonyms'])}")
        print(f"  Antonyms: {', '.join(w['antonyms'])}")
        print(f"  Ex1: {w['examples'][0]['en']}")
        print(f"       {w['examples'][0]['bn']}")
        print(f"  Ex2: {w['examples'][1]['en']}")
        print(f"       {w['examples'][1]['bn']}")
