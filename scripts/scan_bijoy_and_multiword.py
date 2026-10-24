# -*- coding: utf-8 -*-
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

words_11_to_17 = corpus[200:333]

# Check Bijoy glitches across all sentences and meanings
bijoy_glitches = []
multiword_syn_ants = []
pos_def_mismatches = []

for idx, w in enumerate(words_11_to_17, 201):
    word = w['word']
    pos = w['partOfSpeech']
    m_en = w.get('meaningEn', '')
    m_bn = w.get('meaningBn', '')
    
    # Bijoy patterns: double aakars, double e-kars, broken spaces like 'বিক্ষো ভ'
    texts_to_check = [m_bn]
    for ex in w.get('examples', []):
        texts_to_check.append(ex.get('bn', ''))
        
    for text in texts_to_check:
        if re.search(r'[\u09BE\u09BF\u09C0\u09C1\u09C2\u09C7\u09C8\u09CB\u09CC]{2,}', text):
            bijoy_glitches.append((idx, word, "Double vowel sign", text))
        if re.search(r'[\u0980-\u09FF]\s+[\u09BE\u09BF\u09C0\u09C1\u09C2\u09C7\u09C8\u09CB\u09CC]', text):
            bijoy_glitches.append((idx, word, "Vowel sign split by space", text))
        if re.search(r'কায|উেখ|পূণ|সংখ্যাাবৃি|দািক|সেহ|দৈনিন|িধাদ্বে|নিিয়তা|দীিমান|মানববিেষী|বহুবষজীবী', text):
            bijoy_glitches.append((idx, word, "Corrupted conjunct", text))
            
    # Check multiword syns/ants
    for s in w.get('synonyms', []):
        if ' ' in s:
            multiword_syn_ants.append((idx, word, "synonym", s))
    for a in w.get('antonyms', []):
        if ' ' in a:
            multiword_syn_ants.append((idx, word, "antonym", a))

print(f"Total Bijoy/OCR glitches detected: {len(bijoy_glitches)}")
for b in bijoy_glitches[:25]:
    print(f"[{b[0]}: {b[1]}] {b[2]} -> {b[3]}")
if len(bijoy_glitches) > 25:
    print(f"... and {len(bijoy_glitches) - 25} more")

print(f"\nTotal Multi-word Synonyms/Antonyms detected: {len(multiword_syn_ants)}")
for m in multiword_syn_ants:
    print(f"[{m[0]}: {m[1]}] {m[2]} -> '{m[3]}'")
