# -*- coding: utf-8 -*-
"""
Audits Study View content for GRE 333 Sets 11 to 17 (Words 201 to 333).
"""
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

words_11_to_17 = corpus[200:333]
print(f"Total words to audit in Sets 11 to 17: {len(words_11_to_17)} (Words 201 to 333)\n")

issues = {
    'pronunciation_en': [],
    'pronunciation_bn': [],
    'meaning_en_artifacts': [],
    'meaning_bn_artifacts': [],
    'pos_mismatch': [],
    'sentences_missing': [],
    'sentence_pos_violation': [],
    'sentence_bn_issues': [],
    'syn_ant_issues': []
}

for idx, w in enumerate(words_11_to_17, 201):
    word = w['word']
    pos = w['partOfSpeech']
    p_en = w.get('pronunciationEn', '').strip()
    p_bn = w.get('pronunciationBn', '').strip()
    m_en = w.get('meaningEn', '').strip()
    m_bn = w.get('meaningBn', '').strip()
    e_en1 = w.get('exampleEn1', '').strip()
    e_bn1 = w.get('exampleBn1', '').strip()
    e_en2 = w.get('exampleEn2', '').strip()
    e_bn2 = w.get('exampleBn2', '').strip()
    syns = w.get('synonyms', [])
    ants = w.get('antonyms', [])
    
    # 1. Pronunciation
    if not p_en:
        issues['pronunciation_en'].append((idx, word, "Missing pronunciationEn"))
    elif '-' not in p_en and len(word) > 5 and not any(p_en.endswith(sfx) for sfx in ['ing', 'ed']):
        # might be monosyllable or missing hyphens
        pass
        
    if not p_bn:
        issues['pronunciation_bn'].append((idx, word, "Missing pronunciationBn"))
    elif re.search(r'[a-zA-Z]', p_bn):
        issues['pronunciation_bn'].append((idx, word, f"English chars in pronunciationBn: {p_bn}"))
        
    # 2. Meaning En artifacts
    if re.search(r'-\s*[a-z\.\s]+$', m_en, re.I) or '; ;' in m_en or m_en.endswith(';'):
        issues['meaning_en_artifacts'].append((idx, word, m_en))
    if len(m_en) < 5:
        issues['meaning_en_artifacts'].append((idx, word, f"Too short: {m_en}"))
        
    # 3. Meaning Bn artifacts
    if re.search(r'[a-zA-Z]', m_bn):
        issues['meaning_bn_artifacts'].append((idx, word, f"English chars in meaningBn: {m_bn}"))
    if not m_bn:
        issues['meaning_bn_artifacts'].append((idx, word, "Empty meaningBn"))
        
    # 4. Example Sentences existence
    if not e_en1 or not e_en2:
        issues['sentences_missing'].append((idx, word, "Missing example sentence(s)"))
    if not e_bn1 or not e_bn2:
        issues['sentence_bn_issues'].append((idx, word, "Missing exampleBn"))
    elif re.search(r'[a-zA-Z]', e_bn1) or re.search(r'[a-zA-Z]', e_bn2):
        issues['sentence_bn_issues'].append((idx, word, "English characters in exampleBn"))
        
    # 5. Check if word or stem appears in both example sentences
    stem = word.lower()[:min(len(word), 5)]
    if stem not in e_en1.lower():
        issues['sentence_pos_violation'].append((idx, word, f"Word stem '{stem}' not in exampleEn1: '{e_en1}'"))
    if stem not in e_en2.lower():
        issues['sentence_pos_violation'].append((idx, word, f"Word stem '{stem}' not in exampleEn2: '{e_en2}'"))
        
    # 6. Synonyms and Antonyms
    if not syns:
        issues['syn_ant_issues'].append((idx, word, "Empty synonyms list"))
    if not ants:
        issues['syn_ant_issues'].append((idx, word, "Empty antonyms list"))
    for s in syns:
        if ' ' in s or len(s) < 2:
            issues['syn_ant_issues'].append((idx, word, f"Multi-word/odd synonym: '{s}'"))
    for a in ants:
        if ' ' in a or len(a) < 2:
            issues['syn_ant_issues'].append((idx, word, f"Multi-word/odd antonym: '{a}'"))

print("=== AUDIT SUMMARY FOR SETS 11 TO 17 (WORDS 201 TO 333) ===")
for cat, lst in issues.items():
    print(f"{cat}: {len(lst)} issues")
    if lst:
        for item in lst[:10]:
            print("   -", item)
        if len(lst) > 10:
            print(f"   ... and {len(lst) - 10} more")
