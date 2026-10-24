import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    gre_data = json.load(f)

with open('src/data/wordsmart1.json', 'r', encoding='utf-8') as f:
    ws1_data = json.load(f)

with open('src/data/wordsmart2.json', 'r', encoding='utf-8') as f:
    ws2_data = json.load(f)

all_corpus = gre_data + ws1_data + ws2_data

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
        # Disallow words whose synonyms overlap with target synonyms
        w_syns = [s.lower() for s in w.get('synonyms', [])]
        if any(s in lower_syns for s in w_syns):
            return False
        # Disallow words whose definition contains the target word
        if target_lower in w['meaningEn'].lower():
            return False
        return True

    same_pos_candidates = [
        w for w in source_words
        if w['partOfSpeech'] == target_word['partOfSpeech'] and is_valid_distractor(w)
    ]
    
    if len(same_pos_candidates) >= count:
        pool = same_pos_candidates
    else:
        pool = [
            w for w in all_corpus
            if w['partOfSpeech'] == target_word['partOfSpeech'] and is_valid_distractor(w)
        ]
        
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

print("=====================================================================")
print("SIMULATING ALL 133 QUESTIONS FOR SETS 11 TO 17 (WORDS 201 TO 333)")
print("=====================================================================")

total_questions = 0
failed_questions = []

# List of all suspicious strings or trivia patterns
trivia_patterns = [
    'botany', 'botanical', 'genus', 'species', 'family of', 'order of', 
    'herbaceous', 'zoology', 'historical', 'in ancient rome', 'in ancient greece',
    'feudal', 'obsolete', 'archaic', '- sir', '- john', '- robert', '- samuel',
    '; ;', ';;', '  ', '...'
]

for idx in range(200, 333):
    total_questions += 1
    w_obj = gre_data[idx]
    q = get_mode1_question(w_obj)
    target = q['targetWord']
    opts = q['options']
    distractors = q['distractors']
    
    q_errors = []
    
    # a) Check that every question produces exactly 4 options
    if len(opts) != 4:
        q_errors.append(f"Expected 4 options, got {len(opts)}")
        
    # b) Check that exactly 1 option is marked isCorrect: true
    correct_count = sum(1 for o in opts if o['isCorrect'])
    if correct_count != 1:
        q_errors.append(f"Expected 1 correct option, got {correct_count}")
        
    correct_opt = next((o for o in opts if o['isCorrect']), None)
    if correct_opt and correct_opt['text'] != target['meaningEn']:
        q_errors.append(f"Correct option text mismatch: got '{correct_opt['text']}', expected '{target['meaningEn']}'")
        
    # c) Check that no distractor definition is synonymous or overlapping with target definition
    target_syns = set(s.lower() for s in target.get('synonyms', []))
    target_ants = set(a.lower() for a in target.get('antonyms', []))
    
    for d in distractors:
        d_word = d['word'].lower()
        d_syns = set(s.lower() for s in d.get('synonyms', []))
        
        # Check direct synonym
        if d_word in target_syns:
            q_errors.append(f"Distractor word '{d['word']}' is in target synonyms!")
        if d_word in target_ants:
            q_errors.append(f"Distractor word '{d['word']}' is in target antonyms!")
        syn_overlap = target_syns.intersection(d_syns)
        if syn_overlap:
            q_errors.append(f"Distractor '{d['word']}' shares synonyms {syn_overlap} with target '{target['word']}'")
            
        # Check definition text similarity or overlap
        # Check if words in definition are identical
        t_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', target['meaningEn'].lower()))
        d_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', d['meaningEn'].lower()))
        # Remove common stopwords
        stopwords = {'that', 'with', 'from', 'this', 'have', 'having', 'which', 'their', 'something', 'someone', 'person', 'state', 'quality', 'make', 'being', 'especially', 'manner'}
        common_content_words = (t_words & d_words) - stopwords
        if len(common_content_words) >= 4:
            q_errors.append(f"WARNING: High definition overlap between target '{target['word']}' and distractor '{d['word']}': {common_content_words}")

        # d) Check that no distractor mentions the target word in its definition text
        if re.search(r'\b' + re.escape(target['word'].lower()) + r'\b', d['meaningEn'].lower()):
            q_errors.append(f"Distractor '{d['word']}' definition mentions target word '{target['word']}': '{d['meaningEn']}'")
            
        # Also check if target definition mentions distractor word
        if re.search(r'\b' + re.escape(d['word'].lower()) + r'\b', target['meaningEn'].lower()):
            q_errors.append(f"Target definition mentions distractor word '{d['word']}': '{target['meaningEn']}'")

    # e) Check that no definition contains author quotes, trailing semicolons, or trivia
    for opt in opts:
        text = opt['text']
        opt_w = opt['word']['word']
        for tp in trivia_patterns:
            if tp in text.lower():
                q_errors.append(f"Option for '{opt_w}' contains trivia/artifact pattern '{tp}': '{text}'")
        if text.endswith(';') or text.endswith(','):
            q_errors.append(f"Option for '{opt_w}' has trailing punctuation: '{text}'")
        if text.count(';') >= 3:
            q_errors.append(f"Option for '{opt_w}' has 3 or more semicolons: '{text}'")
            
    # POS consistency check
    if target['partOfSpeech'] == 'verb' and not target['meaningEn'].startswith('To '):
        q_errors.append(f"Target word '{target['word']}' is verb but definition does not start with 'To ': '{target['meaningEn']}'")
    if target['partOfSpeech'] == 'noun' and target['meaningEn'].startswith('To '):
        q_errors.append(f"Target word '{target['word']}' is noun but definition starts with 'To ': '{target['meaningEn']}'")
    if target['partOfSpeech'] == 'adjective' and target['meaningEn'].startswith('To '):
        q_errors.append(f"Target word '{target['word']}' is adjective but definition starts with 'To ': '{target['meaningEn']}'")

    if q_errors:
        failed_questions.append({
            'index': target['indexInSource'],
            'word': target['word'],
            'set': target['setNumber'],
            'errors': q_errors,
            'options': [f"[{'CORRECT' if o['isCorrect'] else 'DISTRACTOR'}] {o['word']['word']}: {o['text']}" for o in opts]
        })

print(f"Total Questions Simulated: {total_questions}")
print(f"Total Questions with Warnings/Errors: {len(failed_questions)}")

for fq in failed_questions:
    print(f"\n--- [{fq['index']}] Set {fq['set']} - Word: {fq['word']} ---")
    for err in fq['errors']:
        print(f"  * {err}")
    print("  Options:")
    for opt_str in fq['options']:
        print(f"    - {opt_str}")
