# -*- coding: utf-8 -*-
import json

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

words_11_17 = corpus[200:333]
with open('scripts/words_11_17_utf8.txt', 'w', encoding='utf-8') as out:
    for idx, w in enumerate(words_11_17, 201):
        s0 = w['synonyms'][0] if w.get('synonyms') else ''
        a0 = w['antonyms'][0] if w.get('antonyms') else ''
        out.write(f"[{idx}] {w['word']} ({w['partOfSpeech']})\n")
        out.write(f"    meanEn: {w.get('meaningEn')}\n")
        out.write(f"    meanBn: {w.get('meaningBn')}\n")
        out.write(f"    syn[0]: '{s0}' | all syns: {w.get('synonyms')}\n")
        out.write(f"    ant[0]: '{a0}' | all ants: {w.get('antonyms')}\n\n")
print("Done writing scripts/words_11_17_utf8.txt")
