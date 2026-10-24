# -*- coding: utf-8 -*-
import json
import sys
from nltk.corpus import wordnet as wn

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
        ranked = sorted(candidates, key=lambda c: (ord(c['word'][0]) * 31 + ord(c['word'][-1]) * 17 + seed) % 199)
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
        ranked = sorted(candidates, key=lambda c: (ord(c['word'][0]) * 29 + ord(c['word'][-1]) * 13 + seed) % 199)
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

pos_map = {
    'noun': {'n'},
    'verb': {'v'},
    'adjective': {'a', 's'},
    'adverb': {'r'}
}

print("=== RUNNING DEEP VERIFICATION ON SETS 11-17 ===")

issues = []

for idx, w in enumerate(words_11_17, 201):
    expected_wn = pos_map.get(w['partOfSpeech'], set())
    
    # Check Mode 4
    q4 = get_single_synonym_question(w)
    opts4 = q4['options']
    if len(opts4) != 4:
        issues.append(f"Word {idx} {w['word']}: Mode 4 options count != 4 ({len(opts4)})")
    if len(set(o['word'].lower() for o in opts4)) != 4:
        issues.append(f"Word {idx} {w['word']}: Mode 4 has duplicate options: {[o['word'] for o in opts4]}")
        
    for o in opts4:
        # Check meaningBn is not empty
        if not o['meaningBn']:
            issues.append(f"Word {idx} {w['word']}: Mode 4 option '{o['word']}' has empty meaningBn")
        # Check POS of distractor
        poses = set(x.pos() for x in wn.synsets(o['word'].lower()))
        if poses and not expected_wn.intersection(poses):
            issues.append(f"Word {idx} {w['word']} ({w['partOfSpeech']}): Mode 4 option '{o['word']}' has mismatched WordNet POS {list(poses)} (isCorrect={o['isCorrect']})")

    # Check Mode 5
    q5 = get_single_antonym_question(w)
    opts5 = q5['options']
    if len(opts5) != 4:
        issues.append(f"Word {idx} {w['word']}: Mode 5 options count != 4 ({len(opts5)})")
    if len(set(o['word'].lower() for o in opts5)) != 4:
        issues.append(f"Word {idx} {w['word']}: Mode 5 has duplicate options: {[o['word'] for o in opts5]}")
        
    for o in opts5:
        if not o['meaningBn']:
            issues.append(f"Word {idx} {w['word']}: Mode 5 option '{o['word']}' has empty meaningBn")
        poses = set(x.pos() for x in wn.synsets(o['word'].lower()))
        if poses and not expected_wn.intersection(poses):
            issues.append(f"Word {idx} {w['word']} ({w['partOfSpeech']}): Mode 5 option '{o['word']}' has mismatched WordNet POS {list(poses)} (isCorrect={o['isCorrect']})")

print(f"Total issues found: {len(issues)}")
for iss in issues:
    print(" -", iss)
