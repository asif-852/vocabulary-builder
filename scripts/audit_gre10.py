import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', encoding='utf-8') as f:
    gre = json.load(f)

set1_10 = [w for w in gre if w['setNumber'] <= 10]

report_by_set = {}

for w in set1_10:
    s_num = w['setNumber']
    if s_num not in report_by_set:
        report_by_set[s_num] = []
        
    problems = []
    
    # 1. Bangla meaning in brackets
    bn = w['meaningBn']
    if not bn:
        problems.append("Missing Bangla meaning")
    else:
        # Check corrupted glyphs
        if 'াা' in bn: problems.append(f"Bangla meaning has double a-kar ('াা'): '{bn}'")
        if 'ীী' in bn: problems.append(f"Bangla meaning has double ee-kar ('ীী'): '{bn}'")
        if re.search(r'^[িীুূেৈোৌ]', bn): problems.append(f"Bangla meaning starts with orphaned kar: '{bn}'")
        # Check known dropped ref patterns
        dropped_ref = ['সতক', 'পরিবতন', 'সৌন্দয', 'পদমযাদা', 'মিিত', 'দ্ব্যথ', 'বৎসনা', 'কমকত্তা', 'ধম']
        for dr in dropped_ref:
            if dr in bn:
                problems.append(f"Bangla meaning has missing ref (e.g. '{dr}'): '{bn}'")
                
    # 2. POS accuracy
    pos = w['partOfSpeech']
    
    # 3. Pronunciation format
    pron_en = w['pronunciationEn']
    pron_bn = w['pronunciationBn']
    if not pron_en or '-' not in pron_en or pron_en == pron_en.upper():
        problems.append(f"Unformatted pronunciationEn (needs WordSmart syllable stress format): '{pron_en}'")
    if not pron_bn or pron_bn == "উচ্চারণ":
        problems.append(f"Missing pronunciationBn: '{pron_bn}'")
        
    # 4. English meaning
    en = w['meaningEn']
    if not en or len(en.split()) < 3 or en.startswith("Quality, state"):
        problems.append(f"Weak or generic English definition: '{en}'")
        
    # 5. Synonyms & Antonyms
    syns = w['synonyms']
    ants = w['antonyms']
    if any(s.startswith('syn-') for s in syns):
        problems.append("Dummy synonym token found")
    if any(a.startswith('ant-') for a in ants):
        problems.append("Dummy antonym token found")
    if len(syns) < 3:
        problems.append(f"Fewer than 3 synonyms: {syns}")
    if len(ants) < 3:
        problems.append(f"Fewer than 3 antonyms: {ants}")
        
    # 6. Example sentences & POS usage
    ex1 = w['examples'][0]
    ex2 = w['examples'][1]
    
    for ex_num, ex in [(1, ex1), (2, ex2)]:
        ex_en = ex['en']
        ex_bn = ex['bn']
        if 'াা' in ex_bn:
            problems.append(f"Ex{ex_num} Bangla has double a-kar ('াা'): '{ex_bn[:35]}...'")
        if 'সম্পর্কিত' in ex_bn:
            problems.append(f"Ex{ex_num} Bangla has generic template translation")
        if not ex_en or not ex_bn:
            problems.append(f"Ex{ex_num} is empty")
            
    report_by_set[s_num].append({
        "index": w['indexInSource'],
        "word": w['word'],
        "pos": pos,
        "problems": problems,
        "data": w
    })

print(f"=== GRE 333 SETS 1-10 AUDIT REPORT ===")
total_flagged = 0
for s_num in range(1, 11):
    words_in_set = report_by_set[s_num]
    flagged = [w for w in words_in_set if w['problems']]
    total_flagged += len(flagged)
    print(f"\nSet {s_num}: {len(flagged)} of {len(words_in_set)} words flagged with issues")
    for f in flagged[:4]: # show first 4 per set
        print(f"  #{f['index']} {f['word']} ({f['pos']}):")
        for p in f['problems']:
            print(f"     * {p}")

print(f"\nTotal flagged across Sets 1 to 10: {total_flagged} of 200 words.")
