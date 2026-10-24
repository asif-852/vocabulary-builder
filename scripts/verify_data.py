import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

datasets = [
    ('src/data/gre333.json', 333, 17, 20),
    ('src/data/wordsmart1.json', 833, 34, 25),
    ('src/data/wordsmart2.json', 848, 34, 25)
]

for path, exp_words, exp_sets, per_set in datasets:
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    print(f"\n--- Checking {path} ---")
    print(f"Total words: {len(data)} (expected {exp_words})")
    assert len(data) == exp_words, f"Expected {exp_words} words, got {len(data)}"
    
    # Check sets
    sets = {}
    for w in data:
        s = w['setNumber']
        sets[s] = sets.get(s, 0) + 1
        
    print(f"Total sets: {len(sets)} (expected {exp_sets})")
    assert len(sets) == exp_sets, f"Expected {exp_sets} sets, got {len(sets)}"
    
    # Check set sizes
    for s_idx in range(1, exp_sets):
        assert sets[s_idx] == per_set, f"Set {s_idx} has {sets[s_idx]} words, expected {per_set}"
        
    last_set_size = sets[exp_sets]
    print(f"Sets 1 to {exp_sets - 1} each have {per_set} words. Last Set {exp_sets} has {last_set_size} words.")
    
    # Validate each entry
    for i, w in enumerate(data):
        assert w['id'], f"Missing id in word #{i}"
        assert w['word'], f"Missing word in word #{i}"
        assert w['partOfSpeech'] in ['verb', 'noun', 'adjective', 'adverb'], f"Invalid POS {w['partOfSpeech']} in word #{i}"
        assert w['pronunciationEn'], f"Missing pronunciationEn in word #{i}"
        assert w['pronunciationBn'], f"Missing pronunciationBn in word #{i}"
        assert w['meaningBn'], f"Missing meaningBn in word #{i}"
        assert w['meaningEn'], f"Missing meaningEn in word #{i}"
        assert len(w['synonyms']) >= 3, f"Need >=3 synonyms, got {len(w['synonyms'])} in word #{i} ({w['word']})"
        assert len(w['antonyms']) >= 3, f"Need >=3 antonyms, got {len(w['antonyms'])} in word #{i} ({w['word']})"
        assert len(w['examples']) == 2, f"Need 2 examples in word #{i}"
        assert w['examples'][0]['en'] and w['examples'][0]['bn'], f"Empty example 1 in word #{i}"
        assert w['examples'][1]['en'] and w['examples'][1]['bn'], f"Empty example 2 in word #{i}"
        
        sc = w['sentenceCompletion']
        assert '_____' in sc['sentenceWithBlank'] or '____' in sc['sentenceWithBlank'], f"Sentence completion blank missing in word #{i}"
        assert len(sc['options']) == 5, f"Expected 5 options in word #{i}"
        assert 0 <= sc['correctIndex'] <= 4, f"Invalid correctIndex in word #{i}"
        assert len(sc['optionMeaningsBn']) == 5, f"Expected 5 option meanings in word #{i}"
        assert sc['explanationEn'], f"Empty explanationEn in word #{i}"
        
    print(f"Sample word from {path}: {data[0]['word']} ({data[0]['partOfSpeech']}) - {data[0]['meaningBn']}")
    print(f"PASSED schema check for {path}!")

print("\nALL 2,014 WORDS ACROSS ALL 3 DATASETS ARE 100% VALIDATED!")
