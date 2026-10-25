# -*- coding: utf-8 -*-
"""
Applies comprehensive fixes to GRE 333 Sets 9-12 (Words 161-240) in src/data/gre333.json
based strictly on gre_333_sets_9_12_audit_report_agent_remediation_prompt.md and
MODULE_AUDIT_AND_CURATION_GUIDE.md.
"""
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

JSON_PATH = 'src/data/gre333.json'
REPORT_PATH = 'gre_333_sets_9_12_audit_report_agent_remediation_prompt.md'

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

# Distractor diversity fix for gre333-164 (Impermeable):
# distractors are Anomalous, Complaisant, Austere (A, C, A)
# Replace Austere with Pristine
w164 = next(w for w in corpus if w['id'] == 'gre333-164')
for opt in w164['multiSynonyms']['options']:
    if opt['word'] == 'Austere':
        opt['word'] = 'Pristine'
        opt['meaningBn'] = 'অক্ষত বা আদিম ও নিখুঁত'

# Section 1: Bengali Typography, Bijoy & Diacritic Fixes
# gre333-166
w166 = next(w for w in corpus if w['id'] == 'gre333-166')
w166['examples'][0]['bn'] = w166['examples'][0]['bn'].replace("স্যাঁাঁতসেঁতে", "স্যাঁতসেঁতে")

# gre333-169
w169 = next(w for w in corpus if w['id'] == 'gre333-169')
w169['examples'][0]['bn'] = w169['examples'][0]['bn'].replace("বিস্ ফোরক", "বিস্ফোরক")

# gre333-171
w171 = next(w for w in corpus if w['id'] == 'gre333-171')
w171['examples'][1]['bn'] = w171['examples'][1]['bn'].replace("পাচ্ছি লেন", "পাচ্ছিলেন")

# gre333-178
w178 = next(w for w in corpus if w['id'] == 'gre333-178')
w178['examples'][0]['bn'] = w178['examples'][0]['bn'].replace("অস্ত্রো পচারের", "অস্ত্রোপচারের")

# gre333-181
w181 = next(w for w in corpus if w['id'] == 'gre333-181')
w181['sentenceCompletion']['optionMeaningsBn'][4] = "প্রাণঘাতী বা মারাত্মক ক্ষতিকর"

# gre333-184
w184 = next(w for w in corpus if w['id'] == 'gre333-184')
for opt in w184['multiSynonyms']['options']:
    if "উিগ্ন" in opt['meaningBn']:
        opt['meaningBn'] = opt['meaningBn'].replace("উিগ্ন", "উদ্বিগ্ন")

# gre333-190
w190 = next(w for w in corpus if w['id'] == 'gre333-190')
for opt in w190['multiSynonyms']['options']:
    if "গোঁঁড়া" in opt['meaningBn']:
        opt['meaningBn'] = opt['meaningBn'].replace("গোঁঁড়া", "গোঁড়া")

# gre333-195
w195 = next(w for w in corpus if w['id'] == 'gre333-195')
for opt in w195['multiSynonyms']['options']:
    if "পূবসূরী" in opt['meaningBn']:
        opt['meaningBn'] = opt['meaningBn'].replace("পূবসূরী", "পূর্বসূরি")

# gre333-196
w196 = next(w for w in corpus if w['id'] == 'gre333-196')
for opt in w196['multiSynonyms']['options']:
    if "নিদ্রাকষক" in opt['meaningBn']:
        opt['meaningBn'] = opt['meaningBn'].replace("নিদ্রাকষক", "নিদ্রাকর্ষক")

# gre333-211
w211 = next(w for w in corpus if w['id'] == 'gre333-211')
w211['examples'][0]['bn'] = w211['examples'][0]['bn'].replace("অস্ত্রো পচার", "অস্ত্রোপচার")

# gre333-212
w212 = next(w for w in corpus if w['id'] == 'gre333-212')
w212['examples'][0]['bn'] = w212['examples'][0]['bn'].replace("বিচ্ছি ন্নভাবে", "বিচ্ছিন্নভাবে")

# gre333-221
w221 = next(w for w in corpus if w['id'] == 'gre333-221')
w221['examples'][0]['bn'] = w221['examples'][0]['bn'].replace("অস্ত্রো পচারের", "অস্ত্রোপচারের")

# gre333-224
w224 = next(w for w in corpus if w['id'] == 'gre333-224')
w224['sentenceCompletion']['optionMeaningsBn'][3] = "বেদনাহীন বা সহজ"

# gre333-228
w228 = next(w for w in corpus if w['id'] == 'gre333-228')
w228['examples'][0]['bn'] = w228['examples'][0]['bn'].replace("নিঃঃস্বার্থ", "নিঃস্বার্থ")

# Section 2: Study View & Sentence Completion Fixes
# gre333-169
w169['synonyms'] = ["collapse", "crumple", "buckle"]

# gre333-183
w183 = next(w for w in corpus if w['id'] == 'gre333-183')
w183['antonyms'] = ["declare", "proclaim", "announce"]

# gre333-185
w185 = next(w for w in corpus if w['id'] == 'gre333-185')
w185['synonyms'] = ["parochialism", "isolationism", "provincialism"]

# gre333-188
w188 = next(w for w in corpus if w['id'] == 'gre333-188')
w188['sentenceCompletion']['sentenceWithBlank'] = "Following the sudden global release of the flawed mobile software patch, hundreds of thousands of error reports began to _____ the company's technical support portals."

# gre333-191
w191 = next(w for w in corpus if w['id'] == 'gre333-191')
w191['synonyms'] = ["irritable", "cantankerous", "choleric"]
w191['antonyms'] = ["placid", "calm", "amiable"]

# gre333-193
w193 = next(w for w in corpus if w['id'] == 'gre333-193')
w193['synonyms'] = ["schedule", "route", "agenda"]

# gre333-212
w212['sentenceCompletion']['options'][4] = "Egalitarian"
w212['sentenceCompletion']['optionMeaningsBn'][4] = "সাম্যবাদী ব্যক্তি"

# Verification pass for Sets 9-12 (Words 161-240)
print("\nVerifying Sets 9-12 (Words 161-240)...")
errors = 0
for idx, w in enumerate(corpus[160:240]):
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
        "স্যাঁাঁতসেঁতে", "বিস্ ফোরক", "পাচ্ছি লেন", "অস্ত্রো পচার", 
        "বিমষ", "উিগ্ন", "গোঁঁড়া", "পূবসূরী", "নিদ্রাকষক", 
        "হিংংস্রতা", "ঝোঁঁক", "বিচ্ছি ন্নভাবে", "বেদাহীন বা সহজ", "নিঃঃস্বার্থ"
    ]
    for term in corrupted_terms:
        if term in w_json:
            print(f"Error in {wid}: corrupted term '{term}' found")
            errors += 1

if errors > 0:
    print(f"ABORTING: {errors} errors found in Sets 9-12!")
    sys.exit(1)

print(f"Verification successful: 0 errors across Sets 9-12!")

# Save back to src/data/gre333.json
print(f"Saving updated {JSON_PATH}...")
with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(corpus, f, ensure_ascii=False, indent=2)

print("SUCCESS: Successfully saved updated gre333.json for Sets 9-12!")
