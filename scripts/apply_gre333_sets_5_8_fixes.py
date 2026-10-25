# -*- coding: utf-8 -*-
"""
Applies comprehensive fixes to GRE 333 Sets 5-8 (Words 81-160) in src/data/gre333.json
based strictly on gre_333_sets_5_8_audit_report_agent_remediation_prompt.md and
MODULE_AUDIT_AND_CURATION_GUIDE.md.
"""
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

JSON_PATH = 'src/data/gre333.json'
REPORT_PATH = 'gre_333_sets_5_8_audit_report_agent_remediation_prompt.md'

print(f"Loading {JSON_PATH}...")
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    corpus = json.load(f)

print(f"Loading {REPORT_PATH}...")
with open(REPORT_PATH, 'r', encoding='utf-8') as f:
    report_text = f.read()

# 1. Parse the multiSynonyms replacement blocks
lines = report_text.splitlines()
blocks = {}
current_id = None
current_word = None
in_json = False
json_lines = []

for line in lines:
    id_m = re.search(r'\*\*(gre333-\d{3})\*\*\s*\(([^)]+)\)', line)
    if not id_m:
        id_m = re.search(r'`(gre333-\d{3})`\s*\(([^)]+)\)', line)
    if id_m:
        current_id = id_m.group(1)
        current_word = id_m.group(2)
    
    if line.strip() == '```json':
        in_json = True
        json_lines = []
        continue
    elif line.strip() == '```' and in_json:
        in_json = False
        raw_json = '\n'.join(json_lines).strip()
        if '"multiSynonyms"' in raw_json and current_id:
            wrapped = "{" + raw_json + "}"
            try:
                parsed = json.loads(wrapped)
                blocks[current_id] = parsed['multiSynonyms']
            except Exception as e:
                print(f"Failed to parse {current_id} ({current_word}): {e}")
        continue
    
    if in_json:
        json_lines.append(line)

print(f"Parsed {len(blocks)} multiSynonyms replacement blocks from report.")

# Apply blocks
for wid, ms in blocks.items():
    entry = next(w for w in corpus if w['id'] == wid)
    entry['multiSynonyms'] = ms

# Strict distractor diversity enforcement (eliminating all duplicate initial letters in distractors):
# 1. gre333-140 (Flag): distractor clumping ['D', 'E', 'E'] (['Distend', 'Emulate', 'Exculpate'])
# Replace Exculpate with Prevaricate
w140 = next(w for w in corpus if w['id'] == 'gre333-140')
for opt in w140['multiSynonyms']['options']:
    if opt['word'] == 'Exculpate':
        opt['word'] = 'Prevaricate'
        opt['meaningBn'] = 'সত্য এড়িয়ে চলা বা ছলচাতুরী করা'

# 2. gre333-143 (Foment): distractor clumping ['D', 'D', 'F'] (['Disabuse', 'Distill', 'Flag'])
# Replace Distill with Saturate
w143 = next(w for w in corpus if w['id'] == 'gre333-143')
for opt in w143['multiSynonyms']['options']:
    if opt['word'] == 'Distill':
        opt['word'] = 'Saturate'
        opt['meaningBn'] = 'ভিজিয়ে পূর্ণ করা বা সম্পৃক্ত করা'

# 3. gre333-148 (Garrulous): distractor clumping ['I', 'P', 'P'] (['Indolent', 'Plastic', 'Porous'])
# Replace Plastic with Tangential
w148 = next(w for w in corpus if w['id'] == 'gre333-148')
for opt in w148['multiSynonyms']['options']:
    if opt['word'] == 'Plastic':
        opt['word'] = 'Tangential'
        opt['meaningBn'] = 'আংশিক বা প্রাসঙ্গিক নয় এমন'

# Section 1 Bengali typography replacements across Sets 5-8:
# gre333-081
w81 = next(w for w in corpus if w['id'] == 'gre333-081')
w81['examples'][1]['bn'] = w81['examples'][1]['bn'].replace("দ্বদ্বদ্বদ্বিধাগ্রস্ততার", "দ্বিধাগ্রস্ততার")

# gre333-086
w86 = next(w for w in corpus if w['id'] == 'gre333-086')
w86['examples'][1]['bn'] = w86['examples'][1]['bn'].replace("রেস্তো রাঁটি", "রেস্তোরাঁটি")

# gre333-110
w110 = next(w for w in corpus if w['id'] == 'gre333-110')
w110['examples'][1]['bn'] = w110['examples'][1]['bn'].replace("রেস্তো রাঁর", "রেস্তোরাঁর")

# gre333-126
w126 = next(w for w in corpus if w['id'] == 'gre333-126')
w126['examples'][0]['bn'] = w126['examples'][0]['bn'].replace("কোয়ান্টাম কম্পি উটিংয়ে", "কোয়ান্টাম কম্পিউটিংয়ে")

# gre333-137
w137 = next(w for w in corpus if w['id'] == 'gre333-137')
for opt in w137['multiSynonyms']['options']:
    if 'পাণ্ডিত্য প্রদশনকারী' in opt['meaningBn']:
        opt['meaningBn'] = opt['meaningBn'].replace('পাণ্ডিত্য প্রদশনকারী', 'পাণ্ডিত্য প্রদর্শনকারী')

