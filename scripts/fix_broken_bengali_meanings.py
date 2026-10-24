import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

# Common broken conjuncts from old Bijoy/ANSI OCR:
# উেখ -> উল্লেখ
# সংখ্যাাবৃি -> সংখ্যাবৃদ্ধি
# আপাতদৃিতে -> আপাতদৃষ্টিতে
# বৃি -> বৃদ্ধি
# দৃি -> দৃষ্টি
# কাযকর -> কার্যকর
# পুংখানুপুংখ -> পুঙ্খানুপুঙ্খ
# উগ্রতা -> উগ্রতা

fixes = {
    "উেখ": "উল্লেখ",
    "সংখ্যাাবৃি": "সংখ্যাবৃদ্ধি",
    "আপাতদৃিতে": "আপাতদৃষ্টিতে",
    "কাযকর": "কার্যকর",
    "দৃিভঙ্গি": "দৃষ্টিভঙ্গি",
    "পূণতা": "পূর্ণতা",
    "পূণ": "পূর্ণ"
}

found = 0
for idx, w in enumerate(corpus):
    m_bn = w['meaningBn']
    for bad, good in fixes.items():
        if bad in m_bn:
            print(f"[{idx+1}] {w['word']}: '{m_bn}' -> fixing '{bad}' to '{good}'")
            w['meaningBn'] = m_bn.replace(bad, good)
            found += 1

print(f"Total broken conjunct fixes applied: {found}")

with open('src/data/gre333.json', 'w', encoding='utf-8') as f:
    json.dump(corpus, f, ensure_ascii=False, indent=2)
