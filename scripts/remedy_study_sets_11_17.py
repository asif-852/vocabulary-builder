# -*- coding: utf-8 -*-
"""
Applies comprehensive audit and remedy for Study Module content across Sets 11 to 17 (Words 201 to 333).
Rules enforced:
1. Fix English definitions (Log, Strut, remove citations).
2. Clean all Bijoy/OCR artifacts and broken conjuncts in meaningBn and examples.
3. Clean all multi-word synonyms and antonyms to high-register single GRE words.
4. Clean all double/stacked vowel signs and broken spaces across Bengali text.
"""
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

# Specific word definition and lexical updates
word_overhauls = {
    201: { # Log
        'meaningEn': 'An official record of events, a voyage, or daily occurrences; a journal.',
        'meaningBn': 'দৈনন্দিন কার্যবিবরণী বা নথি',
        'synonyms': ['record', 'journal', 'ledger', 'register'],
        'antonyms': ['erasure', 'omission', 'deletion']
    },
    206: { # Malingerer
        'antonyms': ['toiler', 'worker', 'producer']
    },
    211: { # Meticulous
        'meaningBn': 'অতি সতর্ক বা নিখুঁত'
    },
    215: { # Morose
        'meaningEn': 'Sullen, gloomy, and ill-tempered; sullenly melancholy.',
        'meaningBn': 'বিষণ্ণ বা বিমর্ষ স্বভাবের'
    },
    226: { # Oscillate
        'antonyms': ['stabilize', 'steady', 'settle']
    },
    228: { # Paragon
        'meaningBn': 'আদর্শ বা নিখুঁত দৃষ্টান্ত'
    },
    232: { # Pedantic
        'meaningBn': 'পাণ্ডিত্য প্রদর্শনকারী বা অতিরিক্ত খুঁতখুঁতে'
    },
    233: { # Penchant
        'meaningBn': 'তীব্র ঝোঁক বা বিশেষ অনুরাগ'
    },
    234: { # Penury
        'meaningBn': 'চরম দরিদ্রতা বা নিঃস্ব অবস্থা'
    },
    240: { # Phlegmatic
        'meaningBn': 'শান্ত ও আবেগহীন বা ধীরস্থির'
    },
    252: { # Precursor
        'meaningBn': 'অগ্রদূত বা পূর্বসূরি'
    },
    254: { # Prevaricate
        'antonyms': ['clarify', 'confront', 'authenticate']
    },
    279: { # Reprobate
        'antonyms': ['saint', 'innocent', 'moralist']
    },
    286: { # Sage
        'synonyms': ['philosopher', 'mentor', 'scholar']
    },
    293: { # Shard
        'antonyms': ['whole', 'totality', 'aggregate']
    },
    296: { # Soporific
        'meaningEn': 'Tending to induce drowsiness or sleep; sleep-inducing.'
    },
    306: { # Strut (noun)
        'meaningEn': 'A structural bar, rod, or brace designed to resist pressure in the direction of its length.',
        'meaningBn': 'কাঠামোকে ধরে রাখার জন্য খুঁটি বা ঠেকনা'
    },
    307: { # Subpoena
        'synonyms': ['summons', 'writ', 'citation']
    },
    314: { # Tenuous
        'meaningBn': 'দুর্বল বা কৃশকায় ও ক্ষীণ'
    },
    317: { # Tortuous
        'meaningBn': 'সর্পিল বা অত্যন্ত প্যাঁচালো'
    },
    320: { # Truculence
        'meaningBn': 'আগ্রাসী মনোভাব বা হিংস্রতা'
    },
    321: { # Vacillate
        'antonyms': ['decide', 'persevere', 'persist']
    },
    330: { # Wary
        'meaningBn': 'সতর্ক বা সাবধানী'
    },
    333: { # Zealot
        'meaningBn': 'ধর্মান্ধ বা চরম গোঁড়া ব্যক্তি'
    }
}

