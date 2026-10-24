import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("INSPECTING WORDS 201 to 333:")
for idx in range(200, 333):
    w = d[idx]
    i = w['indexInSource']
    word = w['word']
    pos = w['partOfSpeech']
    men = w['meaningEn']
    mbn = w['meaningBn']
    
    # print all
    print(f"{i:3d}. {word:16s} ({pos:9s}) -> {men}")
