import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total words: {len(data)}")

suspicious = []

for idx, w in enumerate(data):
    m_en = w['meaningEn']
    m_bn = w['meaningBn']
    pos = w['partOfSpeech']
    word = w['word']
    
    # Check for weird characters, multiple semicolons, dashes with names, etc.
    if re.search(r';\s*;\s*;', m_en):
        suspicious.append((idx+1, word, pos, "Multiple semicolons", m_en))
    elif re.search(r'-\s*[a-z\.]+', m_en):
        suspicious.append((idx+1, word, pos, "Dashes with name/tag", m_en))
    elif len(m_en.strip()) < 5:
        suspicious.append((idx+1, word, pos, "Too short", m_en))
    elif re.search(r'[\(\)]', m_en) and ('see' in m_en.lower() or 'c.b' in m_en.lower()):
        suspicious.append((idx+1, word, pos, "Odd citation/note", m_en))
    elif any(c in m_en for c in ['@', '#', '$', '%', '^', '*', '_', '~', '<', '>', '{', '}', '[', ']']):
        suspicious.append((idx+1, word, pos, "Weird symbols", m_en))

print(f"Found {len(suspicious)} suspicious entries by regex:")
for s in suspicious:
    print(f"[{s[0]}] {s[1]} ({s[2]}): {s[3]} -> {s[4]}")
