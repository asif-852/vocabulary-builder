import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

low_candidates = []

for idx, t in enumerate(corpus[:200]):
    t_syns = set(s.lower() for s in t.get('synonyms', []))
    t_syns.add(t['word'].lower())
    t_ants = set(a.lower() for a in t.get('antonyms', []))
    
    candidates = []
    for c in corpus:
        if c['partOfSpeech'] != t['partOfSpeech']:
            continue
        c_word = c['word'].lower()
        if c_word in t_syns or c_word in t_ants:
            continue
        c_syns = set(s.lower() for s in c.get('synonyms', []))
        c_ants = set(a.lower() for a in c.get('antonyms', []))
        if t_syns.intersection(c_syns) or t_ants.intersection(c_syns) or t_syns.intersection(c_ants):
            continue
        if t['word'].lower() in c['meaningEn'].lower() or c_word in t['meaningEn'].lower():
            continue
        candidates.append(c)
    if len(candidates) < 10:
        low_candidates.append((idx+1, t['word'], t['partOfSpeech'], len(candidates)))

print(f"Words with fewer than 10 zero-relation candidates in gre333: {len(low_candidates)}")
for lc in low_candidates:
    print(f"[{lc[0]}] {lc[1]} ({lc[2]}): {lc[3]} candidates")
