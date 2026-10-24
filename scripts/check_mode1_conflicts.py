import json
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

conflicts = []

for q_idx in range(200):
    target = corpus[q_idx]
    distractors = get_meaning_distractors(target, 3)
    
    target_syns = set([s.lower() for s in target.get('synonyms', [])] + [target['word'].lower()])
    
    for d in distractors:
        d_syns = set([s.lower() for s in d.get('synonyms', [])] + [d['word'].lower()])
        overlap = target_syns.intersection(d_syns)
        
        # Check if d is in target synonyms or shares synonyms
        if d['word'].lower() in target_syns:
            set_num = (q_idx // 20) + 1
            q_num = (q_idx % 20) + 1
            conflicts.append((set_num, q_num, target['word'], d['word'], "Direct synonym in distractors!", target['meaningEn'], d['meaningEn']))
        elif len(overlap) > 0:
            set_num = (q_idx // 20) + 1
            q_num = (q_idx % 20) + 1
            conflicts.append((set_num, q_num, target['word'], d['word'], f"Shared synonyms {overlap}", target['meaningEn'], d['meaningEn']))

print(f"Total potential synonym/duplicate conflicts in Mode 1: {len(conflicts)}\n")
for c in conflicts:
    print(f"Set {c[0]}, Q {c[1]}: Target '{c[2]}' vs Distractor '{c[3]}' [{c[4]}]")
    print(f"    Target def:     {c[5]}")
    print(f"    Distractor def: {c[6]}")
    print()
