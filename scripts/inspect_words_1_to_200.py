import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/raw_gre333.json', encoding='utf-8') as f:
    raw = json.load(f)

for s in range(1, 11):
    set_words = raw[(s-1)*20 : s*20]
    word_list = [f"{w['index']}. {w['word']}" for w in set_words]
    print(f"Set {s}: {', '.join(word_list)}")
