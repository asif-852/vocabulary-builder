import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', encoding='utf-8') as f:
    gre = json.load(f)

set1_10 = [w for w in gre if w['setNumber'] <= 10]

# Detailed check categories
font_glitches_meaning = []
font_glitches_examples = []
unformatted_prons = []
noisy_syns_ants = []
pos_suspects = []

for w in set1_10:
    idx = w['indexInSource']
    word = w['word']
    pos = w['partOfSpeech']
    bn = w['meaningBn']
    
    # Font glitches in meaning
    if any(k in bn for k in ['াা', 'ীী', 'ূূ', 'ঁঁ', '্্']) or re.search(r'^[িীুূেৈোৌ]', bn) or any(d in bn for d in ['সতক', 'পরিবতন', 'সৌন্দয', 'পদমযাদা', 'মিিত', 'দ্ব্যথ', 'বৎসনা', 'দুবল']):
        font_glitches_meaning.append((idx, word, bn))
        
    # Font glitches in examples
    for i, ex in enumerate(w['examples'], 1):
        ex_bn = ex['bn']
        if any(k in ex_bn for k in ['াা', 'ীী', 'ূূ', 'ঁঁ', '্্']) or 'ক্রি য়া' in ex_bn or 'নিখোঁঁজ' in ex_bn or 'স্নাায়ু' in ex_bn or 'ব্যাাহত' in ex_bn:
            font_glitches_examples.append((idx, word, f"Ex{i}", ex_bn))
            
    # Unformatted pronunciations
    if w['pronunciationEn'] == word.upper() or '-' not in w['pronunciationEn']:
        unformatted_prons.append((idx, word, w['pronunciationEn'], w['pronunciationBn']))
        
    # Noisy syns or ants
    # E.g. syns with slake, neandertal, or words with lemmas of different senses
    for s in w['synonyms']:
        if s in ['slake', 'neandertal', 'stay', 'appreciate']:
            noisy_syns_ants.append((idx, word, 'synonym', s))
    for a in w['antonyms']:
        if a in ['depreciate']:
            noisy_syns_ants.append((idx, word, 'antonym', a))

print(f"1. Words with Bangla meaning font glitches: {len(font_glitches_meaning)} / 200")
print(f"2. Example sentences with Bangla font glitches: {len(font_glitches_examples)}")
print(f"3. Words with unformatted all-caps pronunciationEn: {len(unformatted_prons)} / 200")
print(f"4. Words with noisy WordNet syns/ants flagged: {len(noisy_syns_ants)}")
