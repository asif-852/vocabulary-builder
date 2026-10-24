import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

def get_meaning_distractors(target_word, count=3):
    target_lower = target_word['word'].lower()
    lower_syns = set([s.lower() for s in target_word.get('synonyms', [])] + [target_lower])
    
    def is_valid(w):
        if w['id'] == target_word['id']:
            return False
        w_lower = w['word'].lower()
        if w_lower == target_lower or w_lower in lower_syns:
            return False
        # No synonym overlap
        if any(s.lower() in lower_syns for s in w.get('synonyms', [])):
            return False
        # Definition doesn't contain target word
        if target_lower in w['meaningEn'].lower():
            return False
        return True
        
    same_pos = [w for w in corpus if w['partOfSpeech'] == target_word['partOfSpeech'] and is_valid(w)]
    
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

print("Simulating all 200 questions across Sets 1 to 10 with new filter and cleaned definitions...\n")

issues_count = 0

for q_idx in range(200):
    word_obj = corpus[q_idx]
    q = get_mode1_question(word_obj)
    target = q['targetWord']
    options = q['options']
    
    correct_opts = [opt for opt in options if opt['isCorrect']]
    assert len(correct_opts) == 1
    assert correct_opts[0]['text'] == target['meaningEn']
    
    for idx, opt in enumerate(options):
        letter = chr(65 + idx)
        text = opt['text']
        opt_word = opt['word']
        
        # Check author names / messy punctuation
        if any(bad in text for bad in ['; ;', ';;', ' - ', '- c.b', '- robert', '- bruce', '- anita', '- samuel', '- sir walter', '- virginia']):
            print(f"Set {(q_idx//20)+1} Q{(q_idx%20)+1} [{target['word']}]: Opt {letter} ({opt_word}) has citation: {text}")
            issues_count += 1
            
        if text.endswith(';') or text.endswith(','):
            print(f"Set {(q_idx//20)+1} Q{(q_idx%20)+1} [{target['word']}]: Opt {letter} ({opt_word}) trailing punct: {text}")
            issues_count += 1
            
        # Check POS mismatch
        if target['partOfSpeech'] == 'adjective':
            if text.startswith('To ') or text.startswith('A ') or text.startswith('An ') or text.startswith('The '):
                print(f"Set {(q_idx//20)+1} Q{(q_idx%20)+1} [{target['word']} (adj)]: Opt {letter} ({opt_word}) POS mismatch: {text}")
                issues_count += 1
        elif target['partOfSpeech'] == 'verb':
            if not text.startswith('To '):
                print(f"Set {(q_idx//20)+1} Q{(q_idx%20)+1} [{target['word']} (verb)]: Opt {letter} ({opt_word}) verb without 'To': {text}")
                issues_count += 1
        elif target['partOfSpeech'] == 'noun':
            if text.startswith('To '):
                print(f"Set {(q_idx//20)+1} Q{(q_idx%20)+1} [{target['word']} (noun)]: Opt {letter} ({opt_word}) noun with 'To': {text}")
                issues_count += 1

print(f"\nAudit completed. Total issues found: {issues_count}")

# Print Set 10, Q1 specifically
q_set10_q1 = get_mode1_question(corpus[180])
print("\n--- Set 10, Q1 [Innocuous (adjective)] Options ---")
for idx, opt in enumerate(q_set10_q1['options']):
    mark = "[CORRECT]" if opt['isCorrect'] else "         "
    print(f"{chr(65+idx)}. {mark} ({opt['word']}): {opt['text']}")

# Print Set 6, Q7 specifically (Dormant)
q_set6_q7 = get_mode1_question(corpus[106])
print("\n--- Set 6, Q7 [Dormant (adjective)] Options ---")
for idx, opt in enumerate(q_set6_q7['options']):
    mark = "[CORRECT]" if opt['isCorrect'] else "         "
    print(f"{chr(65+idx)}. {mark} ({opt['word']}): {opt['text']}")
