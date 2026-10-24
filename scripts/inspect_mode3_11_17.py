# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
data = json.load(open('src/data/gre333.json', encoding='utf-8'))

for w in data[200:333]:
    opts = w['multiSynonyms']['options']
    syns = [o['word'] for o in opts if o['isSynonym']]
    dists = [o['word'] for o in opts if not o['isSynonym']]
    print(f"Set {w['setNumber']} - {w['word']}:")
    print(f"   Synonyms: {syns}")
    print(f"   Distractors: {dists}")
