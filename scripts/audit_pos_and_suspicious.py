# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

words_11_to_17 = corpus[200:333]

for idx, w in enumerate(words_11_to_17, 201):
    pos = w['partOfSpeech']
    m_en = w['meaningEn']
    m_bn = w['meaningBn']
    
    # Check if adjective starts with verb-like phrasing
    if pos == 'adjective' and m_en.lower().startswith(('prove ', 'to ', 'make ', 'cause ')):
        print(f"[{idx}: {w['word']} ({pos})] Adj def starts like verb: '{m_en}'")
        
    # Check if verb starts with noun/adj-like phrasing
    if pos == 'verb' and m_en.lower().startswith(('a ', 'the ', 'an ', 'capable of', 'having ')):
        print(f"[{idx}: {w['word']} ({pos})] Verb def starts like noun/adj: '{m_en}'")
        
    # Check if noun starts with 'To '
    if pos == 'noun' and m_en.lower().startswith('to '):
        print(f"[{idx}: {w['word']} ({pos})] Noun def starts like verb: '{m_en}'")
        
    # Check suspicious Bengali words
    if 'শত' in m_bn and 'শর্ত' not in m_bn:
        print(f"[{idx}: {w['word']}] Suspicious 'শত': '{m_bn}'")
    if 'ধম' in m_bn and 'ধর্ম' not in m_bn:
        print(f"[{idx}: {w['word']}] Suspicious 'ধম': '{m_bn}'")
    if 'কম' in m_bn and 'কর্ম' not in m_bn and 'কম' == m_bn:
        print(f"[{idx}: {w['word']}] Suspicious 'কম': '{m_bn}'")
    if 'বত' in m_bn and 'বর্ত' not in m_bn and 'ব্রত' not in m_bn and 'বতী' not in m_bn:
        print(f"[{idx}: {w['word']}] Suspicious 'বত': '{m_bn}'")
