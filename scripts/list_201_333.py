import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)[200:]

for i, d in enumerate(data):
    print(f"{201+i}: {d['word']} ({d['partOfSpeech']}) -> en: '{d.get('pronunciationEn')}', bn: '{d.get('pronunciationBn')}'")
