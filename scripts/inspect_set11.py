# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

def print_set(set_num):
    start = (set_num - 1) * 20
    end = min(set_num * 20, len(corpus))
    words = corpus[start:end]
    print(f"==================================================")
    print(f"                SET {set_num} (Words {start+1} to {end})")
    print(f"==================================================")
    for idx, w in enumerate(words, start + 1):
        print(f"[{idx}] {w['word']} ({w['partOfSpeech']})")
        print(f"    Pron: {w.get('pronunciationEn')} | {w.get('pronunciationBn')}")
        print(f"    Meaning (Bn): {w.get('meaningBn')}")
        print(f"    Meaning (En): {w.get('meaningEn')}")
        print(f"    Synonyms: {', '.join(w.get('synonyms', []))}")
        print(f"    Antonyms: {', '.join(w.get('antonyms', []))}")
        exs = w.get('examples', [])
        for i, ex in enumerate(exs, 1):
            print(f"    Ex {i} (En): {ex.get('en')}")
            print(f"    Ex {i} (Bn): {ex.get('bn')}")
        print()

print_set(11)
