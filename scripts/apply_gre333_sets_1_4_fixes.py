# -*- coding: utf-8 -*-
"""
Applies comprehensive fixes to GRE 333 Sets 1-4 (Words 1-80) in src/data/gre333.json
based strictly on gre_333_sets_1_4_audit_report_agent_remediation_prompt.md and
MODULE_AUDIT_AND_CURATION_GUIDE.md.
"""
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

JSON_PATH = 'src/data/gre333.json'
REPORT_PATH = 'gre_333_sets_1_4_audit_report_agent_remediation_prompt.md'

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

# Apply multiSynonyms replacements
applied_blocks = 0
for wid, ms in blocks.items():
    entry = next(w for w in corpus if w['id'] == wid)
    entry['multiSynonyms'] = ms
    applied_blocks += 1

# Additional distractor diversity improvements to ensure zero letter clumping:
# In gre333-006, report had Saturate, Distill, Supersede (S-D-S). Replace Supersede with Obviate.
w6 = next(w for w in corpus if w['id'] == 'gre333-006')
for opt in w6['multiSynonyms']['options']:
    if opt['word'] == 'Supersede':
        opt['word'] = 'Obviate'
        opt['meaningBn'] = 'দূর করা বা অপ্রয়োজনীয় করে তোলা'

# In gre333-029, distractors were Contrite, Verbose, Viable (C-V-V). Replace Viable with Pristine.
w29 = next(w for w in corpus if w['id'] == 'gre333-029')
for opt in w29['multiSynonyms']['options']:
    if opt['word'] == 'Viable':
        opt['word'] = 'Pristine'
        opt['meaningBn'] = 'অক্ষত বা আদিম ও নিখুঁত'

# 2. Section 1 Bengali typography, Bijoy & diacritic fixes:
# gre333-013: multiSynonyms.options[5].meaningBn
w13 = next(w for w in corpus if w['id'] == 'gre333-013')
w13['multiSynonyms']['options'][5]['meaningBn'] = "ঘুমপাড়ানি বা নিদ্রাকর্ষক"

# gre333-014: examples[0].bn
w14 = next(w for w in corpus if w['id'] == 'gre333-014')
w14['examples'][0]['bn'] = w14['examples'][0]['bn'].replace("দ্বদ্বদ্বদ্বিধাদ্বন্দ্ব", "দ্বিধাদ্বন্দ্ব")

# gre333-019: multiSynonyms.options[5].meaningBn
w19 = next(w for w in corpus if w['id'] == 'gre333-019')
w19['multiSynonyms']['options'][5]['meaningBn'] = "শান্ত ও আবেগহীন বা ধীরস্থির"

# gre333-035: examples[1].bn
w35 = next(w for w in corpus if w['id'] == 'gre333-035')
w35['examples'][1]['bn'] = w35['examples'][1]['bn'].replace("পরিবর্তন ঘটাচ্ছে ।", "পরিবর্তন ঘটাচ্ছে।")

# gre333-040: examples[1].bn
w40 = next(w for w in corpus if w['id'] == 'gre333-040')
w40['examples'][1]['bn'] = w40['examples'][1]['bn'].replace("শ্রো তারা", "শ্রোতারা")

# gre333-066: examples[0].bn
w66 = next(w for w in corpus if w['id'] == 'gre333-066')
w66['examples'][0]['bn'] = w66['examples'][0]['bn'].replace("প্যাঁাঁচালো", "প্যাঁচালো")

# gre333-073: pronunciationBn
w73 = next(w for w in corpus if w['id'] == 'gre333-073')
w73['pronunciationBn'] = "ডেন-ই-গ্রেইট"

# 3. Section 2 & 3 fixes:
# gre333-007 (Adulterate): sentenceCompletion
w7 = next(w for w in corpus if w['id'] == 'gre333-007')
w7['sentenceCompletion']['optionMeaningsBn'][3] = "অন্য খাতে সরিয়ে ফেলা বা গ্রাস করা"

# gre333-008 (Aesthetic): sentenceCompletion
w8 = next(w for w in corpus if w['id'] == 'gre333-008')
w8['sentenceCompletion']['options'][1] = "Pedestrian"
w8['sentenceCompletion']['optionMeaningsBn'][1] = "সাদামাটা বা গতানুগতিক"
w8['sentenceCompletion']['optionMeaningsBn'][2] = "শিল্পবোধহীন বা স্থূলরুচির"

# gre333-015 (Ameliorate): sentenceCompletion
w15 = next(w for w in corpus if w['id'] == 'gre333-015')
w15['sentenceCompletion']['options'][0] = "Exacerbate"
w15['sentenceCompletion']['optionMeaningsBn'][0] = "আরও খারাপ বা তীব্র করা"

# gre333-024 (Approbation): sentenceCompletion
w24 = next(w for w in corpus if w['id'] == 'gre333-024')
w24['sentenceCompletion']['options'][3] = "Opprobrium"
w24['sentenceCompletion']['optionMeaningsBn'][3] = "তীব্র নিন্দা বা লোকলজ্জা"

# gre333-036 (Banal): synonyms
w36 = next(w for w in corpus if w['id'] == 'gre333-036')
w36['synonyms'] = [s.replace('clichéd', 'cliched') for s in w36['synonyms']]

# gre333-047 (Catalyst): verify meaningBn
w47 = next(w for w in corpus if w['id'] == 'gre333-047')
w47['meaningBn'] = "অনুঘটক বা পরিবর্তন সূচনাকারী"

# Comprehensive verification pass across Sets 1 to 4 (Words 1-80)
print("\nVerifying Sets 1-4 (Words 1-80)...")
errors = 0
for idx, w in enumerate(corpus[:80]):
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
        "দ্বদ্বদ্বদ্বিধা", "নিঃঃসরণ", "নিদ্রাকষক", "ধীরির", "উিগ্ন", 
        "শতসাপেক্ষ", "বিমষ", "প্যাঁাঁচালো", "পূবসূরী", "আদশ", 
        "ডেন্স-ই-গ্রেইট", "শ্রো তারা", "পরিবর্তন ঘটাচ্ছে ।"
    ]
    for term in corrupted_terms:
        if term in w_json:
            print(f"Error in {wid}: corrupted term '{term}' found")
            errors += 1

if errors > 0:
    print(f"ABORTING: {errors} errors found!")
    sys.exit(1)

print(f"Verification successful: 0 errors across Sets 1-4!")

# Save back to src/data/gre333.json
print(f"Saving updated {JSON_PATH}...")
with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(corpus, f, ensure_ascii=False, indent=2)

print("SUCCESS: Successfully saved updated gre333.json!")
