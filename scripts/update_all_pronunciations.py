import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Dictionary for GRE 333 words 201 to 333: (pron_en, pron_bn, pos)
GRE_201_333_PRON = {
    201: ('LOG', 'লগ', 'noun'),
    202: ('loh-KWAY-shus', 'লো-কোয়ে-শাস', 'adjective'),
    203: ('LOO-sid', 'লু-সিড', 'adjective'),
    204: ('LOO-muh-nus', 'লু-মি-নাস', 'adjective'),
    205: ('mag-nuh-NIM-ih-tee', 'ম্যাগ-না-নিম-ই-টি', 'noun'),
    206: ('muh-LING-ger-er', 'মা-লিং-গার-আর', 'noun'),
    207: ('MAL-ee-uh-bul', 'ম্যাল-ই-আ-বাল', 'adjective'),
    208: ('MAV-er-ik', 'ম্যাভ-আর-ইক', 'noun'),
    209: ('men-DAY-shus', 'মেন-ডেই-শাস', 'adjective'),
    210: ('met-uh-MOR-fuh-sis', 'মেট-আ-মর-ফা-সিস', 'noun'),
    211: ('muh-TIK-yuh-lus', 'মা-টিক-ইউ-লাস', 'adjective'),
    212: ('MIS-un-throhp', 'মিস-আন-থ্রোপ', 'noun'),
    213: ('MIT-uh-gayt', 'মিট-ই-গেইট', 'verb'),
    214: ('MOL-uh-fy', 'মল-ই-ফাই', 'verb'),
    215: ('muh-ROHS', 'মা-রোস', 'adjective'),
    216: ('mun-DAYN', 'মান-ডেইন', 'adjective'),
    217: ('nih-GAYT', 'নি-গেইট', 'verb'),
    218: ('NEE-uh-fyt', 'নি-আ-ফাইট', 'noun'),
    219: ('OB-dyoor-it', 'অব-ডিউর-ইট', 'adjective'),
    220: ('ub-SEE-kwee-us', 'আব-সি-কুই-আস', 'adjective'),
    221: ('OB-vee-ayt', 'অব-ভি-এইট', 'verb'),
    222: ('uh-KLOOD', 'আ-ক্লুড', 'verb'),
    223: ('uh-FISH-us', 'আ-ফিশ-আস', 'adjective'),
    224: ('OH-ner-us', 'ও-নার-আস', 'adjective'),
    225: ('uh-PROH-bree-um', 'আ-প্রো-ব্রি-আম', 'noun'),
    226: ('OS-uh-layt', 'অস-ই-লেইট', 'verb'),
    227: ('os-ten-TAY-shus', 'অস-টেন-টেই-শাস', 'adjective'),
    228: ('PAIR-uh-gon', 'প্যার-আ-গন', 'noun'),
    229: ('PAHR-tuh-zun', 'পার-টি-জান', 'noun'),
    230: ('path-uh-LOJ-ih-kul', 'প্যাথ-আ-লজ-ই-কাল', 'adjective'),
    231: ('PAW-suh-tee', 'প-সি-টি', 'noun'),
    232: ('pih-DAN-tik', 'পি-ড্যান-টিক', 'adjective'),
    233: ('PEN-chunt', 'পেন-চান্ট', 'noun'),
    234: ('PEN-yuh-ree', 'পেন-ইউ-রি', 'noun'),
    235: ('puh-REN-ee-ul', 'পা-রেন-ই-আল', 'adjective'),
    236: ('per-FID-ee-us', 'পার-ফিড-ই-আস', 'adjective'),
    237: ('per-FUNGK-tuh-ree', 'পার-ফাংক-টা-রি', 'adjective'),
    238: ('PUR-mee-uh-bul', 'পার-মি-আ-বাল', 'adjective'),
    239: ('per-VAY-siv', 'পার-ভেই-সিভ', 'adjective'),
    240: ('fleg-MAT-ik', 'ফ্লেগ-ম্যাট-ইক', 'adjective'),
    241: ('PY-uh-tee', 'পাই-আ-টি', 'noun'),
    242: ('PLAY-kayt', 'প্লেই-কেইট', 'verb'),
    243: ('plas-TIS-uh-tee', 'প্লাস-টিস-ই-টি', 'noun'),
    244: ('PLAT-uh-tood', 'প্ল্যাট-ই-টুড', 'noun'),
    245: ('PLETH-er-uh', 'প্লেথ-এর-আ', 'noun'),
    246: ('PLUM-it', 'প্লাম-ইট', 'verb'),
    247: ('POR-us', 'পোর-আস', 'adjective'),
    248: ('prag-MAT-ik', 'প্র্যাগ-ম্যাট-ইক', 'adjective'),
    249: ('PREE-am-bul', 'প্রি-অ্যাম-বাল', 'noun'),
    250: ('prih-KAIR-ee-us', 'প্রি-কের-ই-আস', 'adjective'),
    251: ('prih-SIP-uh-tayt', 'প্রি-সিপ-ই-টেইট', 'verb'),
    252: ('prih-KUR-ser', 'প্রি-কার-সার', 'noun'),
    253: ('prih-ZUMP-choo-us', 'প্রি-জাম্প-চু-আস', 'adjective'),
    254: ('prih-VAIR-uh-kayt', 'প্রি-ভ্যার-ই-কেইট', 'verb'),
    255: ('PRIS-teen', 'প্রিস-টিন', 'adjective'),
    256: ('PROH-buh-tee', 'প্রো-বা-টি', 'noun'),
    257: ('prob-luh-MAT-ik', 'প্রব-লা-ম্যাট-ইক', 'adjective'),
    258: ('PROD-uh-gul', 'প্রড-ই-গাল', 'adjective'),
    259: ('pruh-FOWND', 'প্রো-ফাউন্ড', 'adjective'),
    260: ('proh-HIB-ih-tiv', 'প্রো-হিব-ই-টিভ', 'adjective'),
    261: ('pruh-LIF-uh-rayt', 'প্রো-লিফ-আ-রেইট', 'verb'),
    262: ('pruh-PEN-suh-tee', 'প্রো-পেন-সি-টি', 'noun'),
    263: ('pruh-PISH-ee-ayt', 'প্রো-পিশ-ই-এইট', 'verb'),
    264: ('pruh-PRY-uh-tee', 'প্রো-প্রাই-আ-টি', 'noun'),
    265: ('proh-SKRYB', 'প্রো-স্ক্রাইব', 'verb'),
    266: ('PUN-junt', 'পান-জান্ট', 'adjective'),
    267: ('KWOL-uh-fyd', 'কোয়াল-ই-ফাইড', 'adjective'),
    268: ('KWIB-ul', 'কুইব-আল', 'verb'),
    269: ('kwee-ES-unt', 'কুই-এস-অ্যান্ট', 'adjective'),
    270: ('RAIR-uh-fyd', 'রের-ই-ফাইড', 'adjective'),
    271: ('rih-KAL-sih-trunt', 'রি-ক্যাল-সি-ট্র্যান্ট', 'adjective'),
    272: ('rih-KANT', 'রি-ক্যান্ট', 'verb'),
    273: ('REK-loos', 'রেক-লুস', 'noun'),
    274: ('REK-un-dyt', 'রেক-আন-ডাইট', 'adjective'),
    275: ('rih-FRAK-tuh-ree', 'রি-ফ্র্যাক-টা-রি', 'adjective'),
    276: ('rih-FYOOT', 'রি-ফিউট', 'verb'),
    277: ('REL-uh-gayt', 'রেল-ই-গেইট', 'verb'),
    278: ('rih-PROHCH', 'রি-প্রোচ', 'verb'),
    279: ('REP-ruh-bayt', 'রেপ-রা-বেইট', 'noun'),
    280: ('rih-PYOO-dee-ayt', 'রি-পিউ-ডি-এইট', 'verb'),
    281: ('rih-SIND', 'রি-সিন্ড', 'verb'),
    282: ('rez-uh-LOO-shun', 'রেজ-আ-লু-শান', 'noun'),
    283: ('rih-ZOLV', 'রি-জল্ভ', 'verb'),
    284: ('RET-uh-sunt', 'রেট-ই-স্যান্ট', 'adjective'),
    285: ('REV-er-unt', 'রেভ-এর-অ্যান্ট', 'adjective'),
    286: ('SAYJ', 'সেইজ', 'adjective'),
    287: ('suh-LOO-bree-us', 'সা-লু-ব্রি-আস', 'adjective'),
    288: ('SANGK-shun', 'স্যাংক-শান', 'noun'),
    289: ('SAY-shee-ayt', 'সেই-শি-এইট', 'verb'),
    290: ('SACH-uh-rayt', 'স্যাচ-আ-রেইট', 'verb'),
    291: ('SAY-ver', 'সেই-ভার', 'verb'),
    292: ('sih-KREET', 'সি-ক্রিট', 'verb'),
    293: ('SHAHRD', 'শার্ড', 'noun'),
    294: ('SKEP-tik', 'স্কেপ-টিক', 'noun'),
    295: ('suh-LIS-uh-tus', 'সা-লিস-ই-টাস', 'adjective'),
    296: ('sop-uh-RIF-ik', 'সপ-আ-রিফ-ইক', 'adjective'),
    297: ('SPEE-shus', 'স্পি-শাস', 'adjective'),
    298: ('SPEK-trum', 'স্পেক-ট্রাম', 'noun'),
    299: ('spuh-RAD-ik', 'স্পা-র্যাড-ইক', 'adjective'),
    300: ('STIG-muh', 'স্টিগ-মা', 'noun'),
    301: ('STINT', 'স্টিন্ট', 'verb'),
    302: ('STIP-yuh-layt', 'স্টিপ-ইউ-লেইট', 'verb'),
    303: ('STOL-id', 'স্টল-ইড', 'adjective'),
    304: ('STRY-ay-tid', 'স্ট্রাই-এই-টিড', 'adjective'),
    305: ('STRUT', 'স্ট্রাট', 'verb'),
    306: ('STRUT', 'স্ট্রাট', 'noun'),
    307: ('suh-PEE-nuh', 'সা-পি-না', 'noun'),
    308: ('sub-SYD', 'সাব-সাইড', 'verb'),
    309: ('sub-STAN-shee-ayt', 'সাব-স্ট্যান-শি-এইট', 'verb'),
    310: ('soo-per-SEED', 'সু-পার-সিড', 'verb'),
    311: ('sup-uh-ZISH-un', 'সাপ-আ-জিশ-আন', 'noun'),
    312: ('TAS-it', 'ট্যাস-ইট', 'adjective'),
    313: ('tan-JEN-shul', 'ট্যান-জেন-শাল', 'adjective'),
    314: ('TEN-yoo-us', 'টেন-ইউ-আস', 'adjective'),
    315: ('TY-rayd', 'টাই-রেইড', 'noun'),
    316: ('TOR-per', 'টর-পার', 'noun'),
    317: ('TOR-choo-us', 'টর-চু-আস', 'adjective'),
    318: ('TRAK-tuh-bul', 'ট্র্যাক-টা-বাল', 'adjective'),
    319: ('trans-GRESH-un', 'ট্র্যান্স-গ্রেশ-আন', 'noun'),
    320: ('TRUK-yuh-lunss', 'ট্রাক-ইউ-ল্যান্স', 'noun'),
    321: ('VAS-uh-layt', 'ভ্যাস-ই-লেইট', 'verb'),
    322: ('VEN-uh-rayt', 'ভেন-আ-রেইট', 'verb'),
    323: ('vuh-RAY-shus', 'ভা-রেই-শাস', 'adjective'),
    324: ('ver-BOHS', 'ভার-বোস', 'adjective'),
    325: ('VY-uh-bul', 'ভাই-আ-বাল', 'adjective'),
    326: ('VIS-kus', 'ভিস-কাস', 'adjective'),
    327: ('vy-TOO-per-uh-tiv', 'ভাই-টু-পার-আ-টিভ', 'adjective'),
    328: ('VOL-uh-tul', 'ভল-আ-টাইল', 'adjective'),
    329: ('WOR-un-tid', 'ওয়ার-অ্যান-টিড', 'adjective'),
    330: ('WAIR-ee', 'ওয়ের-ই', 'adjective'),
    331: ('WEL-ter', 'ওয়েল-টার', 'noun'),
    332: ('HWIM-zih-kul', 'হুইম-জি-কাল', 'adjective'),
    333: ('ZEL-ut', 'জেল-অ্যাট', 'noun'),
}

