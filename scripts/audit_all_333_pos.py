import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("Auditing all 333 words in gre333.json:")
for idx, w in enumerate(d):
    i = w['indexInSource']
    word = w['word']
    pos = w['partOfSpeech']
    men = w['meaningEn']
    mbn = w['meaningBn']
    
    # Check POS alignment
    if pos == 'verb' and not men.startswith('To '):
        print(f"[{i}] {word} ({pos}): verb def does not start with 'To ': {men}")
    elif pos == 'noun' and men.startswith('To '):
        print(f"[{i}] {word} ({pos}): noun def starts with 'To ': {men}")
    elif pos == 'adjective' and men.startswith('To '):
        print(f"[{i}] {word} ({pos}): adj def starts with 'To ': {men}")
