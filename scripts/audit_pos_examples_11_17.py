# -*- coding: utf-8 -*-
"""
Audits part of speech usage in example sentences for Words 201 to 333.
"""
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

words_11_to_17 = corpus[200:333]

pos_issues = []

for idx, w in enumerate(words_11_to_17, 201):
    word = w['word']
    pos = w['partOfSpeech']
    exs = w.get('examples', [])
    
    for i, ex in enumerate(exs, 1):
        en = ex.get('en', '')
        bn = ex.get('bn', '')
        
        # Verb checks: if pos == 'verb', check if word is used as a verb
        # Look for the word in the sentence
        pattern = re.compile(rf'\b{re.escape(word[:min(len(word), 4)])}[a-z]*\b', re.I)
        matches = pattern.findall(en)
        if not matches:
            pos_issues.append((idx, word, pos, f"Sentence {i} does not seem to contain headword: '{en}'"))
        else:
            match_word = matches[0].lower()
            # If word is verb, but matched word is e.g. ending in 'tion' or 'ance' (noun form!)
            if pos == 'verb' and (match_word.endswith('tion') or match_word.endswith('ment') or match_word.endswith('ance') or match_word.endswith('ence')):
                pos_issues.append((idx, word, pos, f"Sentence {i} uses NOUN form '{match_word}' for VERB headword: '{en}'"))
            # If word is noun, but matched word is e.g. ending in 'ing' or 'ed' used as verb
            # If word is adjective, but used as noun (e.g. ending in 'ity' or 'ness')
            elif pos == 'adjective' and (match_word.endswith('ness') or match_word.endswith('ity')):
                pos_issues.append((idx, word, pos, f"Sentence {i} uses NOUN form '{match_word}' for ADJ headword: '{en}'"))
            elif pos == 'noun' and match_word.endswith('ly') and len(match_word) > len(word):
                pos_issues.append((idx, word, pos, f"Sentence {i} uses ADVERB form '{match_word}' for NOUN headword: '{en}'"))

print(f"Total POS anomalies in example sentences: {len(pos_issues)}")
for p in pos_issues:
    print(f"[{p[0]}: {p[1]} ({p[2]})] {p[3]}")
