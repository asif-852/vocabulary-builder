# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

for s in range(1, 11):
    start = (s - 1) * 20
    end = s * 20
    words = corpus[start:end]
    print(f"=== SET {s} (Words {start+1} to {end}) ===")
    for idx, w in enumerate(words, start + 1):
        print(f"{idx:3d}. {w['word']:16} ({w['partOfSpeech']}) [{w['meaningBn']}]")
        print(f"     Syn: {', '.join(w.get('synonyms', []))}")
        print(f"     Ant: {', '.join(w.get('antonyms', []))}")
    print()
