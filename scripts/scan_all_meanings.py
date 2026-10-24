import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for idx, w in enumerate(data):
    m_en = w['meaningEn']
    m_bn = w['meaningBn']
    word = w['word']
    pos = w['partOfSpeech']
    
    # Check for:
    # 1. Trailing or double semicolons
    # 2. Lowercase start
    # 3. Missing period or weird ending
    # 4. Any mention of authors or hyphens with spaces
    # 5. Very short or very long
    # 6. Mismatched POS in definition (e.g. verb meaning for noun, etc.)
    issues = []
    if ';;' in m_en or '; ;' in m_en:
        issues.append("Double/multiple semicolons")
    if re.search(r'-\s*[a-z]', m_en):
        issues.append("Author attribution / dash lowercase")
    if m_en.endswith(';'):
        issues.append("Ends with semicolon")
    if not m_en[0].isupper() and not m_en.startswith('('):
        issues.append("Does not start with capital")
    if len(m_en.split()) > 25:
        issues.append("Overly long definition (>25 words)")
    if len(m_en.split()) < 3:
        issues.append("Very short definition (<3 words)")
        
    if issues:
        print(f"[{idx+1}] {word} ({pos}): {', '.join(issues)}")
        print(f"     meaningEn: {m_en}")
