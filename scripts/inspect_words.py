# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
data = json.load(open('src/data/gre333.json', encoding='utf-8'))

for i, w in enumerate(data[280:333], start=281):
    print(f"{i}: {w['word']} ({w.get('partOfSpeech', '')}) -> {w.get('meaningEn', '')} | {w.get('meaningBn', '')}")
