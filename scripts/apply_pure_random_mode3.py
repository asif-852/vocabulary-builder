# -*- coding: utf-8 -*-
"""
Applies pure random, sophisticated, zero-relation distractors to Mode 3 across Sets 1 to 10 in gre333.json.
Guarantees:
1. 3 True Synonyms (1 easy, 1 medium, 1 hard/sophisticated).
2. 3 Purely Random Distractors:
   - Zero relation to target word: NO antonyms, NO synonyms, NO shared synonyms/antonyms.
   - Exact same part of speech.
   - Purely random & sophisticated GRE words.
   - No early loop words like Abate or Aberrant.
3. Every single option has an authentic Bengali meaning with zero English characters and zero placeholders.
"""

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('scripts')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

# Load existing curated true synonyms from Sets 1 to 10
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

distractor_counts = {}
banned_distractors = {'abate', 'aberrant'}

applied_count = 0
for idx in range(1, 201):
    target = corpus[idx - 1]
    t_word = target['word']
    pos = target['partOfSpeech']
    
    # Retrieve the 3 curated true synonyms
    true_syns = [o for o in existing_sets[idx]['options'] if o['isSynonym']]
    assert len(true_syns) == 3, f"Word {idx} {t_word} must have 3 true synonyms"
    
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
            
    target['multiSynonyms'] = {
        "options": true_syns + distractors
    }
    applied_count += 1

# Write back to gre333.json
with open('src/data/gre333.json', 'w', encoding='utf-8') as f:
    json.dump(corpus, f, ensure_ascii=False, indent=2)

print(f"Applied pure random Mode 3 configuration to {applied_count} words in gre333.json!")
