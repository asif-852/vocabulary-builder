import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

def fix_bengali_pronunciation(bn_str, en_str):
    if not bn_str:
        return ""
    
    t = bn_str
    # Common English-to-Bengali cluster substitutions inside phonetics
    substitutions = [
        ('str্যাkt', 'স্ট্র্যাক্ট'),
        ('strুশ', 'স্ট্রুশ'),
        ('st্যান', 'স্ট্যান'),
        ('stোল', 'স্টোল'),
        ('stিপ', 'স্টিপ'),
        ('stিন্ট', 'স্টিন্ট'),
        ('stাট', 'স্ট্রাট'),
        ('stি', 'স্টি'),
        ('st', 'স্ট'),
        ('kt', 'ক্ট'),
        ('brিজ', 'ব্রিজ'),
        ('br', 'ব্র'),
        ('lv', 'ল্ভ'),
        ('klেইম', 'ক্লেইম'),
        ('kl', 'ক্ল'),
        ('krু', 'ক্রু'),
        ('kr', 'ক্র'),
        ('kwিজ', 'কুইজ'),
        ('kwিট', 'কুইট'),
        ('kwেই', 'কোয়ে'),
        ('kwি', 'কুই'),
        ('kw', 'কোয়া'),
        ('plেই', 'প্লেই'),
        ('pl্যাট', 'প্ল্যাট'),
        ('plেথ', 'প্লেথ'),
        ('pl', 'প্ল'),
        ('pr্যাগ', 'প্র্যাগ'),
        ('prি', 'প্রি'),
        ('prিশ', 'প্রিস'),
        ('prোড', 'প্রড'),
        ('prা', 'প্রো'),
        ('prো', 'প্রো'),
        ('pr', 'প্র'),
        ('flেগ', 'ফ্লেগ'),
        ('fl', 'ফ্ল'),
        ('spি', 'স্পি'),
        ('spেক', 'স্পেক'),
        ('spা', 'স্পা'),
        ('sp', 'স্প'),
        ('fyুট', 'ফিউট'),
        ('fy', 'ফাই'),
        ('dyু', 'ডিউ'),
        ('dy', 'ডি'),
        ('ty', 'টাই'),
        ('vy', 'ভাই'),
        ('nts', 'ন্টস'),
        ('nss', 'ন্স'),
        ('nk', 'ংক'),
        ('sh', 'শ'),
        ('ch', 'চ'),
        ('th', 'থ'),
    ]
    for eng, bng in substitutions:
        t = t.replace(eng, bng)
        t = t.replace(eng.upper(), bng)

    # Any remaining single lowercase letters
    single_letters = {
        'a': 'আ', 'b': 'ব', 'c': 'ক', 'd': 'ড', 'e': 'ই', 'f': 'ফ',
        'g': 'গ', 'h': 'হ', 'i': 'ই', 'j': 'জ', 'k': 'ক', 'l': 'ল',
        'm': 'ম', 'n': 'ন', 'o': 'ও', 'p': 'প', 'q': 'ক', 'r': 'র',
        's': 'স', 't': 'ট', 'u': 'উ', 'v': 'ভ', 'w': 'ওয়', 'x': 'ক্স',
        'y': 'ই', 'z': 'জ'
    }
    for eng, bng in single_letters.items():
        t = re.sub(r'(?i)\b' + eng + r'\b', bng, t)
        t = t.replace(eng, bng)
        t = t.replace(eng.upper(), bng)
        
    return t

# Test on WS1
with open('src/data/wordsmart1.json', 'r', encoding='utf-8') as f:
    ws1 = json.load(f)

still_bad = 0
for w in ws1:
    fixed = fix_bengali_pronunciation(w.get('pronunciationBn', ''), w.get('pronunciationEn', ''))
    if re.search(r'[a-zA-Z]', fixed):
        still_bad += 1
        print(f"Still bad: {w['word']} -> orig: {w.get('pronunciationBn')} | fixed: {fixed}")

print(f"WS1 fixed! Remaining bad: {still_bad}/{len(ws1)}")
