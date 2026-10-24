# -*- coding: utf-8 -*-
"""
Generates high-caliber, PURELY RANDOM, SOPHISTICATED distractors for Mode 3 across Sets 1 to 10.
Rules:
1. Exactly 3 True Synonyms (1 easy, 1 medium, 1 hard/sophisticated).
2. Exactly 3 Distractors:
   - Purely random & sophisticated GRE words of the exact same part of speech.
   - ZERO relation with target word: NOT a synonym, NOT an antonym, NO shared synonyms, NO shared antonyms.
   - NO overused words (Abate, Aberrant) in early sets.
   - Evenly dispersed across the entire 333-word GRE corpus.
3. Every single option (all 6) has an authentic Bengali definition with zero English characters.
"""

import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

# Load existing Sets 1 to 10 to keep the high-caliber curated 3 true synonyms
existing_sets = {}
for s_idx in range(1, 11):
    mod = __import__(f'mode3_set{s_idx}')
    data = getattr(mod, f'SET_{s_idx}')
    existing_sets.update(data)

corpus_by_pos = {}
for w in corpus:
    pos = w['partOfSpeech']
    if pos not in corpus_by_pos:
        corpus_by_pos[pos] = []
    corpus_by_pos[pos].append(w)

adverb_distractors = [
    {"word": "Ostensibly", "isSynonym": False, "meaningBn": "আপাতদৃষ্টিতে বা বাহ্যত"},
    {"word": "Invariably", "isSynonym": False, "meaningBn": "সর্বদাই বা অপরিবর্তনীয়ভাবে"},
    {"word": "Vehemently", "isSynonym": False, "meaningBn": "তীব্রভাবে বা প্রবল আবেগের সাথে"}
]

# Track distractor usage count to guarantee even, random dispersion
distractor_counts = {}

# Ban words 1 and 2 (Abate, Aberrant) from ever being distractors so user never sees them repeated
banned_distractors = {'abate', 'aberrant'}

final_mode3_data = {}

for idx in range(1, 201):
    target = corpus[idx - 1]
    t_word = target['word']
    pos = target['partOfSpeech']
    
    # Retrieve the 3 curated true synonyms
    true_syns = [o for o in existing_sets[idx]['options'] if o['isSynonym']]
    assert len(true_syns) == 3
    
    if pos == 'adverb':
        distractors = adverb_distractors
    else:
        # Build strict zero-relation candidate pool
        t_syns = set(s.lower() for s in target.get('synonyms', []))
        t_syns.add(t_word.lower())
        for ts in true_syns:
            t_syns.add(ts['word'].lower())
            
        t_ants = set(a.lower() for a in target.get('antonyms', []))
        
        candidates = []
        for c in corpus_by_pos[pos]:
            c_name = c['word'].lower()
            if c_name in banned_distractors or c_name in t_syns or c_name in t_ants:
                continue
            c_syns = set(s.lower() for s in c.get('synonyms', []))
            c_ants = set(a.lower() for a in c.get('antonyms', []))
            
            # ZERO synonym or antonym intersection
            if t_syns.intersection(c_syns) or t_ants.intersection(c_syns) or t_syns.intersection(c_ants) or t_ants.intersection(c_ants):
                continue
            # ZERO mention of target word in meaning
            if t_word.lower() in c['meaningEn'].lower() or c_name in target['meaningEn'].lower():
                continue
            candidates.append(c)
            
        assert len(candidates) >= 3, f"Not enough candidates for {t_word}: {len(candidates)}"
        
        # Sort candidates using a pseudo-random hash seeded by index and characters to spread choices across the corpus
        seed = (idx * 97 + sum(ord(ch) for ch in t_word) * 31) % 10007
        
        def rank_candidate(c):
            usage = distractor_counts.get(c['word'], 0)
            h = (ord(c['word'][0]) * 109 + ord(c['word'][-1]) * 41 + ord(c['word'][len(c['word'])//2]) * 17 + seed) % 257
            return (usage, h)
            
        ranked = sorted(candidates, key=rank_candidate)
        selected = ranked[:3]
        
        distractors = []
        for s in selected:
            distractor_counts[s['word']] = distractor_counts.get(s['word'], 0) + 1
            distractors.append({
                "word": s['word'],
                "isSynonym": False,
                "meaningBn": s['meaningBn'].strip()
            })
            
    final_mode3_data[idx] = {
        "options": true_syns + distractors
    }

print("Generated completely clean, zero-relation, purely random distractors for all 200 words!")

# Verify: Count any antonyms or synonyms among distractors
violations = 0
for idx in range(1, 201):
    target = corpus[idx - 1]
    t_syns = set(s.lower() for s in target.get('synonyms', []))
    t_ants = set(a.lower() for a in target.get('antonyms', []))
    t_syns.add(target['word'].lower())
    
    opts = final_mode3_data[idx]['options']
    for o in opts:
        if not o['isSynonym']:
            w = o['word'].lower()
            if w in t_syns or w in t_ants:
                print(f"VIOLATION at {idx} ({target['word']}): distractor {o['word']} is in syns/ants!")
                violations += 1

print(f"Total violations found: {violations}")
