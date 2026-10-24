import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)[:200]

print("=== AUDIT REPORT FOR GRE 333 (SETS 1 TO 10, WORDS 1 TO 200) ===")

# 1. Check Pronunciations
bad_pron_en = []
bad_pron_bn = []
for d in data:
    en_p = d.get('pronunciationEn', '')
    bn_p = d.get('pronunciationBn', '')
    if not en_p or en_p.isupper() or '-' not in en_p:
        bad_pron_en.append((d['id'], d['word'], en_p))
    if not bn_p or '-' not in bn_p:
        bad_pron_bn.append((d['id'], d['word'], bn_p))

print(f"\n1. Pronunciations:")
print(f"   - Invalid/unformatted English pronunciations: {len(bad_pron_en)}")
print(f"   - Invalid/unformatted Bengali pronunciations: {len(bad_pron_bn)}")
if bad_pron_en:
    print(f"     Examples: {bad_pron_en[:3]}")

# 2. Check Part of Speech
valid_pos = {'noun', 'verb', 'adjective', 'adverb'}
bad_pos = []
for d in data:
    pos = d.get('partOfSpeech', '')
    if pos not in valid_pos:
        bad_pos.append((d['id'], d['word'], pos))

print(f"\n2. Part of Speech:")
print(f"   - Words with non-standard POS: {len(bad_pos)}")

# 3. Check Headword Meaning Bengali
dup_kars = re.compile(r'([\u09BE-\u09CC\u0981-\u0983])\1+')
corrupt_roots = ['সতক', 'সৌন্দয', 'পদমযাদা', 'মিিত', 'দ্ব্যথ', 'পরিবতন', 'নিময়', 'নিধারিত', 'কমী', 'বহিস্কাার', 'মযাদা']

bad_meanings_bn = []
for d in data:
    mbn = d.get('meaningBn', '')
    if not mbn:
        bad_meanings_bn.append((d['id'], d['word'], "MISSING"))
    elif dup_kars.search(mbn):
        bad_meanings_bn.append((d['id'], d['word'], f"DUP KAR: {mbn}"))
    elif any(cr in mbn for cr in corrupt_roots):
        bad_meanings_bn.append((d['id'], d['word'], f"CORRUPT ROOT: {mbn}"))

print(f"\n3. Headword Bengali Meanings:")
print(f"   - Words with missing or font-corrupted Bengali meaning: {len(bad_meanings_bn)}")
if bad_meanings_bn:
    print(f"     List: {bad_meanings_bn}")

# 4. Check Synonyms & Antonyms
bad_syns = []
bad_ants = []
for d in data:
    syns = d.get('synonyms', [])
    ants = d.get('antonyms', [])
    if len(syns) < 2 or any(len(s.strip()) == 0 for s in syns):
        bad_syns.append((d['id'], d['word'], syns))
    if len(ants) < 2 or any(len(a.strip()) == 0 or 'ant-' in a for a in ants):
        bad_ants.append((d['id'], d['word'], ants))

print(f"\n4. Synonyms & Antonyms:")
print(f"   - Insufficient or placeholder synonyms: {len(bad_syns)}")
print(f"   - Insufficient or placeholder antonyms: {len(bad_ants)}")

# 5. Check Examples & Translations
dummy_bn_kw = ['সম্পর্কিত', 'উদাহরণ', 'বাক্য']
bad_examples = []
for d in data:
    exs = d.get('examples', [])
    if len(exs) < 2:
        bad_examples.append((d['id'], d['word'], "Less than 2 examples"))
        continue
    for i, ex in enumerate(exs):
        en = ex.get('en', '').strip()
        bn = ex.get('bn', '').strip()
        if not en or not bn:
            bad_examples.append((d['id'], d['word'], f"Empty ex{i+1}"))
        elif any(k in bn for k in dummy_bn_kw):
            bad_examples.append((d['id'], d['word'], f"Dummy ex{i+1}: {bn}"))
        elif dup_kars.search(bn):
            bad_examples.append((d['id'], d['word'], f"Dup kar ex{i+1}: {bn}"))
        elif any(cr in bn for cr in corrupt_roots):
            bad_examples.append((d['id'], d['word'], f"Corrupt root ex{i+1}: {bn}"))

print(f"\n5. Examples & Translations:")
print(f"   - Broken or dummy examples: {len(bad_examples)}")
if bad_examples:
    for b in bad_examples:
        print(f"     {b}")

# 6. Check Sentence Completion 501 Questions
bad_sc = []
for d in data:
    sc = d.get('sentenceCompletion')
    if not sc:
        bad_sc.append((d['id'], d['word'], "MISSING"))
        continue
    if len(sc.get('options', [])) != 5:
        bad_sc.append((d['id'], d['word'], f"Options count = {len(sc.get('options', []))}"))
    if sc.get('options', [])[sc.get('correctIndex', -1)] != d['word']:
        bad_sc.append((d['id'], d['word'], "Correct option mismatch"))
    if '_____' not in sc.get('sentenceWithBlank', ''):
        bad_sc.append((d['id'], d['word'], "No blank in sentenceWithBlank"))
    if len(sc.get('optionMeaningsBn', [])) != 5:
        bad_sc.append((d['id'], d['word'], "Missing option meanings Bn"))

print(f"\n6. Sentence Completion Questions:")
print(f"   - Defective sentence completion questions: {len(bad_sc)}")
if bad_sc:
    print(f"     List: {bad_sc}")
