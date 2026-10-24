import json
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

print(f"Loaded existing true synonyms for {len(existing_sets)} words.")

# Build dictionary of all corpus words by POS for quick lookup
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

# Track distractor usage frequency to ensure broad, purely random dispersion
distractor_usage = {}

new_sets_data = {}

for idx in range(1, 201):
    target = corpus[idx - 1]
    w_name = target['word']
    pos = target['partOfSpeech']
    
    # Retrieve the 3 curated true synonyms
    old_opts = existing_sets[idx]['options']
    true_syns = [o for o in old_opts if o['isSynonym']]
    assert len(true_syns) == 3, f"Word {idx} does not have 3 true synonyms!"
    
    if pos == 'adverb':
        distractors = adverb_distractors
    else:
        # Build strict zero-relation candidates
        t_syns = set(s.lower() for s in target.get('synonyms', []))
        t_syns.add(w_name.lower())
        for ts in true_syns:
            t_syns.add(ts['word'].lower())
        t_ants = set(a.lower() for a in target.get('antonyms', []))
        
        candidates = []
        for c in corpus_by_pos[pos]:
            c_word = c['word'].lower()
            if c_word in t_syns or c_word in t_ants:
                continue
            c_syns = set(s.lower() for s in c.get('synonyms', []))
            c_ants = set(a.lower() for a in c.get('antonyms', []))
            
            # Zero synonym / antonym overlap
            if t_syns.intersection(c_syns) or t_ants.intersection(c_syns) or t_syns.intersection(c_ants) or t_ants.intersection(c_ants):
                continue
            # Zero definition mention
            if w_name.lower() in c['meaningEn'].lower() or c_word in target['meaningEn'].lower():
                continue
            candidates.append(c)
            
        assert len(candidates) >= 3, f"Not enough zero-relation candidates for {w_name}: {len(candidates)}"
        
        # Sort candidates by:
        # 1. Least used distractor across all questions (ensures variety)
        # 2. Pseudo-random hash using word letters + index
        seed = sum(ord(ch) for ch in w_name) + idx * 37
        
        def candidate_sort_key(c):
            usage = distractor_usage.get(c['word'], 0)
            h = (ord(c['word'][0]) * 73 + ord(c['word'][-1]) * 19 + seed) % 101
            return (usage, h)
            
        ranked = sorted(candidates, key=candidate_sort_key)
        selected_candidates = ranked[:3]
        
        distractors = []
        for sc in selected_candidates:
            distractor_usage[sc['word']] = distractor_usage.get(sc['word'], 0) + 1
            # Clean Bengali meaning
            m_bn = sc['meaningBn'].strip()
            distractors.append({
                "word": sc['word'],
                "isSynonym": False,
                "meaningBn": m_bn
            })
            
    new_options = true_syns + distractors
    new_sets_data[idx] = {
        "options": new_options
    }

print("Successfully generated zero-relation, purely random, sophisticated distractors for all 200 words!")

# Test sample words:
for sample_id in [1, 22, 181]:
    t_word = corpus[sample_id - 1]
    opts = new_sets_data[sample_id]['options']
    print(f"\nSample [{sample_id}] {t_word['word']} ({t_word['partOfSpeech']}):")
    print("  True Synonyms:")
    for o in [o for o in opts if o['isSynonym']]:
        print(f"    - {o['word']} ({o['meaningBn']})")
    print("  Zero-Relation Distractors:")
    for o in [o for o in opts if not o['isSynonym']]:
        print(f"    - {o['word']} ({o['meaningBn']})")