# gre333-142
w142 = next(w for w in corpus if w['id'] == 'gre333-142')
w142['examples'][1]['bn'] = w142['examples'][1]['bn'].replace("তুচ্ছতাচ্ছি ল্য", "তুচ্ছতাচ্ছিল্য")

# gre333-143
w143 = next(w for w in corpus if w['id'] == 'gre333-143')
w143['examples'][0]['bn'] = w143['examples'][0]['bn'].replace("বিদেশি আন্দো লনকারীরা", "বিদেশি আন্দোলনকারীরা")

# gre333-144
w144 = next(w for w in corpus if w['id'] == 'gre333-144')
w144['examples'][1]['bn'] = w144['examples'][1]['bn'].replace("কেন্দ্রীয় ব্যাংাংক", "কেন্দ্রীয় ব্যাংক")

# gre333-145
w145 = next(w for w in corpus if w['id'] == 'gre333-145')
for opt in w145['multiSynonyms']['options']:
    if 'ঝোঁঁক' in opt['meaningBn']:
        opt['meaningBn'] = opt['meaningBn'].replace('ঝোঁঁক', 'ঝোঁক')

# Section 2: Study View & Base Array Fixes
# gre333-089
w89 = next(w for w in corpus if w['id'] == 'gre333-089')
w89['meaningEn'] = "A lack of compatibility or similarity between two or more facts; an inconsistency."

# gre333-106
w106 = next(w for w in corpus if w['id'] == 'gre333-106')
w106['antonyms'] = ["flexible", "tolerant", "receptive"]

# gre333-141
w141 = next(w for w in corpus if w['id'] == 'gre333-141')
w141['examples'][0] = {
    "en": "The experienced director patiently guided every fledgling in the theatrical troupe.",
    "bn": "অভিজ্ঞ পরিচালক নাট্যদলের প্রতিটি নবীন শিক্ষানবিসকে ধৈর্যের সাথে পথ দেখিয়েছিলেন।"
}
w141['sentenceCompletion']['sentenceWithBlank'] = "Without generous venture capital subsidies and strategic mentorship, the industry _____ would have succumbed to fierce competition from established tech conglomerates within its first year."

# Verification pass for Sets 5-8 (Words 81-160)
print("\nVerifying Sets 5-8 (Words 81-160)...")
errors = 0
for idx, w in enumerate(corpus[80:160]):
    wid = w['id']
    word = w['word']
    
    # Check multiSynonyms
    ms = w.get('multiSynonyms', {}).get('options', [])
    if len(ms) != 6:
        print(f"Error in {wid}: multiSynonyms options length is {len(ms)}")
        errors += 1
    syns = [o for o in ms if o['isSynonym']]
    dists = [o for o in ms if not o['isSynonym']]
    if len(syns) != 3 or len(dists) != 3:
        print(f"Error in {wid}: syns={len(syns)}, dists={len(dists)}")
        errors += 1
    
    dletters = [d['word'][0].upper() for d in dists]
    if len(set(dletters)) < 3:
        print(f"Error in {wid}: duplicate distractor starting letters {dletters}")
        errors += 1
        
    ants = [a.lower() for a in w.get('antonyms', [])]
    for d in dists:
        if d['word'].lower() in ants:
            print(f"Error in {wid}: distractor '{d['word']}' is in antonyms")
            errors += 1

    # Check multi-word/hyphenated
    for k in ['synonyms', 'antonyms']:
        for item in w.get(k, []):
            if ' ' in item or '-' in item:
                print(f"Error in {wid}: {k} has '{item}'")
                errors += 1
    for opt in ms:
        ow = opt['word']
        if ' ' in ow or '-' in ow:
            print(f"Error in {wid}: multiSynonyms option has '{ow}'")
            errors += 1

    # Check sentenceCompletion
    sc = w.get('sentenceCompletion', {})
    if len(sc.get('options', [])) != 5 or len(sc.get('optionMeaningsBn', [])) != 5:
        print(f"Error in {wid}: sentenceCompletion count mismatch")
        errors += 1
    if len(set(sc.get('options', []))) != 5:
        print(f"Error in {wid}: duplicate option in sentenceCompletion")
        errors += 1

    # Check string corruptions
    w_json = json.dumps(w, ensure_ascii=False)
    corrupted_terms = [
        "দ্বদ্বদ্বদ্বিধা", "দৈনিন কাযবিবরণী", "রেস্তো রাঁ", "ঝোঁঁক", "প্যাঁাঁচালো", 
        "নিঃঃসরণ", "ধীরির", "কম্পি উটিং", "অতি সতক", "সতক বা সাবধানী", 
        "পাণ্ডিত্য প্রদশনকারী", "আন্দো লনকারী", "ব্যাংাংক", "তুচ্ছতাচ্ছি ল্য"
    ]
    for term in corrupted_terms:
        if term in w_json:
            print(f"Error in {wid}: corrupted term '{term}' found")
            errors += 1

if errors > 0:
    print(f"ABORTING: {errors} errors found in Sets 5-8!")
    sys.exit(1)

print(f"Verification successful: 0 errors across Sets 5-8!")

# Save back to src/data/gre333.json
print(f"Saving updated {JSON_PATH}...")
with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(corpus, f, ensure_ascii=False, indent=2)

print("SUCCESS: Successfully saved updated gre333.json for Sets 5-8!")
