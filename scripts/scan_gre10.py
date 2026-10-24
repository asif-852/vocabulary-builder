import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', encoding='utf-8') as f:
    gre = json.load(f)

set1_10 = [w for w in gre if w['setNumber'] <= 10]

print(f"Total words scanned in Sets 1 to 10: {len(set1_10)}")

issues_found = []

for w in set1_10:
    word_issues = []
    
    # 1. Check Bangla meaning in bracket
    bn = w['meaningBn']
    if not bn:
        word_issues.append("Missing Bangla meaning")
    # Check for broken font patterns (double matras, dropped ref, leading kars)
    if 'াা' in bn or 'ীী' in bn or 'ূূ' in bn:
        word_issues.append(f"Corrupted vowel signs in Bangla meaning: {bn}")
    if re.search(r'^[িীুূেৈোৌ]', bn):
        word_issues.append(f"Orphan leading kar in Bangla meaning: {bn}")
        
    # 2. Check Part of Speech
    pos = w['partOfSpeech']
    if pos not in ['verb', 'noun', 'adjective', 'adverb']:
        word_issues.append(f"Invalid POS: {pos}")
        
    # 3. Check Pronunciation
    pron_en = w['pronunciationEn']
    pron_bn = w['pronunciationBn']
    if not pron_en or pron_en == w['word'].upper() or '-' not in pron_en:
        word_issues.append(f"Missing or naive pronunciationEn: {pron_en}")
        
    # 4. Check Meaning EN
    en_mean = w['meaningEn']
    if not en_mean or en_mean.startswith("Quality, state, or action"):
        word_issues.append(f"Generic or missing English meaning: {en_mean}")
        
    # 5. Check Synonyms
    syns = w['synonyms']
    if len(syns) < 3:
        word_issues.append(f"Fewer than 3 synonyms: {syns}")
    for s in syns:
        if 'syn-' in s:
            word_issues.append(f"Dummy synonym: {s}")
            
    # 6. Check Antonyms
    ants = w['antonyms']
    if len(ants) < 3:
        word_issues.append(f"Fewer than 3 antonyms: {ants}")
    for a in ants:
        if 'ant-' in a:
            word_issues.append(f"Dummy antonym: {a}")
            
    # 7. Check Examples
    examples = w['examples']
    if len(examples) != 2:
        word_issues.append(f"Expected 2 examples, got {len(examples)}")
    else:
        for ex_i, ex in enumerate(examples, 1):
            ex_en = ex['en']
            ex_bn = ex['bn']
            if not ex_en:
                word_issues.append(f"Example {ex_i} EN is empty")
            if not ex_bn:
                word_issues.append(f"Example {ex_i} BN is empty")
            if 'াা' in ex_bn or 'ীী' in ex_bn or 'ূূ' in ex_bn:
                word_issues.append(f"Corrupted vowel sign in Ex{ex_i} BN: {ex_bn[:40]}...")
            if 'সম্পর্কিত' in ex_bn:
                word_issues.append(f"Dummy template in Ex{ex_i} BN: {ex_bn}")
                
            # Check if target word is in example sentence
            # Target word might be inflected (e.g. -ed, -s, -ing, or irregular)
            w_stem = w['word'].lower()[:4]
            if w_stem not in ex_en.lower():
                word_issues.append(f"Target word '{w['word']}' might not appear in Ex{ex_i}: '{ex_en}'")
                
    if word_issues:
        issues_found.append({
            "setNumber": w['setNumber'],
            "index": w['indexInSource'],
            "word": w['word'],
            "pos": pos,
            "issues": word_issues
        })

print(f"\nFound issues in {len(issues_found)} of 200 words:")
for iss in issues_found[:30]:
    print(f"Set {iss['setNumber']} #{iss['index']} {iss['word']} ({iss['pos']}):")
    for i in iss['issues']:
        print(f"   - {i}")
