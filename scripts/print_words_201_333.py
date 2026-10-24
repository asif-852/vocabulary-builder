import json
import sys

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

with open('scripts/words_201_333.txt', 'w', encoding='utf-8') as f:
    for idx in range(200, 333):
        w = d[idx]
        f.write(f"[{w['indexInSource']}] Set {w['setNumber']} | {w['word']} ({w['partOfSpeech']})\n")
        f.write(f"   EN: {w['meaningEn']}\n")
        f.write(f"   BN: {w['meaningBn']}\n")
        f.write(f"   Syns: {', '.join(w.get('synonyms', []))}\n")
        f.write(f"   Ants: {', '.join(w.get('antonyms', []))}\n\n")

print("Wrote words_201_333.txt successfully")
