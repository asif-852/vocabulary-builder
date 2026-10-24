import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)[:200]

# Patterns where space occurs right before a kar, or after 'ি', 'ে', 'ো' when it splits a word
# Or space followed by single consonant letter at end of word like "হচ্ছি ল" -> "হচ্ছিল"
patterns = [
    re.compile(r'([ক-হ]ি)\s+([ক-হ])'), # e.g. ক্রি য়া -> ক্রিয়া, কম্পি উটার -> কম্পিউটার, অনুচক্রি কা -> অনুচক্রিকা
    re.compile(r'([ক-হ]ে)\s+([ক-হ])'), # e.g. স্প্রে ড -> স্প্রেড
    re.compile(r'([ক-হ]ো)\s+([ক-হ])'), # e.g. উন্মো চনে -> উন্মোচনে
    re.compile(r'([ক-হ]্[ক-হ]ি)\s+([ক-হ])'), # e.g. হচ্ছি ল -> হচ্ছিল
    re.compile(r'\s+([িীুূৃেৈোৌ])'), # orphan kar preceded by space
]

candidates = set()
for d in data:
    for ex in d['examples']:
        bn = ex['bn']
        for p in patterns:
            for m in p.finditer(bn):
                # check if m.group(0) is a real split or two legitimate separate words
                # print snippet
                start = max(0, m.start() - 5)
                end = min(len(bn), m.end() + 5)
                candidates.add((d['id'], d['word'], m.group(0), bn[start:end]))

print(f"Total candidate matches: {len(candidates)}")
for c in sorted(candidates):
    print(c)
