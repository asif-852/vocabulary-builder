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

print(f"Loaded GRE 333 words: {len(gre_data)}")
print(f"Total corpus words: {len(all_corpus)}")

# Let's verify getMeaningDistractors logic exactly as in src/data/index.ts:
def get_meaning_distractors(target_word, count=3):
    source_words = gre_data  # target_word['source'] == 'gre333'
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
        # Disallow words whose synonyms overlap with target synonyms/antonyms/target word
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

print("\n--- AUDITING WORDS 201 TO 333 IN GRE 333 (SETS 11 TO 17) ---")

author_patterns = [
    '; ;', ';;', ' - ', '- c.b', '- robert', '- bruce', '- anita', '- samuel', 
    '- sir walter', '- virginia', '- nordhoff', '- emerson', '- thoreau', '- dryden',
    '- pope', '- milton', '- shakespeare', '- bacon', '- johnson', '- swift',
    '- addison', '- locke', '- burke', '- carlyle', '- macaulay', '- ruskin',
    '- tennyson', '- browning', '- arnold', '- huxley', '- darwin'
]

flagged_entries = []
all_issues = []

for idx in range(200, 333):
    word_obj = gre_data[idx]
    w = word_obj['word']
    pos = word_obj['partOfSpeech']
    m_en = word_obj['meaningEn']
    m_bn = word_obj['meaningBn']
    set_num = word_obj['setNumber']
    word_idx = word_obj['indexInSource']
    
    issues = []
    
    # Check 1: Author attribution / trailing punctuation / artifacts
    for ap in author_patterns:
        if ap in m_en.lower():
            issues.append(f"Author attribution pattern '{ap}' in meaningEn: '{m_en}'")
            
    if m_en.endswith(';') or m_en.endswith(','):
        issues.append(f"Trailing punctuation in meaningEn: '{m_en}'")
        
    if m_en.startswith('(') and ')' in m_en:
        issues.append(f"Parenthetical prefix in meaningEn: '{m_en}'")
        
    # Check 2: Botanical / historical / obscure trivia
    # E.g. Latin names, botanical terms, obscure quotes
    if any(k in m_en.lower() for k in ['genus', 'species', 'family of plants', 'order of', 'historical', 'obsolete', 'in former times']):
        issues.append(f"Botanical or historical trivia in meaningEn: '{m_en}'")
        
    # Check 3: POS consistency
    if pos == 'verb' and not m_en.startswith('To '):
        issues.append(f"Verb meaningEn does not start with 'To ': '{m_en}'")
    if pos == 'noun' and m_en.startswith('To '):
        issues.append(f"Noun meaningEn starts with 'To ': '{m_en}'")
    if pos == 'adjective' and m_en.startswith('To '):
        issues.append(f"Adjective meaningEn starts with 'To ': '{m_en}'")
        
    # Check 4: Simulate runtime question
    q = get_mode1_question(word_obj)
    opts = q['options']
    
    # 4a: exactly 4 options
    if len(opts) != 4:
        issues.append(f"Question has {len(opts)} options, expected 4")
        
    # 4b: exactly 1 correct option
    correct_opts = [o for o in opts if o['isCorrect']]
    if len(correct_opts) != 1:
        issues.append(f"Question has {len(correct_opts)} correct options, expected 1")
    elif correct_opts[0]['text'] != m_en:
        issues.append(f"Correct option text mismatch: '{correct_opts[0]['text']}' vs '{m_en}'")
        
    # 4c: Check distractors
    for dist in q['distractors']:
        d_word = dist['word']
        d_pos = dist['partOfSpeech']
        d_men = dist['meaningEn']
        
        # Check POS match
        if d_pos != pos:
            issues.append(f"Distractor '{d_word}' has POS '{d_pos}', expected '{pos}'")
            
        # Check if distractor mentions target word
        if w.lower() in d_men.lower():
            issues.append(f"Distractor '{d_word}' definition contains target word '{w}': '{d_men}'")
            
        # Check if target definition mentions distractor word
        if d_word.lower() in m_en.lower():
            issues.append(f"Target word definition contains distractor '{d_word}': '{m_en}'")
            
        # Check for semantic overlap or synonymy
        target_syns = [s.lower() for s in word_obj.get('synonyms', [])]
        target_ants = [a.lower() for a in word_obj.get('antonyms', [])]
        d_syns = [s.lower() for s in dist.get('synonyms', [])]
        d_ants = [a.lower() for a in dist.get('antonyms', [])]
        
        if d_word.lower() in target_syns:
            issues.append(f"CRITICAL: Distractor '{d_word}' is listed as a synonym of target '{w}'!")
        if d_word.lower() in target_ants:
            issues.append(f"Distractor '{d_word}' is listed as an antonym of target '{w}'!")
        overlap_syns = set(target_syns).intersection(d_syns)
        if overlap_syns:
            issues.append(f"CRITICAL: Distractor '{d_word}' shares synonyms with target '{w}': {overlap_syns}")
            
    if issues:
        flagged_entries.append({
            'index': word_idx,
            'set': set_num,
            'word': w,
            'pos': pos,
            'meaningEn': m_en,
            'meaningBn': m_bn,
            'issues': issues
        })
        all_issues.extend(issues)

print(f"\nTotal words audited in Sets 11-17: 133 (Words 201 to 333)")
print(f"Total words with flagged issues: {len(flagged_entries)}")
print(f"Total flagged issues: {len(all_issues)}\n")

for item in flagged_entries:
    print(f"[{item['index']}] Set {item['set']} - {item['word']} ({item['pos']}):")
    print(f"   MeaningEn: {item['meaningEn']}")
    for iss in item['issues']:
        print(f"   - {iss}")
