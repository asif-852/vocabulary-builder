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

fixes_count = 0

def replace_in_obj(obj):
    global fixes_count
    if isinstance(obj, str):
        res = obj
        for bad, good in patterns:
            if bad in res:
                res = res.replace(bad, good)
                fixes_count += 1
        return res
    elif isinstance(obj, list):
        return [replace_in_obj(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: replace_in_obj(v) for k, v in obj.items()}
    return obj

d_clean = replace_in_obj(d)
print(f"Total pattern replacements across gre333.json: {fixes_count}")
