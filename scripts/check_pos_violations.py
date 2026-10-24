import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)[:200]

print("Scanning for POS violations in 400 sentences across Sets 1-10...")

verb_as_noun_pattern = re.compile(r'\b(?:a|an|the|his|her|their|our|its|this|that)\s+(?:\w+\s+)?{word}\b', re.IGNORECASE)
noun_as_verb_pattern = re.compile(r'\b(?:to|will|would|can|could|should|must|did|does|do)\s+{word}\b', re.IGNORECASE)

flagged = []

for d in data:
    word = d['word']
    pos = d['partOfSpeech']
    
    for i, ex in enumerate(d['examples']):
        en = ex['en']
        bn = ex['bn']
        
        if pos == 'verb':
            # Check if verb is preceded by determiner/possessive: 'a/an/the/his/her/their <verb>'
            p = re.compile(r'\b(?:a|an|the|his|her|their|our|my|your|this|that|these|those)\s+(?:[a-z\-]+\s+)?' + re.escape(word) + r'\b', re.IGNORECASE)
            m = p.search(en)
            if m:
                # Exclude legitimate cases like gerunds or participial adjectives if any, but base verbs shouldn't have 'a clear <verb>'
                flagged.append((d['id'], word, pos, f"Sentence {i+1} might treat verb as noun: '{m.group(0)}'", en, bn))
                
        elif pos == 'noun':
            # Check if noun is preceded by modal/infinitive: 'to <noun>'
            p = re.compile(r'\b(?:to|will|would|shall|should|must|can|could|may|might|did|does|do)\s+' + re.escape(word) + r'\b', re.IGNORECASE)
            m = p.search(en)
            if m:
                flagged.append((d['id'], word, pos, f"Sentence {i+1} might treat noun as verb: '{m.group(0)}'", en, bn))
                
        elif pos == 'adjective':
            # Check if adjective is preceded by infinitive 'to <adj>' (without be/become/seem)
            p = re.compile(r'\b(?:to|will|would|shall|should|must|can|could)\s+' + re.escape(word) + r'\b', re.IGNORECASE)
            m = p.search(en)
            if m:
                flagged.append((d['id'], word, pos, f"Sentence {i+1} might treat adj as verb: '{m.group(0)}'", en, bn))

print(f"Total suspected POS violations: {len(flagged)}")
for f in flagged:
    print(f"\n[{f[0]}] {f[1]} ({f[2]}): {f[3]}")
    print(f"   EN: {f[4]}")
    print(f"   BN: {f[5]}")
