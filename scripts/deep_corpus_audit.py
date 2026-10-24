import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

print(f"Total words in corpus: {len(corpus)}\n")

pos_mismatches = []
messy_meanings = []

for idx, item in enumerate(corpus):
    w = item['word']
    pos = item['partOfSpeech']
    m_en = item['meaningEn']
    m_bn = item['meaningBn']
    
    # Check messy punctuation / author citations
    if any(k in m_en for k in ['; ;', ';;', ' - ', '- c.b', '- robert', '- bruce', '- anita', '- samuel', '- sir walter', '- virginia', '- nordhoff']):
        messy_meanings.append((idx+1, w, pos, "Author / multiple semicolons", m_en))
    elif m_en.endswith(';') or m_en.endswith(','):
        messy_meanings.append((idx+1, w, pos, "Trailing punctuation", m_en))
    elif m_en.startswith('(') and ')' in m_en:
        messy_meanings.append((idx+1, w, pos, "Parenthetical start", m_en))
        
    # Check POS alignment with meaningEn
    if pos == 'verb':
        if m_en.startswith('A ') or m_en.startswith('An ') or m_en.startswith('The '):
            pos_mismatches.append((idx+1, w, pos, "Noun definition for verb", m_en))
        elif not m_en.startswith('To ') and not (m_en[0].isupper() and any(m_en.startswith(v) for v in ['Cause', 'Make', 'Be', 'Lessen', 'Give', 'Show', 'Take', 'Express', 'Act', 'Put', 'Fill', 'Grow', 'Cast', 'Cancel', 'Command'])):
            # Check if it looks like an adjective or noun
            if m_en.endswith('able') or m_en.endswith('al') or m_en.endswith('ive') or m_en.endswith('ous'):
                pos_mismatches.append((idx+1, w, pos, "Adj-like ending for verb", m_en))
                
    elif pos == 'noun':
        if m_en.startswith('To '):
            pos_mismatches.append((idx+1, w, pos, "Verb definition ('To...') for noun", m_en))
        elif m_en.endswith('ous') or m_en.endswith('ful') or m_en.endswith('ive'):
            pos_mismatches.append((idx+1, w, pos, "Adj-like ending for noun", m_en))
            
    elif pos == 'adjective':
        if m_en.startswith('To '):
            pos_mismatches.append((idx+1, w, pos, "Verb definition ('To...') for adjective", m_en))
        elif m_en.startswith('A ') or m_en.startswith('An ') or m_en.startswith('The '):
            pos_mismatches.append((idx+1, w, pos, "Noun definition ('A/An/The...') for adjective", m_en))

print("=== MESSY / CITATION ARTIFACTS ===")
for m in messy_meanings:
    print(f"[{m[0]}] {m[1]} ({m[2]}): {m[3]}")
    print(f"      meaningEn: {m[4]}")

print("\n=== POS MISMATCHES IN DEFINITIONS ===")
for p in pos_mismatches:
    print(f"[{p[0]}] {p[1]} ({p[2]}): {p[3]}")
    print(f"      meaningEn: {p[4]}")
