# -*- coding: utf-8 -*-
"""
Applies comprehensive fixes to GRE 333 Sets 13-17 (Words 241-333) in src/data/gre333.json
based strictly on gre_333_sets_13_17_audit_report_agent_remediation_prompt.md and
MODULE_AUDIT_AND_CURATION_GUIDE.md.
"""
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

JSON_PATH = 'src/data/gre333.json'
REPORT_PATH = 'gre_333_sets_13_17_audit_report_agent_remediation_prompt.md'

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

# Fix distractor diversity clumping in the parsed blocks:
# 1. gre333-257 (Problematic): Sublime, Striated, Gustatory (S, S, G) -> Replace Striated with Mendacious
w257 = next(w for w in corpus if w['id'] == 'gre333-257')
for opt in w257['multiSynonyms']['options']:
    if opt['word'] == 'Striated':
        opt['word'] = 'Mendacious'
        opt['meaningBn'] = 'মিথ্যাবাদী বা অসত্য'

# 2. gre333-317 (Tortuous): Boorish, Seditious, Salubrious (B, S, S) -> Replace Seditious with Mendacious
w317 = next(w for w in corpus if w['id'] == 'gre333-317')
for opt in w317['multiSynonyms']['options']:
    if opt['word'] == 'Seditious':
        opt['word'] = 'Mendacious'
        opt['meaningBn'] = 'মিথ্যাবাদী বা অসত্য'

# Section 1: Bengali Typography, Bijoy & Diacritic Fixes
# gre333-242
w242 = next(w for w in corpus if w['id'] == 'gre333-242')
w242['examples'][0]['bn'] = w242['examples'][0]['bn'].replace("ক্রে তাদের", "ক্রেতাদের")

# gre333-245
w245 = next(w for w in corpus if w['id'] == 'gre333-245')
w245['examples'][1]['bn'] = w245['examples'][1]['bn'].replace("ক্রে তারা", "ক্রেতারা")

# gre333-252
w252 = next(w for w in corpus if w['id'] == 'gre333-252')
w252['examples'][0]['bn'] = w252['examples'][0]['bn'].replace("কম্পি উটার", "কম্পিউটার")

# gre333-259
w259 = next(w for w in corpus if w['id'] == 'gre333-259')
w259['examples'][1]['bn'] = w259['examples'][1]['bn'].replace("শ্রো তাদের", "শ্রোতাদের")

# gre333-260
w260 = next(w for w in corpus if w['id'] == 'gre333-260')
w260['examples'][0]['bn'] = w260['examples'][0]['bn'].replace("ক্রে তাদের", "ক্রেতাদের")

# gre333-270
w270 = next(w for w in corpus if w['id'] == 'gre333-270')
w270['examples'][0]['bn'] = w270['examples'][0]['bn'].replace("নিঃঃশ্বাস", "নিঃশ্বাস")

# gre333-271
w271 = next(w for w in corpus if w['id'] == 'gre333-271')
w271['examples'][1]['bn'] = w271['examples'][1]['bn'].replace("স্টে ডিয়ামের", "স্টেডিয়ামের")

# gre333-273
w273 = next(w for w in corpus if w['id'] == 'gre333-273')
w273['sentenceCompletion']['options'][1] = "Cosmopolite"
w273['sentenceCompletion']['optionMeaningsBn'][1] = "বিশ্বনাগরিক বা সমাজপ্রিয় ব্যক্তি"

# gre333-275
w275 = next(w for w in corpus if w['id'] == 'gre333-275')
w275['examples'][0]['bn'] = w275['examples'][0]['bn'].replace("খাচ্ছি লেন", "খাচ্ছিলেন")

# gre333-292
w292 = next(w for w in corpus if w['id'] == 'gre333-292')
w292['examples'][0]['bn'] = w292['examples'][0]['bn'].replace("নিঃঃসরণ", "নিঃসরণ")

# gre333-295
w295 = next(w for w in corpus if w['id'] == 'gre333-295')
w295['meaningBn'] = "উদ্বিগ্ন বা যত্নশীল মনোভাবাপন্ন"

# gre333-296
w296 = next(w for w in corpus if w['id'] == 'gre333-296')
w296['meaningBn'] = "ঘুমপাড়ানি বা নিদ্রাকর্ষক"

