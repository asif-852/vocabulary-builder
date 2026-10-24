import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    gre_data = json.load(f)

# Let's inspect all 333 words
fixes_needed = {}

for idx, item in enumerate(gre_data):
    w = item['word']
    pos = item['partOfSpeech']
    m_en = item['meaningEn']
    m_bn = item['meaningBn']
    
    reasons = []
    
    # 1. Author citation or multiple semicolons
    if any(k in m_en for k in ['; ;', ';;', ' - ', '- c.b', '- robert', '- bruce', '- anita', '- samuel', '- sir walter', '- virginia', '- nordhoff']):
        reasons.append("Author attribution / multiple semicolons")
        
    # 2. Domain / parenthetical prefix
    if m_en.startswith('(') and ')' in m_en:
        reasons.append("Parenthetical prefix")
        
    # 3. Trailing semicolon / comma
    if m_en.endswith(';') or m_en.endswith(','):
        reasons.append("Trailing punctuation")
        
    # 4. Verb without 'To '
    if pos == 'verb' and not m_en.startswith('To '):
        reasons.append(f"Verb does not start with 'To ' (starts with: '{m_en[:15]}...')")
        
    # 5. Adjective with noun definition ('A...', 'An...', 'The...') or verb ('To...')
    if pos == 'adjective':
        if m_en.startswith('To '):
            reasons.append("Adjective starts with 'To '")
        elif m_en.startswith('A ') or m_en.startswith('An ') or m_en.startswith('The '):
            reasons.append(f"Adjective starts with noun article: '{m_en[:20]}...'")
            
    # 6. Noun starting with 'To '
    if pos == 'noun' and m_en.startswith('To '):
        reasons.append("Noun starts with 'To '")
        
    # 7. Overly long or historical/biological specific
    if idx + 1 in [210, 218, 248, 251, 252, 275, 300, 333]:
        reasons.append("Off-target / technical / historical definition")

    if reasons:
        fixes_needed[idx + 1] = {
            'word': w,
            'pos': pos,
            'current_meaningEn': m_en,
            'meaningBn': m_bn,
            'reasons': reasons
        }

print(f"Total entries in gre333.json requiring definition cleanup: {len(fixes_needed)}\n")
for id_num, info in sorted(fixes_needed.items()):
    print(f"[{id_num}] {info['word']} ({info['pos']}):")
    print(f"     Reasons: {', '.join(info['reasons'])}")
    print(f"     Current: {info['current_meaningEn']}")
