import sys
sys.path.append('scripts')
from build_pure_random_mode3 import final_mode3_data, corpus

for idx in [1, 22, 107, 181, 194]:
    t = corpus[idx - 1]
    opts = final_mode3_data[idx]['options']
    print(f"=== Word [{idx}] {t['word']} ({t['partOfSpeech']}) - {t['meaningBn']} ===")
    print("  Correct Synonyms:")
    for o in [o for o in opts if o['isSynonym']]:
        print(f"    - {o['word']}: {o['meaningBn']}")
    print("  Purely Random Unrelated Distractors:")
    for o in [o for o in opts if not o['isSynonym']]:
        print(f"    - {o['word']}: {o['meaningBn']}")
    print()
