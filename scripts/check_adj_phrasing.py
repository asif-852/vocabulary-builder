import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("Checking noun vs adjective phrasing in Words 201 to 333:")
for idx in range(200, 333):
    w = d[idx]
    i = w['indexInSource']
    word = w['word']
    pos = w['partOfSpeech']
    men = w['meaningEn']
    
    if pos == 'adjective':
        # Check if starts with "A " or "An " or "The "
        if men.startswith('A ') or men.startswith('An ') or men.startswith('The '):
            print(f"[{i}] {word} (adjective): starts with article: {men}")
    elif pos == 'noun':
        # Check if doesn't start with article or noun indicator
        # Typically nouns start with A, An, The, Someone, One, The state, The quality, etc.
        pass
