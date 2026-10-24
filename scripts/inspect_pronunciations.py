import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== CHECKING GRE 333 (first 40) ===")
with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    gre = json.load(f)

for d in gre[:40]:
    print(f"{d['id']} {d['word']} ({d['partOfSpeech']}): EN='{d.get('pronunciationEn')}' | BN='{d.get('pronunciationBn')}'")

print("\n=== CHECKING WORDSMART 1 (first 20) ===")
with open('src/data/wordsmart1.json', 'r', encoding='utf-8') as f:
    ws1 = json.load(f)

for d in ws1[:20]:
    print(f"{d['id']} {d['word']} ({d['partOfSpeech']}): EN='{d.get('pronunciationEn')}' | BN='{d.get('pronunciationBn')}'")

print("\n=== CHECKING WORDSMART 2 (first 20) ===")
with open('src/data/wordsmart2.json', 'r', encoding='utf-8') as f:
    ws2 = json.load(f)

for d in ws2[:20]:
    print(f"{d['id']} {d['word']} ({d['partOfSpeech']}): EN='{d.get('pronunciationEn')}' | BN='{d.get('pronunciationBn')}'")
