import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

print("Checking words 1 to 200 for any awkwardness, typos, or inaccuracies:\n")

for i in range(200):
    w = corpus[i]
    m_en = w['meaningEn']
    m_bn = w['meaningBn']
    pos = w['partOfSpeech']
    word = w['word']
    
    # Check if definition starts with capital
    if not m_en[0].isupper() and not m_en.startswith('('):
        print(f"[{i+1}] {word} ({pos}): does not start with capital: '{m_en}'")
        
    # Check for odd characters
    if any(c in m_en for c in ['@', '#', '$', '%', '^', '*', '_', '~', '<', '>', '{', '}', '[', ']']):
        print(f"[{i+1}] {word} ({pos}): strange symbols: '{m_en}'")
        
    # Check POS alignment
    if pos == 'verb' and not (m_en.startswith('To ') or m_en.startswith('Cause ') or m_en.startswith('Make ') or m_en.startswith('Be ') or m_en.startswith('Reduce ')):
        print(f"[{i+1}] {word} ({pos}): Verb meaning without 'To...': '{m_en}'")
    elif pos == 'noun' and m_en.startswith('To '):
        print(f"[{i+1}] {word} ({pos}): Noun meaning with 'To...': '{m_en}'")
    elif pos == 'adjective' and (m_en.startswith('To ') or m_en.startswith('A ') or m_en.startswith('An ') or m_en.startswith('The ')):
        print(f"[{i+1}] {word} ({pos}): Adjective meaning with 'To...' or 'A/An/The': '{m_en}'")
