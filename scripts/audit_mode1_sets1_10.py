import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

def get_meaning_distractors(target_word, count=3):
    same_pos = [
        w for w in corpus 
        if w['partOfSpeech'] == target_word['partOfSpeech'] 
        and w['id'] != target_word['id'] 
        and w['word'].lower() != target_word['word'].lower()
    ]
    seed = sum(ord(c) for c in target_word['word'])
    shuffled = sorted(same_pos, key=lambda a: (ord(a['word'][0]) * seed) % 97)
    return shuffled[:count]

def get_mode1_question(target_word):
    distractors = get_meaning_distractors(target_word, 3)
    raw_options = [
        {'text': target_word['meaningEn'], 'isCorrect': True, 'word': target_word['word'], 'pos': target_word['partOfSpeech']},
        *[
            {'text': d['meaningEn'], 'isCorrect': False, 'word': d['word'], 'pos': d['partOfSpeech']}
            for d in distractors
        ]
    ]
    seed_word = target_word['indexInSource']
    shuffled = sorted(raw_options, key=lambda a: (ord(a['text'][0]) * 19 + seed_word) % 43)
    return {
        'targetWord': target_word,
        'distractors': distractors,
        'options': shuffled
    }

print("=== AUDITING MODE 1 FOR SETS 1 TO 10 (WORDS 1 TO 200) ===\n")

flagged_questions = []

for q_idx in range(200):
    word_obj = corpus[q_idx]
    q = get_mode1_question(word_obj)
    target = q['targetWord']
    options = q['options']
    
    issues = []
    
    # Check if correct option text matches target meaning
    correct_opts = [opt for opt in options if opt['isCorrect']]
    if len(correct_opts) != 1:
        issues.append(f"Expected 1 correct option, got {len(correct_opts)}")
    else:
        c_opt = correct_opts[0]
        if c_opt['text'] != target['meaningEn']:
            issues.append(f"Correct option text mismatch: '{c_opt['text']}' vs '{target['meaningEn']}'")
            
    # Check each option for awkward artifacts
    for idx, opt in enumerate(options):
        letter = chr(65 + idx)
        text = opt['text']
        opt_word = opt['word']
        
        # Check author names / messy punctuation
        if any(bad in text for bad in ['; ;', ';;', ' - ', '- c.b', '- robert', '- bruce', '- anita', '- samuel', '- sir walter', '- virginia']):
            issues.append(f"Option {letter} ({opt_word}) has author attribution / multiple semicolons: '{text}'")
            
        if text.endswith(';') or text.endswith(','):
            issues.append(f"Option {letter} ({opt_word}) has trailing punctuation: '{text}'")
            
        # Check POS grammatical mismatch
        # If target is adjective:
        if target['partOfSpeech'] == 'adjective':
            if text.startswith('To ') or text.startswith('A person ') or text.startswith('A mentor ') or text.startswith('A state ') or text.startswith('An act '):
                issues.append(f"Option {letter} ({opt_word}) is POS mismatch for adjective: '{text}'")
        # If target is noun:
        elif target['partOfSpeech'] == 'noun':
            if text.startswith('To ') or (text.endswith('ing') and not any(text.startswith(w) for w in ['The', 'A', 'An'])):
                if not text.startswith('The ') and not text.startswith('A ') and not text.startswith('An '):
                    # Could be verb-like or adj-like
                    pass
        # If target is verb:
        elif target['partOfSpeech'] == 'verb':
            if text.startswith('A ') or text.startswith('An ') or text.startswith('The ') or text.startswith('Having ') or text.startswith('Characterized '):
                issues.append(f"Option {letter} ({opt_word}) is POS mismatch for verb: '{text}'")
                
        # Check if distractor meaning is a synonym or too similar to target word
        if not opt['isCorrect']:
            target_syns = [s.lower() for s in target.get('synonyms', [])]
            if opt_word.lower() in target_syns:
                issues.append(f"CRITICAL: Option {letter} is a synonym of target word ({opt_word} in {target['word']} synonyms)! Distractor meaning might be correct too!")
    
    if issues:
        set_num = (q_idx // 20) + 1
        q_num = (q_idx % 20) + 1
        flagged_questions.append({
            'set': set_num,
            'q': q_num,
            'word': target['word'],
            'pos': target['partOfSpeech'],
            'meaningEn': target['meaningEn'],
            'options': options,
            'issues': issues
        })

print(f"Total flagged questions in Sets 1 to 10: {len(flagged_questions)}\n")

for f in flagged_questions:
    print(f"Set {f['set']}, Q {f['q']} [{f['word']} ({f['pos']})]:")
    for iss in f['issues']:
        print(f"  * {iss}")
    print("  Options:")
    for idx, opt in enumerate(f['options']):
        c_mark = "[CORRECT]" if opt['isCorrect'] else "         "
        print(f"    {chr(65+idx)}. {c_mark} ({opt['word']}): {opt['text']}")
    print()