# gre333-298
w298 = next(w for w in corpus if w['id'] == 'gre333-298')
w298['sentenceCompletion']['optionMeaningsBn'][3] = "নির্জনতা"

# gre333-315
w315 = next(w for w in corpus if w['id'] == 'gre333-315')
w315['examples'][0]['bn'] = w315['examples'][0]['bn'].replace("ক্ষুব্ধ ক্রে তা", "ক্ষুব্ধ ক্রেতা")

# gre333-316
w316 = next(w for w in corpus if w['id'] == 'gre333-316')
w316['examples'][0]['bn'] = w316['examples'][0]['bn'].replace("নিমজ্জি ত", "নিমজ্জিত")

# gre333-320
w320 = next(w for w in corpus if w['id'] == 'gre333-320')
w320['examples'][0]['bn'] = w320['examples'][0]['bn'].replace("হিংংস্র", "হিংস্র")

# gre333-329
w329 = next(w for w in corpus if w['id'] == 'gre333-329')
w329['examples'][1]['bn'] = w329['examples'][1]['bn'].replace("প্রতিক্রি য়াটি", "প্রতিক্রিয়াটি")

# gre333-330
w330 = next(w for w in corpus if w['id'] == 'gre333-330')
w330['examples'][1]['bn'] = w330['examples'][1]['bn'].replace("ক্রে তাদের", "ক্রেতাদের")

# Section 2: Critical Part-of-Speech & Base Array Fixes
# gre333-242 (Placate)
w242['synonyms'] = ["appease", "pacify", "mollify", "conciliate"]

# gre333-251 (Precipitate)
w251 = next(w for w in corpus if w['id'] == 'gre333-251')
w251['examples'] = [
    {
        "en": "A sudden diplomatic insult can easily precipitate an armed border conflict.",
        "bn": "একটি আকস্মিক কূটনৈতিক অপমান সহজেই সশস্ত্র সীমান্ত সংঘাত ডেকে আনতে পারে।"
    },
    {
        "en": "The bank failure threatened to precipitate a nationwide economic panic.",
        "bn": "ব্যাংকটির পতন দেশজুড়ে এক চরম অর্থনৈতিক আতঙ্ক ত্বরান্বিত করার আশঙ্কা তৈরি করেছিল।"
    }
]

# gre333-268 (Quibble)
w268 = next(w for w in corpus if w['id'] == 'gre333-268')
w268['sentenceCompletion'] = {
    "sentenceWithBlank": "Rather than addressing the overarching constitutional principles at stake in the landmark appeal, the defense attorneys chose to _____ endlessly over minor typographical ambiguities in the statute.",
    "options": [
        "Concur",
        "Acquiesce",
        "Capitulate",
        "Harmonize",
        "Quibble"
    ],
    "correctIndex": 4,
    "optionMeaningsBn": [
        "একমত হওয়া",
        "নীরবে মেনে নেওয়া",
        "আত্মসমর্পণ করা",
        "সামঞ্জস্য বিধান করা",
        "তুচ্ছ বিষয়ে খুঁত ধরা বা অহেতুক তর্ক করা"
    ],
    "explanationEn": "Quibble (verb) means to argue or raise petty, trivial objections about a minor matter.",
    "sentenceTranslationBn": "যুগান্তকারী আপিল মামলাটিতে জড়িত মূল সাংবিধানিক নীতিগুলোর মুখোমুখি হওয়ার পরিবর্তে, আসামিপক্ষের আইনজীবীরা আইনের সামান্য মুদ্রণজনিত অস্পষ্টতা নিয়ে অহেতুক খুঁত ধরা ও তর্ক করার পথ বেছে নিয়েছিলেন।"
}

# gre333-270 (Rarefied)
w270['synonyms'] = ["tenuous", "refined", "esoteric", "lofty"]

# gre333-274 (Recondite)
w274 = next(w for w in corpus if w['id'] == 'gre333-274')
w274['sentenceCompletion']['options'][3] = "Pellucid"
w274['sentenceCompletion']['optionMeaningsBn'][3] = "অত্যন্ত স্বচ্ছ ও সহজবোধ্য"

