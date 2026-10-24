import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("Checking Words 201 to 333 (Sets 11 to 17):")
for idx in range(200, 333):
    w = d[idx]
    pos = w['partOfSpeech']
    men = w['meaningEn']
    word = w['word']
    i = w['indexInSource']
    
    # 1. Check POS phrasing
    if pos == 'verb' and not men.startswith('To '):
        print(f"VERB NOT TO: [{i}] {word}: {men}")
    if pos == 'noun' and men.startswith('To '):
        print(f"NOUN STARTS TO: [{i}] {word}: {men}")
    if pos == 'adjective' and men.startswith('To '):
        print(f"ADJ STARTS TO: [{i}] {word}: {men}")
        
    # 2. Check trailing punctuation or semicolon
    if men.endswith(';') or men.endswith(','):
        print(f"TRAILING PUNCT: [{i}] {word}: {men}")
    if not men.endswith('.'):
        print(f"NO PERIOD AT END: [{i}] {word}: {men}")
        
    # 3. Check author names / quotation artifacts
    if any(q in men.lower() for q in [' - ', ';;', '; ;', 'vol.', 'ibid', 'c.b.', 'thoreau', 'emerson', 'scott', 'shakespeare']):
        print(f"AUTHOR/ARTIFACT: [{i}] {word}: {men}")
        
    # 4. Check double spaces or weird chars
    if '  ' in men:
        print(f"DOUBLE SPACE: [{i}] {word}: {men}")
    if any(c in men for c in ['[', ']', '{', '}', '<', '>', '~', '`', '_', '@', '#', '$', '%', '^', '*', '+', '=']):
        print(f"SPECIAL CHARS: [{i}] {word}: {men}")
        
    # 5. Check Bangla meaning for Bijoy/broken characters
    mbn = w['meaningBn']
    if any(glitch in mbn for glitch in ['কাযকর', 'উেখ', 'পূণ', 'সংখ্যাাবৃি', 'দািক', 'সেহ', 'িধাদ্বে', 'নিিয়তা', 'দীিমান', 'মানববিেষী', 'বহুবষজীবী', 'অনিভরযোগ্য', 'অতিপ্রাচুয']):
        print(f"BANGLA GLITCH: [{i}] {word}: {mbn}")
        
    # Check duplicate diacritics in Bangla
    if any(dup in mbn for dup in ['াা', 'ীী', 'ুু', 'ূূ', 'েে']):
        print(f"BANGLA DUP DIACRITIC: [{i}] {word}: {mbn}")

print("\nDone scanning words 201-333.")
