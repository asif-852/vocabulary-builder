import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    gre_data = json.load(f)

# Apply fixes to in-memory copy first to verify
for w in gre_data:
    if w['indexInSource'] == 288:
        w['partOfSpeech'] = 'verb'
        w['explanationEn'] = "Sanction (verb) means to give formal and explicit approval or to impose a penalty."
    if w['indexInSource'] == 245:
        w['meaningBn'] = "আধিক্য বা অতিপ্রাচুর্য"
    if w['indexInSource'] == 250:
        w['meaningBn'] = "ঝুঁকিপূর্ণ বা অনির্ভরযোগ্য"

def get_meaning_distractors(target_word, count=3):
    source_words = gre_data
    target_lower = target_word['word'].lower()
    
    target_syns = [s.lower() for s in target_word.get('synonyms', [])]
    target_ants = [a.lower() for a in target_word.get('antonyms', [])]
    lower_syns = set([target_lower] + target_syns + target_ants)
    
    def is_valid_distractor(w):
        if w['id'] == target_word['id']:
            return False
        w_lower = w['word'].lower()
        if w_lower == target_lower or w_lower in lower_syns:
            return False
        w_syns = [s.lower() for s in w.get('synonyms', [])]
        if any(s in lower_syns for s in w_syns):
            return False
        if target_lower in w['meaningEn'].lower():
            return False
        return True

    same_pos_candidates = [
        w for w in source_words
        if w['partOfSpeech'] == target_word['partOfSpeech'] and is_valid_distractor(w)
    ]
    
    pool = same_pos_candidates
    seed = sum(ord(c) for c in target_word['word'])
    shuffled = sorted(pool, key=lambda a: (ord(a['word'][0]) * seed) % 97)
    return shuffled[:count]

def get_mode1_question(target_word):
    distractors = get_meaning_distractors(target_word, 3)
    raw_options = [
        {'text': target_word['meaningEn'], 'isCorrect': True, 'word': target_word},
        *[
            {'text': d['meaningEn'], 'isCorrect': False, 'word': d}
            for d in distractors
        ]
    ]
    seed = target_word['indexInSource']
    shuffled = sorted(raw_options, key=lambda a: (ord(a['text'][0]) * 19 + seed) % 43)
    return {
        'targetWord': target_word,
        'distractors': distractors,
        'options': shuffled
    }

print("Simulating all 133 questions with fixes applied...")
issues_found = []

for idx in range(200, 333):
    target = gre_data[idx]
    q = get_mode1_question(target)
    opts = q['options']
    distractors = q['distractors']
    
    # Check 1: exactly 4 options
    if len(opts) != 4:
        issues_found.append(f"Q {target['indexInSource']} ({target['word']}): options count = {len(opts)}")
        
    # Check 2: exactly 1 correct
    correct_count = sum(1 for o in opts if o['isCorrect'])
    if correct_count != 1:
        issues_found.append(f"Q {target['indexInSource']} ({target['word']}): correct count = {correct_count}")
        
    # Check 3: no duplicate options
    texts = [o['text'] for o in opts]
    if len(set(texts)) != 4:
        issues_found.append(f"Q {target['indexInSource']} ({target['word']}): duplicate options text!")
        
    # Check 4: POS match for all options
    for o in opts:
        if o['word']['partOfSpeech'] != target['partOfSpeech']:
            issues_found.append(f"Q {target['indexInSource']} ({target['word']}): POS mismatch with {o['word']['word']} ({o['word']['partOfSpeech']})")
            
    # Check 5: target word mentioned in distractor definition
    for d in distractors:
        if target['word'].lower() in d['meaningEn'].lower():
            issues_found.append(f"Q {target['indexInSource']} ({target['word']}): target word in distractor {d['word']} definition: '{d['meaningEn']}'")
        if d['word'].lower() in target['meaningEn'].lower():
            issues_found.append(f"Q {target['indexInSource']} ({target['word']}): distractor {d['word']} in target definition: '{target['meaningEn']}'")

    # Check 6: any option definition with artifacts
    for o in opts:
        t = o['text']
        if any(bad in t.lower() for bad in ['; ;', ';;', ' - ', '- c.b', '- sir walter', '- robert']):
            issues_found.append(f"Q {target['indexInSource']} ({target['word']}): author quote / semicolon artifact in '{t}'")
        if t.endswith(';') or t.endswith(','):
            issues_found.append(f"Q {target['indexInSource']} ({target['word']}): trailing punctuation in '{t}'")

print(f"Total issues found across 133 simulated questions: {len(issues_found)}")
for iss in issues_found:
    print(f"  * {iss}")

if len(issues_found) == 0:
    print(">>> 100% CLEAN: All 133 questions produce exactly 4 valid options, 1 correct answer, identical POS, zero artifacts, zero synonym overlaps, and zero target-word leaks!")
