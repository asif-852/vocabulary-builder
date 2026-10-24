import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)[:200]

print("Checking part-of-speech usage in examples...")

issues = []

for d in data:
    word = d['word']
    pos = d['partOfSpeech']
    exs = d['examples']
    
    for i, ex in enumerate(exs):
        en = ex['en']
        bn = ex['bn']
        
        # Check if the word appears in en
        matches = list(re.finditer(r'\b' + re.escape(word) + r'\b', en, re.IGNORECASE))
        if not matches:
            # Maybe an inflected form like -ed, -ing, -s?
            # User said: "The sentences should take the base form of the word, if the word is a noun, the sentences should contain noun, if verb, then verb."
            inflected = list(re.finditer(r'\b' + re.escape(word[:-1] if word.endswith('e') else word) + r'(?:ed|ing|s|es|d)?\b', en, re.IGNORECASE))
            if not inflected:
                issues.append((d['id'], word, pos, f"Sentence {i+1} does not contain '{word}': {en}"))

print(f"Total base/inflected absence issues: {len(issues)}")
for iss in issues:
    print(iss)
