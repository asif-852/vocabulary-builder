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
    ('সেহ', 'সন্দেহ'),
    ('িধাদ্বে', 'দ্বিধাদ্বন্দ্বে'),
    ('নিিয়তা', 'নিষ্ক্রিয়তা'),
    ('দীিমান', 'দীপ্তিমান'),
    ('মানববিেষী', 'মানববিদ্বেষী'),
    ('বহুবষজীবী', 'বহুবর্ষজীবী'),
    ('নিস্ব', 'নিঃস্ব'),
]

for idx, w in enumerate(d):
    i = w['indexInSource']
    s = w['setNumber']
    text = json.dumps(w, ensure_ascii=False)
    for bad, good in patterns:
        if bad in text:
            print(f"Set {s} | [{i}] {w['word']}: found '{bad}' -> '{good}'")
