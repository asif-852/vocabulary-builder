# -*- coding: utf-8 -*-
"""
Repairs legacy Bijoy/OCR artifacts in Bengali meanings across gre333.json.
"""
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

text_replacements = {
    'দীিমান': 'দীপ্তিমান',
    'মিথ্যাাবাদী': 'মিথ্যাবাদী',
    'মানববিেষী': 'মানববিদ্বেষী',
    'লোকলজ্জাা': 'লোকলজ্জা',
    'চিরস্থায়ীী': 'চিরস্থায়ী',
    'বহুবষজীবী': 'বহুবর্ষজীবী',
    'বিশ্বাাসঘাতক': 'বিশ্বাসঘাতক',
    'সবব্যাাপী বা সবগ্রাসী': 'সর্বব্যাপী বা সর্বগ্রাসী',
    'হ্রাাস': 'হ্রাস',
    'দািক বা অনধিকারচর্চাকারী': 'দাম্ভিক বা অনধিকারচর্চাকারী',
    'অপব্যয়ীী': 'অপব্যয়ী',
    'পূবমত': 'পূর্বমত',
    'প্রত্যাাহার': ' প্রত্যাহার',
    'প্রত্যাাহৃত': 'প্রত্যাহৃত',
    'তিরস্কাার': 'তিরস্কার',
    'প্রত্যাাখ্যাান': 'প্রত্যাখ্যান',
    'প্রতিিত বা': 'প্রতিষ্ঠিত বা',
    'প্রতিিত': 'প্রতিষ্ঠিত',
    'নিিয়তা বা অবসাদ': 'নিষ্ক্রিয়তা বা অবসাদ',
    'িধাদ্বে দোলা বা অনিিত থাকা': 'দ্বিধাদ্বন্দ্বে দোলা বা অনিশ্চিত থাকা',
    'উদ্বায়ীী বা দ্রুত পরিবতনশীল ও বিস্\nফোরক': 'উদ্বায়ী বা দ্রুত পরিবর্তনশীল ও বিস্ফোরক',
    'উদ্বায়ীী বা দ্রুত পরিবতনশীল ও বিস্ফোরক': 'উদ্বায়ী বা দ্রুত পরিবর্তনশীল ও বিস্ফোরক',
    'ন্যাায্য': 'ন্যায্য',
    'খামখেয়াালী বা কাল্পনিক ও অদ্ভুুত': 'খামখেয়ালী বা কাল্পনিক ও অদ্ভুত',
    'অদ্ভুুত': 'অদ্ভুত',
    'প্রত্যাাহার করা বা ফিরিয়ে নেওয়া': 'বাতিল বা প্রত্যাহার করা',
    'প্রত্যাাহার করা': 'প্রত্যাহার করা',
    'বাতিল বা  প্রত্যাহার করা': 'বাতিল বা প্রত্যাহার করা',
}

changes = 0
for idx, w in enumerate(corpus):
    orig = w['meaningBn']
    new_bn = orig
    for k, v in text_replacements.items():
        if k in new_bn:
            new_bn = new_bn.replace(k, v)
    
    # Strip weird spaces or newlines
    new_bn = ' '.join(new_bn.split())
    
    # Clean double aakars or ee-kars
    new_bn = re.sub(r'া+', 'া', new_bn)
    new_bn = re.sub(r'ী+', 'ী', new_bn)
    new_bn = re.sub(r'ু+', 'ু', new_bn)
    new_bn = re.sub(r'ূ+', 'ূ', new_bn)
    new_bn = re.sub(r'ে+', 'ে', new_bn)
    
    if new_bn != orig:
        print(f"[{idx+1}: {w['word']}]: '{orig}' -> '{new_bn}'")
        w['meaningBn'] = new_bn
        changes += 1

with open('src/data/gre333.json', 'w', encoding='utf-8') as f:
    json.dump(corpus, f, ensure_ascii=False, indent=2)

print(f"Successfully cleaned {changes} words in gre333.json!")
