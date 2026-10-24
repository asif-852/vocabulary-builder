# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

words_11_to_17 = corpus[200:333]

reph_words = [
    ('সতক', 'সতর্ক'),
    ('বিমষ', 'বিমর্ষ'),
    ('আদশ', 'আদর্শ'),
    ('দুবল', 'দুর্বল'),
    ('কায', 'কার্য'),
    ('বষ', 'বর্ষ'),
    ('পূব', 'পূর্ব'),
    ('প্যাঁাঁচালো', 'প্যাঁচালো'),
    ('হিংংস্রতা', 'হিংস্রতা'),
    ('গোঁঁড়া', 'গোঁড়া'),
    ('দৈনিন', 'দৈনন্দিন'),
    ('সেহ', 'সন্দেহ'),
    ('উেখ', 'উল্লেখ'),
    ('পূণ', 'পূর্ণ'),
    ('সংখ্যাাবৃি', 'সংখ্যাবৃদ্ধি'),
    ('দািক', 'দাম্ভিক'),
    ('নিস্ব', 'নিঃস্ব'),
    ('বিখ্যাাত', 'বিখ্যাত'),
]

for idx, w in enumerate(words_11_to_17, 201):
    texts = [w['meaningBn']] + [ex.get('bn', '') for ex in w.get('examples', [])]
    for t in texts:
        for bad, good in reph_words:
            if bad in t:
                print(f"[{idx}: {w['word']}] Found '{bad}' -> should be '{good}': in '{t}'")