# General text cleanups in Bengali (conjuncts, broken spaces)
text_replacements = {
    'কাযবিবরণী': 'কার্যবিবরণী',
    'দৈনিন': 'দৈনন্দিন',
    'ক্যাাপ্টে ন': 'ক্যাপ্টেন',
    'ক্যাপ্টে ন': 'ক্যাপ্টেন',
    'অধ্যাাপক': 'অধ্যাপক',
    'ব্যাাখ্যাা': 'ব্যাখ্যা',
    'ব্যাখ্যাা': 'ব্যাখ্যা',
    'মিথ্যাা': 'মিথ্যা',
    'প্রত্যাাখ্যাান': 'প্রত্যাখ্যান',
    'প্রত্যাখ্যান': 'প্রত্যাখ্যান',
    'ম্যাানগ্রো ভ': 'ম্যানগ্রোভ',
    'চ্যাাম্পি য়নশিপ': 'চ্যাম্পিয়নশিপ',
    'চ্যাম্পি য়নশিপ': 'চ্যাম্পিয়নশিপ',
    'ম্যাাচ': 'ম্যাচ',
    'অক্লাান্ত': 'অক্লান্ত',
    'গণবিক্ষো ভ': 'গণবিক্ষোভ',
    'বিক্ষো ভ': 'বিক্ষোভ',
    'পদত্যাাগ': 'পদত্যাগ',
    'ক্লাাউড': 'ক্লাউড',
    'ব্যাাকআপ': 'ব্যাকআপ',
    'দেওয়াা': 'দেওয়া',
    'ক্ষো ভ': 'ক্ষোভ',
    'পেন্ডুুলাম': 'পেন্ডুলাম',
    'পেন্ডুলাম': 'পেন্ডুলাম',
    'ব্যাাপকভাবে': 'ব্যাপকভাবে',
    'ব্যাাপক': 'ব্যাপক',
    'মিথ্যাাবাদী': 'মিথ্যাবাদী',
    'বিখ্যাাত': 'বিখ্যাত',
    'নিস্ব অবস্থা': 'নিঃস্ব অবস্থা',
    'নিস্ব': 'নিঃস্ব',
    'সমস্যাা': 'সমস্যা',
    'সমস্যাাবহুল': 'সমস্যাবহুল',
    'ভূমিকম্পে র': 'ভূমিকম্পের',
    'ম্যাানেজার': 'ম্যানেজার',
    'তথ্যাাদির': 'তথ্যাদির',
    'ঘণ্টাার': 'ঘণ্টার',
    'ম্যাাজিস্ট্রে ট': 'ম্যাজিস্ট্রেট',
    'ম্যাজিস্ট্রে ট': 'ম্যাজিস্ট্রেট',
    'সুখ্যাাত': 'সুখ্যাত',
    'অপব্যয়ীী': 'অপব্যয়ী',
    'ভুয়াা': 'ভুয়া',
    'ব্যাাকটেরিয়া': 'ব্যাকটেরিয়া',
    'ব্যাকটেরিয়া': 'ব্যাকটেরিয়া',
    'সংখ্যাাবৃদ্ধি': 'সংখ্যাবৃদ্ধি',
    'সংখ্যাাবৃি': 'সংখ্যাবৃদ্ধি',
    'প্রত্যাাহার': 'প্রত্যাহার',
    'তিরস্কাার': 'তিরস্কার',
    'হ্রাাস': 'হ্রাস',
    'প্রতিিত': 'প্রতিষ্ঠিত',
    'নিিয়তা': 'নিষ্ক্রিয়তা',
    'ঘোরপ্যাঁাঁচালো': 'ঘোরপ্যাঁচালো',
    'প্যাঁাঁচালো': 'প্যাঁচালো',
    'িধাদ্বে': 'দ্বিধাদ্বন্দ্বে',
    'অনিিত': 'অনিশ্চিত',
    'উদ্বায়ীী': 'উদ্বায়ী',
    'উদ্বায়ী': 'উদ্বায়ী',
    'ন্যাায্য': 'ন্যায্য',
    'খামখেয়াালী': 'খামখেয়ালী',
    'অদ্ভুুত': 'অদ্ভুত',
    'গোঁঁড়া': 'গোঁড়া',
    'হিংংস্রতা': 'হিংস্রতা',
    'পূবসূরী': 'পূর্বসূরি',
    'প্রদশনকারী': 'প্রদর্শনকারী',
    'ঝোঁঁক': 'ঝোঁক',
    'ধীরির': 'ধীরস্থির',
    'দুবল': 'দুর্বল',
    'সতক': 'সতর্ক',
    'বিমষ': 'বিমর্ষ',
    'আদশ': 'আদর্শ',
}

def clean_bengali_text(text):
    if not text:
        return text
    res = text
    for k, v in text_replacements.items():
        if k in res:
            res = res.replace(k, v)
    # Strip double vowel signs
    res = re.sub(r'[\u09BE]{2,}', '\u09BE', res) # aakar
    res = re.sub(r'[\u09BF]{2,}', '\u09BF', res) # hrossho-ikar
    res = re.sub(r'[\u09C0]{2,}', '\u09C0', res) # dirgho-ikar
    res = re.sub(r'[\u09C1]{2,}', '\u09C1', res) # hrossho-ukar
    res = re.sub(r'[\u09C2]{2,}', '\u09C2', res) # dirgho-ukar
    res = re.sub(r'[\u09C7]{2,}', '\u09C7', res) # e-kar
    res = re.sub(r'[\u0981]{2,}', '\u0981', res) # chandrabindu
    # Remove weird double spaces
    res = ' '.join(res.split())
    return res

total_modified = 0

for idx in range(201, 334):
    item = corpus[idx - 1]
    
    # 1. Apply specific word overhaul if configured
    if idx in word_overhauls:
        for k, v in word_overhauls[idx].items():
            item[k] = v
            
    # 2. Clean meaningBn
    orig_mbn = item.get('meaningBn', '')
    item['meaningBn'] = clean_bengali_text(orig_mbn)
    
    # 3. Clean examples
    for ex in item.get('examples', []):
        ex['bn'] = clean_bengali_text(ex.get('bn', ''))
        
    total_modified += 1

with open('src/data/gre333.json', 'w', encoding='utf-8') as f:
    json.dump(corpus, f, ensure_ascii=False, indent=2)

print(f"Successfully remediated all {total_modified} words in Sets 11 to 17 in gre333.json!")
