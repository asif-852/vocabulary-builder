# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

corpus_map = {w['word'].lower(): w for w in corpus}
corpus_by_pos = {}
for w in corpus:
    pos = w['partOfSpeech']
    if pos not in corpus_by_pos:
        corpus_by_pos[pos] = []
    corpus_by_pos[pos].append(w)

adverb_pool = [
    {"word": "Ostensibly", "meaningBn": "আপাতদৃষ্টিতে বা বাহ্যত"},
    {"word": "Invariably", "meaningBn": "সর্বদাই বা অপরিবর্তনীয়ভাবে"},
    {"word": "Vehemently", "meaningBn": "তীব্রভাবে বা প্রবল আবেগের সাথে"},
    {"word": "Deliberately", "meaningBn": "ইচ্ছাকৃতভাবে বা উদ্দেশ্যপ্রণোদিতভাবে"}
]

def capitalize_word(s):
    if not s:
        return s
    return s[0].upper() + s[1:].lower()

def lookup_bn(term, fallback=""):
    found = corpus_map.get(term.lower())
    if found:
        return found['meaningBn']
    return fallback

def get_single_synonym_question(target_word):
    correct_syn = capitalize_word(target_word['synonyms'][0]) if target_word.get('synonyms') else capitalize_word(target_word['word'])
    distractor_words = []
    lower_syns = set(s.lower() for s in target_word.get('synonyms', []))
    lower_syns.add(target_word['word'].lower())
    lower_syns.add(correct_syn.lower())
    lower_ants = set(a.lower() for a in target_word.get('antonyms', []))
    
    if target_word.get('antonyms'):
        trap_word = target_word['antonyms'][0]
        distractor_words.append({
            'word': capitalize_word(trap_word),
            'meaningBn': lookup_bn(trap_word, target_word['meaningBn'])
        })
        
    if target_word['partOfSpeech'] == 'adverb':
        for adv in adverb_pool:
            if len(distractor_words) >= 3:
                break
            lower = adv['word'].lower()
            if lower not in lower_syns and not any(d['word'].lower() == lower for d in distractor_words):
                distractor_words.append(adv)
    else:
        candidates = []
        for w in corpus:
            c_name = w['word'].lower()
            if c_name in lower_syns or c_name in lower_ants:
                continue
            if any(d['word'].lower() == c_name for d in distractor_words):
                continue
            if w['partOfSpeech'] != target_word['partOfSpeech']:
                continue
            c_syns = set(s.lower() for s in w.get('synonyms', []))
            c_ants = set(a.lower() for a in w.get('antonyms', []))
            if target_word['word'].lower() in c_syns or target_word['word'].lower() in c_ants:
                continue
            skip = False
            for s in target_word.get('synonyms', []):
                if s.lower() in c_syns:
                    skip = True
                    break
            if skip:
                continue
            candidates.append(w)
            
        seed = (target_word['indexInSource'] * 79 + ord(target_word['word'][0]) * 23) % 10007
        def rank_c(c):
            hash_a = (ord(c['word'][0]) * 31 + ord(c['word'][-1]) * 17 + seed) % 199
            return hash_a
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
    seed = target_word['indexInSource']
    options.sort(key=lambda o: (ord(o['word'][0]) * 17 + seed) % 31)
    return {'correctSynonym': correct_syn, 'options': options}

