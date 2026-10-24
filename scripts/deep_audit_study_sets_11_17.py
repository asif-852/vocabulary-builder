# -*- coding: utf-8 -*-
"""
Deep inspection of Study Module data for Sets 11 to 17 (Words 201 to 333).
"""
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

words_11_to_17 = corpus[200:333]
print(f"Auditing {len(words_11_to_17)} words (Words 201 to 333)...\n")

findings = []

for idx, w in enumerate(words_11_to_17, 201):
    word = w['word']
    pos = w['partOfSpeech']
    p_en = w.get('pronunciationEn', '').strip()
    p_bn = w.get('pronunciationBn', '').strip()
    m_en = w.get('meaningEn', '').strip()
    m_bn = w.get('meaningBn', '').strip()
    examples = w.get('examples', [])
    syns = w.get('synonyms', [])
    ants = w.get('antonyms', [])
    
    # 1. Pronunciation
    if not p_en or not p_bn:
        findings.append((idx, word, f"Missing pronunciation: en='{p_en}', bn='{p_bn}'"))
        
    # 2. Meaning English artifacts
    if re.search(r'-\s*[a-z\.\s]+$', m_en, re.I) or '; ;' in m_en or m_en.endswith(';') or m_en.count(';') > 3:
        findings.append((idx, word, f"Scraped author citation/semicolons in meaningEn: '{m_en}'"))
        
    # Check if definition matches POS (e.g. noun def for verb)
    if pos == 'verb' and (m_en.startswith('A ') or m_en.startswith('The ') or m_en.startswith('An ')):
        findings.append((idx, word, f"POS mismatch: verb with noun definition: '{m_en}'"))
    elif pos == 'adjective' and (m_en.startswith('To ') or m_en.startswith('A ')):
        findings.append((idx, word, f"POS mismatch: adjective with non-adj definition: '{m_en}'"))
        
    # 3. Meaning Bengali artifacts
    if re.search(r'[a-zA-Z]', m_bn):
        findings.append((idx, word, f"English chars in meaningBn: '{m_bn}'"))
    if 'কায' in m_bn or 'দৈনিন' in m_bn or 'সেহ' in m_bn or 'উেখ' in m_bn or 'পূণ' in m_bn or 'দািক' in m_bn:
        findings.append((idx, word, f"Corrupted Bengali conjuncts in meaningBn: '{m_bn}'"))
        
    # 4. Examples
    if len(examples) < 2:
        findings.append((idx, word, f"Has fewer than 2 examples: {len(examples)}"))
    else:
        for ex_i, ex in enumerate(examples, 1):
            en = ex.get('en', '').strip()
            bn = ex.get('bn', '').strip()
            if not en or not bn:
                findings.append((idx, word, f"Example {ex_i} has empty en or bn"))
            if '  ' in bn or 'ক্যাাপ্টে ন' in bn:
                findings.append((idx, word, f"Example {ex_i} has Bijoy artifacts in Bengali: '{bn}'"))
            # Check stem in sentence
            stem = word.lower()[:min(len(word), 4)]
            if stem not in en.lower():
                findings.append((idx, word, f"Example {ex_i} may not contain target word ('{word}'): '{en}'"))
                
    # 5. Synonyms & Antonyms
    for s in syns:
        if ' ' in s or len(s) < 2:
            findings.append((idx, word, f"Multi-word synonym: '{s}'"))
    for a in ants:
        if ' ' in a or len(a) < 2:
            findings.append((idx, word, f"Multi-word antonym: '{a}'"))

print(f"Total findings across Sets 11 to 17: {len(findings)}")
for f in findings:
    print(f"Word {f[0]} ({f[1]}): {f[2]}")