# Hyphen adjustments for Sets 1-10
GRE_1_200_FIXES = {
    6: ('ad-MON-ish', 'অ্যাড-মন-ইশ'),
    56: ('kun-SIL-ee-uh-tor-ee', 'কান-সিল-ই-আ-টর-ই'),
    77: ('DES-ul-tor-ee', 'ডেস-আল-টর-ই'),
    109: ('ih-BOOL-yunt', 'ই-বুল-ইয়ান্ট'),
    193: ('eye-TIN-er-air-ee', 'আই-টিন-এর-এর-ই')
}

def clean_ws_pron(bn_str):
    if not bn_str:
        return ""
    t = bn_str
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

def main():
    print("1. Updating GRE 333 pronunciations...")
    with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
        gre = json.load(f)

    # Sets 1-10 hyphen adjustments
    for idx, (en, bn) in GRE_1_200_FIXES.items():
        gre[idx - 1]['pronunciationEn'] = en
        gre[idx - 1]['pronunciationBn'] = bn

    # Sets 11-17 words 201-333 updates
    for idx, (en, bn, pos) in GRE_201_333_PRON.items():
        gre[idx - 1]['pronunciationEn'] = en
        gre[idx - 1]['pronunciationBn'] = bn
        gre[idx - 1]['partOfSpeech'] = pos

    with open('src/data/gre333.json', 'w', encoding='utf-8') as f:
        json.dump(gre, f, ensure_ascii=False, indent=2)
    print("   -> GRE 333 pronunciations successfully updated!")

    print("2. Updating WordSmart 1 pronunciations...")
    with open('src/data/wordsmart1.json', 'r', encoding='utf-8') as f:
        ws1 = json.load(f)
    for w in ws1:
        w['pronunciationBn'] = clean_ws_pron(w.get('pronunciationBn', ''))
    with open('src/data/wordsmart1.json', 'w', encoding='utf-8') as f:
        json.dump(ws1, f, ensure_ascii=False, indent=2)
    print("   -> WordSmart 1 pronunciations successfully updated!")

    print("3. Updating WordSmart 2 pronunciations...")
    with open('src/data/wordsmart2.json', 'r', encoding='utf-8') as f:
        ws2 = json.load(f)
    for w in ws2:
        w['pronunciationBn'] = clean_ws_pron(w.get('pronunciationBn', ''))
    with open('src/data/wordsmart2.json', 'w', encoding='utf-8') as f:
        json.dump(ws2, f, ensure_ascii=False, indent=2)
    print("   -> WordSmart 2 pronunciations successfully updated!")

if __name__ == '__main__':
    main()