# gre333-278 (Reproach)
w278 = next(w for w in corpus if w['id'] == 'gre333-278')
w278['examples'] = [
    {
        "en": "The manager had to reproach the clerk for repeatedly arriving late.",
        "bn": "বারবার দেরিতে আসার কারণে ব্যবস্থাপক কর্মচারীটিকে তিরস্কার করতে বাধ্য হয়েছিলেন।"
    },
    {
        "en": "Citizens began to reproach the council for neglecting flood defenses.",
        "bn": "বন্যা প্রতিরক্ষা ব্যবস্থা অবহেলা করার জন্য নাগরিকরা কাউন্সিলকে ভর্ৎসনা করতে শুরু করে।"
    }
]

# gre333-283 (Resolve)
w283 = next(w for w in corpus if w['id'] == 'gre333-283')
w283['examples'] = [
    {
        "en": "The board met urgently to resolve the financial crisis before Monday.",
        "bn": "সোমবারের আগেই আর্থিক সংকটটি সমাধান করতে পরিচালনা পর্ষদ জরুরি বৈঠকে বসেছিল।"
    },
    {
        "en": "Mediators met to resolve the border dispute between neighbors.",
        "bn": "প্রতিবেশীদের মধ্যকার সীমান্ত বিরোধ মীমাংসা করতে মধ্যস্থতাকারীরা বসেছিলেন।"
    }
]

# gre333-286 (Sage)
w286 = next(w for w in corpus if w['id'] == 'gre333-286')
w286['examples'] = [
    {
        "en": "The veteran diplomat offered sage observations during the peace summit.",
        "bn": "শান্তি সম্মেলনের সময় প্রবীণ কূটনীতিক অত্যন্ত প্রজ্ঞাপূর্ণ পর্যবেক্ষণ তুলে ধরেছিলেন।"
    },
    {
        "en": "His grandmother offered sage counsel that guided him through life.",
        "bn": "তার দাদি এমন বিচক্ষণ পরামর্শ দিয়েছিলেন যা তাকে পুরো জীবন পথ দেখিয়েছে।"
    }
]

# gre333-296 (Soporific)
w296 = next(w for w in corpus if w['id'] == 'gre333-296')
w296['antonyms'] = ["stimulating", "invigorating", "energizing"]

# gre333-310 (Supersede)
w310 = next(w for w in corpus if w['id'] == 'gre333-310')
w310['synonyms'] = ["replace", "supplant", "oust", "displace"]

# gre333-317 (Tortuous)
w317 = next(w for w in corpus if w['id'] == 'gre333-317')
w317['synonyms'] = ["winding", "twisting", "convoluted", "serpentine"]

# gre333-322 (Venerate)
w322 = next(w for w in corpus if w['id'] == 'gre333-322')
w322['synonyms'] = ["revere", "honor", "worship", "hallow"]

# gre333-323 (Veracious)
w323 = next(w for w in corpus if w['id'] == 'gre333-323')
w323['synonyms'] = ["truthful", "honest", "accurate", "candid"]

# gre333-324 (Verbose)
w324 = next(w for w in corpus if w['id'] == 'gre333-324')
w324['meaningEn'] = "Using or expressed in more words than are needed; wordy and prolix."

# Verification pass for Sets 13-17 (Words 241-333)
print("\nVerifying Sets 13-17 (Words 241-333)...")
errors = 0
for idx, w in enumerate(corpus[240:333]):
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
        "ক্রে তাদের", "ক্রে তারা", "কম্পি উটার", "শ্রো তাদের", "নিঃঃশ্বাস", 
        "স্টে ডিয়াম", "খাচ্ছি লেন", "ঊর্ধ্ বে", "নিঃঃসরণ", "উিগ্ন বা যত্নশীল", 
        "নিদ্রাকষক", "নির্জ্জনতা", "ক্ষুব্ধ ক্রে তা", "নিমজ্জি ত", "হিংংস্র", "প্রতিক্রি য়াটি"
    ]
    for term in corrupted_terms:
        if term in w_json:
            print(f"Error in {wid}: corrupted term '{term}' found")
            errors += 1

if errors > 0:
    print(f"ABORTING: {errors} errors found in Sets 13-17!")
    sys.exit(1)

print(f"Verification successful: 0 errors across Sets 13-17!")

# Save back to src/data/gre333.json
print(f"Saving updated {JSON_PATH}...")
with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(corpus, f, ensure_ascii=False, indent=2)

print("SUCCESS: Successfully saved updated gre333.json for Sets 13-17!")