def get_single_antonym_question(target_word):
    correct_ant = capitalize_word(target_word['antonyms'][0]) if target_word.get('antonyms') else capitalize_word(target_word['word'])
    distractor_words = []
    lower_ants = set(a.lower() for a in target_word.get('antonyms', []))
    lower_ants.add(target_word['word'].lower())
    lower_ants.add(correct_ant.lower())
    lower_syns = set(s.lower() for s in target_word.get('synonyms', []))
    
    if target_word.get('synonyms'):
        trap_word = target_word['synonyms'][0]
        distractor_words.append({
            'word': capitalize_word(trap_word),
            'meaningBn': lookup_bn(trap_word, target_word['meaningBn'])
        })
        
    if target_word['partOfSpeech'] == 'adverb':
        for adv in adverb_pool:
            if len(distractor_words) >= 3:
                break
            lower = adv['word'].lower()
            if lower not in lower_ants and not any(d['word'].lower() == lower for d in distractor_words):
                distractor_words.append(adv)
    else:
        candidates = []
        for w in corpus:
            c_name = w['word'].lower()
            if c_name in lower_ants or c_name in lower_syns:
                continue
            if any(d['word'].lower() == c_name for d in distractor_words):
                continue
            if w['partOfSpeech'] != target_word['partOfSpeech']:
                continue
            c_ants = set(a.lower() for a in w.get('antonyms', []))
            c_syns = set(s.lower() for s in w.get('synonyms', []))
            if target_word['word'].lower() in c_ants or target_word['word'].lower() in c_syns:
                continue
            skip = False
            for a in target_word.get('antonyms', []):
                if a.lower() in c_ants:
                    skip = True
                    break
            if skip:
                continue
            candidates.append(w)
            
        seed = (target_word['indexInSource'] * 67 + ord(target_word['word'][0]) * 19) % 10007
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
        {'word': correct_ant, 'meaningBn': lookup_bn(correct_ant, target_word['meaningBn']), 'isCorrect': True}
    ] + [
        {'word': d['word'], 'meaningBn': d['meaningBn'], 'isCorrect': False}
        for d in distractor_words[:3]
    ]
    seed = target_word['indexInSource'] + 7
    options.sort(key=lambda o: (ord(o['word'][0]) * 13 + seed) % 31)
    return {'correctAntonym': correct_ant, 'options': options}

words_11_17 = corpus[200:333]

print("=== AUDITING SIMULATION FOR SETS 11-17 ===")
m4_issues = []
m5_issues = []

for idx, w in enumerate(words_11_17, 201):
    q4 = get_single_synonym_question(w)
    opts4 = q4['options']
    if len(opts4) != 4:
        m4_issues.append((idx, w['word'], f"Expected 4 options, got {len(opts4)}"))
    if len(set(o['word'].lower() for o in opts4)) != 4:
        m4_issues.append((idx, w['word'], f"Duplicate options: {[o['word'] for o in opts4]}"))
    # Check if any distractor is a synonym
    for o in opts4:
        if not o['isCorrect']:
            if o['word'].lower() in [s.lower() for s in w.get('synonyms', [])]:
                m4_issues.append((idx, w['word'], f"Distractor {o['word']} is in target synonyms!"))
            if o['word'].lower() == w['word'].lower():
                m4_issues.append((idx, w['word'], f"Distractor {o['word']} is the target word!"))
                
    q5 = get_single_antonym_question(w)
    opts5 = q5['options']
    if len(opts5) != 4:
        m5_issues.append((idx, w['word'], f"Expected 4 options, got {len(opts5)}"))
    if len(set(o['word'].lower() for o in opts5)) != 4:
        m5_issues.append((idx, w['word'], f"Duplicate options: {[o['word'] for o in opts5]}"))
    # Check if any distractor is an antonym
    for o in opts5:
        if not o['isCorrect']:
            if o['word'].lower() in [a.lower() for a in w.get('antonyms', [])]:
                m5_issues.append((idx, w['word'], f"Distractor {o['word']} is in target antonyms!"))
            if o['word'].lower() == w['word'].lower():
                m5_issues.append((idx, w['word'], f"Distractor {o['word']} is the target word!"))

print(f"Mode 4 simulation issues: {len(m4_issues)}")
for iss in m4_issues:
    print(" ", iss)
print(f"Mode 5 simulation issues: {len(m5_issues)}")
for iss in m5_issues:
    print(" ", iss)
