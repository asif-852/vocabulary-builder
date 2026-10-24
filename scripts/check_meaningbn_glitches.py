import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

patterns = [
    ('অতিপ্রাচুয', 'অতিপ্রাচুর্য'),
    ('অনিভরযোগ্য', 'অনির্ভরযোগ্য'),
    ('কাযকর', 'কার্যকর'),
    ('উেখ', 'উল্লেখ'),
    ('পূণ', 'পূর্ণ'),
    ('সংখ্যাাবৃি', 'সংখ্যাবৃদ্ধি'),
    ('দািক', 'দাম্ভিক'),
    ('সেহপ্রবণ', 'সন্দেহপ্রবণ'),
    ('সেহজনক', 'সন্দেহজনক'),
    ('সেহ', 'সন্দেহ'),
    ('িধাদ্বে', 'দ্বিধাদ্বন্দ্বে'),
    ('নিিয়তা', 'নিষ্ক্রিয়তা'),
    ('দীিমান', 'দীপ্তিমান'),
    ('মানববিেষী', 'মানববিদ্বেষী'),
    ('বহুবষজীবী', 'বহুবর্ষজীবী'),
    ('নিস্ব', 'নিঃস্ব'),
]

for idx in range(200, 333):
    w = d[idx]
    i = w['indexInSource']
    mbn = w['meaningBn']
    for bad, good in patterns:
        if bad in mbn:
            print(f"meaningBn: [{i}] {w['word']}: '{bad}' in '{mbn}' -> '{good}'")
