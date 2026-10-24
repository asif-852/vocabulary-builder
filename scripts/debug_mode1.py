import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Set 10 is index 180 to 199 (words 181 to 200)
# Word 181 is Innocuous
target = data[180]
print(f"Target word: {target['word']} ({target['partOfSpeech']}) - {target['meaningEn']} / {target['meaningBn']}")

corpus = data
same_pos = [w for w in corpus if w['partOfSpeech'] == target['partOfSpeech'] and w['id'] != target['id'] and w['word'].lower() != target['word'].lower()]

seed = sum(ord(c) for c in target['word'])
shuffled = sorted(same_pos, key=lambda a: (ord(a['word'][0]) * seed) % 97)
distractors = shuffled[:3]
for d in distractors:
    print(f"Distractor: {d['word']} - {d['meaningEn']}")

rawOptions = [{'text': target['meaningEn'], 'isCorrect': True, 'word': target['word']}] + [{'text': d['meaningEn'], 'isCorrect': False, 'word': d['word']} for d in distractors]

seed_word = target['indexInSource']
final_options = sorted(rawOptions, key=lambda a: (ord(a['text'][0]) * 19 + seed_word) % 43)

print('\nFinal Options for Set 10 Q1:')
for idx, opt in enumerate(final_options):
    print(f"{chr(65+idx)}. {opt['text']} (isCorrect: {opt['isCorrect']}, word: {opt['word']})")
