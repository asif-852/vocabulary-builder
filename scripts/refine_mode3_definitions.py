# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

# Update Belie's meaningBn in corpus
for w in corpus:
    if w['word'] == 'Belie':
        w['meaningBn'] = 'ভুল ধারণা সৃষ্টি করা বা আসল রূপ গোপন রাখা'

# Update options in multiSynonyms across all 200 words
refined = 0
for idx in range(1, 201):
    w = corpus[idx - 1]
    ms = w.get('multiSynonyms')
    if not ms:
        continue
    for opt in ms['options']:
        if opt['word'] == 'Atypical' and 'বিপরীত' in opt['meaningBn']:
            opt['meaningBn'] = 'প্রথাগত কাঠামোর বাইরে বা ব্যতিক্রমধর্মী'
            refined += 1
        elif opt['word'] == 'Contradict' and 'বিপরীত' in opt['meaningBn']:
            opt['meaningBn'] = 'পরস্পরবিরোধী বক্তব্য দেওয়া বা অসত্য প্রমাণ করা'
            refined += 1
        elif opt['word'] == 'Belie' and 'বিপরীত' in opt['meaningBn']:
            opt['meaningBn'] = 'ভুল ধারণা সৃষ্টি করা বা আসল রূপ গোপন রাখা'
            refined += 1
        elif opt['word'] == 'Heterogeneous' and 'বিপরীত' in opt['meaningBn']:
            opt['meaningBn'] = 'বহুবিধ ভিন্নধর্মী উপাদানে গঠিত'
            refined += 1

with open('src/data/gre333.json', 'w', encoding='utf-8') as f:
    json.dump(corpus, f, ensure_ascii=False, indent=2)

print(f"Refined {refined} option definitions in src/data/gre333.json!")
