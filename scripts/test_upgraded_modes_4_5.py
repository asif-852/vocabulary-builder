# -*- coding: utf-8 -*-
"""
Prototype of upgraded getSingleSynonymQuestion and getSingleAntonymQuestion.
Tests all 200 words across Sets 1 to 10.
"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

corpus_by_pos = {}
for w in corpus:
    pos = w['partOfSpeech']
    if pos not in corpus_by_pos:
        corpus_by_pos[pos] = []
    corpus_by_pos[pos].append(w)

corpus_map = {w['word'].lower(): w for w in corpus}

adverb_pool = [
    {"word": "Ostensibly", "meaningBn": "আপাতদৃষ্টিতে বা বাহ্যত"},
    {"word": "Invariably", "meaningBn": "সর্বদাই বা অপরিবর্তনীয়ভাবে"},
    {"word": "Vehemently", "meaningBn": "তীব্রভাবে বা প্রবল আবেগের সাথে"},
    {"word": "Deliberately", "meaningBn": "ইচ্ছাকৃতভাবে বা উদ্দেশ্যপ্রণোদিতভাবে"}
]

def lookup_bn(term, fallback=""):
    found = corpus_map.get(term.lower())
    if found:
        return found['meaningBn']
    return fallback

def capitalize_word(w):
    if not w:
        return ""
    return w[0].upper() + w[1:]

def get_single_synonym_question(target_word):
    t_word = target_word['word']
    pos = target_word['partOfSpeech']
    idx = target_word['indexInSource']
    
    correct_syn = capitalize_word(target_word['synonyms'][0] if target_word['synonyms'] else t_word)
    
    distractor_words = []
    lower_syns = set(s.lower() for s in target_word.get('synonyms', []))
    lower_syns.add(t_word.lower())
    lower_syns.add(correct_syn.lower())
    
    lower_ants = set(a.lower() for a in target_word.get('antonyms', []))
    
    # Trap: 1 antonym if available, with authentic Bengali meaning
    if target_word.get('antonyms'):
        trap_word = target_word['antonyms'][0]
        distractor_words.append({
            'word': capitalize_word(trap_word),
            'meaningBn': lookup_bn(trap_word, f"{target_word['meaningBn']} (বিপরীত)")
        })
        
    if pos == 'adverb':
        for adv in adverb_pool:
            if len(distractor_words) >= 3:
                break
            if adv['word'].lower() not in lower_syns and adv['word'].lower() != distractor_words[0]['word'].lower():
                distractor_words.append(adv)
    else:
        # Filter candidates
        candidates = []
        for c in corpus_by_pos.get(pos, []):
            c_name = c['word'].lower()
            if c_name in lower_syns or c_name in lower_ants:
                continue
            if any(d['word'].lower() == c_name for d in distractor_words):
                continue
            c_syns = set(s.lower() for s in c.get('synonyms', []))
            c_ants = set(a.lower() for a in c.get('antonyms', []))
            if t_word.lower() in c_syns or t_word.lower() in c_ants:
                continue
            if lower_syns.intersection(c_syns):
                continue
            candidates.append(c)
            
        # Seeded deterministic shuffle
        seed = (idx * 79 + sum(ord(ch) for ch in t_word) * 23) % 10007
        def rank_c(c):
            return (ord(c['word'][0]) * 31 + ord(c['word'][-1]) * 17 + seed) % 199
            
        ranked = sorted(candidates, key=rank_c)
        for c in ranked:
            if len(distractor_words) >= 3:
                break
            distractor_words.append({
                'word': capitalize_word(c['word']),
                'meaningBn': c['meaningBn']
            })
            
    options = [
        {'word': correct_syn, 'meaningBn': target_word['meaningBn'], 'isCorrect': True}
    ] + [
        {'word': d['word'], 'meaningBn': d['meaningBn'], 'isCorrect': False}
        for d in distractor_words[:3]
    ]
    
    # Deterministic shuffle
    options.sort(key=lambda o: (ord(o['word'][0]) * 17 + idx) % 31)
    return {'correctSynonym': correct_syn, 'options': options}

def get_single_antonym_question(target_word):
    t_word = target_word['word']
    pos = target_word['partOfSpeech']
    idx = target_word['indexInSource']
    
    correct_ant = capitalize_word(target_word['antonyms'][0] if target_word['antonyms'] else t_word)
    correct_ant_bn = lookup_bn(correct_ant, f"বিপরীত: {target_word['meaningBn']}")
    
    distractor_words = []
    lower_ants = set(a.lower() for a in target_word.get('antonyms', []))
    lower_ants.add(t_word.lower())
    lower_ants.add(correct_ant.lower())
    
    lower_syns = set(s.lower() for s in target_word.get('synonyms', []))
    
    # Trap: 1 synonym if available, with authentic Bengali meaning
    if target_word.get('synonyms'):
        trap_word = target_word['synonyms'][0]
        distractor_words.append({
            'word': capitalize_word(trap_word),
            'meaningBn': lookup_bn(trap_word, target_word['meaningBn'])
        })
        
    if pos == 'adverb':
        for adv in adverb_pool:
            if len(distractor_words) >= 3:
                break
            if adv['word'].lower() not in lower_ants and adv['word'].lower() != distractor_words[0]['word'].lower():
                distractor_words.append(adv)
    else:
        candidates = []
        for c in corpus_by_pos.get(pos, []):
            c_name = c['word'].lower()
            if c_name in lower_ants or c_name in lower_syns:
                continue
            if any(d['word'].lower() == c_name for d in distractor_words):
                continue
            c_ants = set(a.lower() for a in c.get('antonyms', []))
            c_syns = set(s.lower() for s in c.get('synonyms', []))
            if t_word.lower() in c_ants or t_word.lower() in c_syns:
                continue
            if lower_ants.intersection(c_ants):
                continue
            candidates.append(c)
            
        seed = (idx * 67 + sum(ord(ch) for ch in t_word) * 19) % 10007
        def rank_c(c):
            return (ord(c['word'][0]) * 29 + ord(c['word'][-1]) * 13 + seed) % 199
            
        ranked = sorted(candidates, key=rank_c)
        for c in ranked:
            if len(distractor_words) >= 3:
                break
            distractor_words.append({
                'word': capitalize_word(c['word']),
                'meaningBn': c['meaningBn']
            })
            
    options = [
        {'word': correct_ant, 'meaningBn': correct_ant_bn, 'isCorrect': True}
    ] + [
        {'word': d['word'], 'meaningBn': d['meaningBn'], 'isCorrect': False}
        for d in distractor_words[:3]
    ]
    
    options.sort(key=lambda o: (ord(o['word'][0]) * 13 + idx + 7) % 31)
    return {'correctAntonym': correct_ant, 'options': options}

print("Running Prototype Verification across Words 1 to 200...")
m4_errors = 0
m5_errors = 0
m4_dist_counts = {}
m5_dist_counts = {}

for idx in range(1, 201):
    target = corpus[idx - 1]
    
    # Mode 4
    q4 = get_single_synonym_question(target)
    if len(q4['options']) != 4:
        print(f"M4 Error at {idx}: expected 4 options, got {len(q4['options'])}")
        m4_errors += 1
    correct4 = [o for o in q4['options'] if o['isCorrect']]
    if len(correct4) != 1:
        print(f"M4 Error at {idx}: expected 1 correct, got {len(correct4)}")
        m4_errors += 1
    for o in q4['options']:
        if not o['isCorrect']:
            m4_dist_counts[o['word']] = m4_dist_counts.get(o['word'], 0) + 1
            
    # Mode 5
    q5 = get_single_antonym_question(target)
    if len(q5['options']) != 4:
        print(f"M5 Error at {idx}: expected 4 options, got {len(q5['options'])}")
        m5_errors += 1
    correct5 = [o for o in q5['options'] if o['isCorrect']]
    if len(correct5) != 1:
        print(f"M5 Error at {idx}: expected 1 correct, got {len(correct5)}")
        m5_errors += 1
    for o in q5['options']:
        if not o['isCorrect']:
            m5_dist_counts[o['word']] = m5_dist_counts.get(o['word'], 0) + 1

print(f"Mode 4 errors: {m4_errors}")
print(f"Mode 4 total unique distractors: {len(m4_dist_counts)}, max reuse: {max(m4_dist_counts.values())}")
print(f"Mode 5 errors: {m5_errors}")
print(f"Mode 5 total unique distractors: {len(m5_dist_counts)}, max reuse: {max(m5_dist_counts.values())}")
print("\nSample Word 170 (Inadvertently):")
print("Mode 4 options:", [(o['word'], o['isCorrect']) for o in get_single_synonym_question(corpus[169])['options']])
print("Mode 5 options:", [(o['word'], o['isCorrect']) for o in get_single_antonym_question(corpus[169])['options']])
