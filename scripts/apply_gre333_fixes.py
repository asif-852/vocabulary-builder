import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 1. Update Sanction
sanction_word = data[287]
assert sanction_word['word'] == 'Sanction'
sanction_word['partOfSpeech'] = 'verb'
if 'explanationEn' in sanction_word.get('sentenceCompletion', {}):
    sanction_word['sentenceCompletion']['explanationEn'] = "Sanction (verb) means to give formal and explicit approval or to impose a penalty."
print("Updated [288] Sanction: partOfSpeech -> 'verb'")

# 2. Update Plethora and Precarious meaningBn
plethora = data[244]
assert plethora['word'] == 'Plethora'
plethora['meaningBn'] = "আধিক্য বা অতিপ্রাচুর্য"
print("Updated [245] Plethora: meaningBn -> 'আধিক্য বা অতিপ্রাচুর্য'")

precarious = data[249]
assert precarious['word'] == 'Precarious'
precarious['meaningBn'] = "ঝুঁকিপূর্ণ বা অনির্ভরযোগ্য"
print("Updated [250] Precarious: meaningBn -> 'ঝুঁকিপূর্ণ বা অনির্ভরযোগ্য'")

# 3. Clean all Bijoy conjunct glitches across the dataset
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

replacements = 0

def clean_obj(obj):
    global replacements
    if isinstance(obj, str):
        res = obj
        for bad, good in patterns:
            if bad in res:
                res = res.replace(bad, good)
                replacements += 1
        return res
    elif isinstance(obj, list):
        return [clean_obj(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: clean_obj(v) for k, v in obj.items()}
    return obj

data = clean_obj(data)
print(f"Cleaned {replacements} occurrences of Bijoy patterns across data.")

with open('src/data/gre333.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Saved src/data/gre333.json successfully!")
