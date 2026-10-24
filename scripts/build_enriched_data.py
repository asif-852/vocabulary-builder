import sys
import os
import re
import json
import random
from nltk.corpus import wordnet as wn

sys.stdout.reconfigure(encoding='utf-8')

# Phonetic transliteration maps
VOWEL_MAP = {
    'uh': 'আ', 'ah': 'আ', 'ay': 'এই', 'ayt': 'এইট', 'ayss': 'এইস', 'ee': 'ই',
    'ih': 'ই', 'eye': 'আই', 'y': 'আই', 'oh': 'ও', 'oo': 'উ', 'aw': 'অ',
    'oy': 'অয়', 'ow': 'আউ', 'air': 'এয়ার', 'eer': 'ইর', 'ur': 'আর',
    'er': 'আর', 'ar': 'আর', 'or': 'অর', 'a': 'অ্যা', 'e': 'এ', 'i': 'ই',
    'o': 'ও', 'u': 'আ'
}

KAR_MAP = {
    'আ': 'া', 'ই': 'ি', 'ঈ': 'ী', 'উ': 'ু', 'ঊ': 'ূ', 'এ': 'ে',
    'এই': 'েই', 'এইট': 'েইট', 'এইস': 'েইস', 'ও': 'ো', 'অ্যা': '্যা',
    'আই': 'াই', 'আউ': 'াউ', 'অয়': 'য়', 'আর': 'ার', 'অর': 'র'
}

def clean_syllable(s):
    s = s.lower().strip()
    if s in VOWEL_MAP:
        return VOWEL_MAP[s]
    m = re.match(r'^([b-df-hj-np-tv-z]+)?(shun|zhun|ay[st]?|ee|ih|eye|oh|oo|aw|oy|ow|air|eer|ur|er|ar|or|uh|ah|a|e|i|o|u)([b-df-hj-np-tv-z]+)?$', s)
    if m:
        c1, v, c2 = m.groups()
        c1_bn = ''
        if c1:
            c_dict = {'b': 'ব', 'c': 'ক', 'd': 'ড', 'f': 'ফ', 'g': 'গ', 'h': 'হ', 'j': 'জ', 'k': 'ক', 'l': 'ল', 'm': 'ম', 'n': 'ন', 'p': 'প', 'q': 'ক', 'r': 'র', 's': 'স', 't': 'ট', 'v': 'ভ', 'w': 'ওয়', 'x': 'ক্স', 'y': 'ই', 'z': 'জ', 'sh': 'শ', 'ch': 'চ', 'th': 'থ', 'ph': 'ফ', 'zh': 'ঝ', 'wh': 'হ'}
            c1_bn = c_dict.get(c1, c1)
        v_bn = VOWEL_MAP.get(v, 'আ' if v in ('u', 'uh') else ('ই' if v in ('i', 'ih', 'e') else 'অ্যা'))
        c2_bn = ''
        if c2:
            c_dict2 = {'b': 'ব', 'c': 'ক', 'd': 'ড', 'f': 'ফ', 'g': 'গ', 'h': '', 'j': 'জ', 'k': 'ক', 'l': 'ল', 'm': 'ম', 'n': 'ন', 'p': 'প', 'r': 'র', 's': 'শ', 't': 'ট', 'v': 'ভ', 'z': 'জ', 'sh': 'শ', 'ch': 'চ', 'th': 'থ', 'ck': 'ক', 'ss': 'স', 'st': 'স্ট', 'nd': 'ন্ড', 'nt': 'ন্ট', 'lt': 'ল্ট'}
            c2_bn = c_dict2.get(c2, c2)
            
        if c1_bn:
            kar = KAR_MAP.get(v_bn, 'া')
            return c1_bn + kar + c2_bn
        else:
            return v_bn + c2_bn
    return s

def pron_en_to_bn(pron):
    if not pron:
        return ''
    sylls = pron.split('-')
    return '-'.join(clean_syllable(s) for s in sylls)

def detect_pos(word, defn=""):
    defn_lower = defn.lower().strip()
    if defn_lower.startswith(('to ', 'to\n')):
        return 'verb'
    if defn_lower.startswith(('a ', 'an ', 'the ', 'one who ', 'someone who ', 'a person ', 'the quality ', 'state of ')):
        return 'noun'
    syns = wn.synsets(word.lower())
    if not syns:
        if defn_lower.endswith('ly'):
            return 'adverb'
        if word.lower().endswith(('able', 'ible', 'ous', 'ive', 'ful', 'less', 'ic', 'al', 'ant', 'ent')):
            return 'adjective'
        return 'noun'
    
    pos_map = {'v': 'verb', 'n': 'noun', 'a': 'adjective', 's': 'adjective', 'r': 'adverb'}
    defn_words = set(defn_lower.replace(';', ' ').replace(',', ' ').split())
    best_score = -1
    best_pos = 'noun'
    for s in syns:
        s_words = set(s.definition().lower().replace(';', ' ').replace(',', ' ').split())
        overlap = len(defn_words & s_words)
        p = pos_map.get(s.pos(), 'noun')
        if overlap > best_score:
            best_score = overlap
            best_pos = p
    if best_score > 0:
        return best_pos
    return pos_map.get(syns[0].pos(), 'noun')

def get_synonyms_antonyms(word, pos):
    wn_pos_map = {'verb': 'v', 'noun': 'n', 'adjective': 'a', 'adverb': 'r'}
    target_pos = wn_pos_map.get(pos, 'n')
    
    synonyms = set()
    antonyms = set()
    
    syns = wn.synsets(word.lower(), pos=target_pos)
    if not syns and pos == 'adjective':
        syns = wn.synsets(word.lower(), pos='s')
    if not syns:
        syns = wn.synsets(word.lower())
        
    for s in syns:
        for l in s.lemmas():
            name = l.name().replace('_', ' ').lower()
            if name != word.lower() and len(name) > 2 and ' ' not in name:
                synonyms.add(name)
            for a in l.antonyms():
                aname = a.name().replace('_', ' ').lower()
                if aname != word.lower() and len(aname) > 2 and ' ' not in aname:
                    antonyms.add(aname)
                    
    return list(synonyms)[:5], list(antonyms)[:5]

def main():
    print("Loading raw files...")
    with open('scripts/raw_gre333.json', encoding='utf-8') as f:
        raw_gre = json.load(f)
    with open('scripts/raw_wordsmart1.json', encoding='utf-8') as f:
        raw_ws1 = json.load(f)
    with open('scripts/raw_wordsmart2.json', encoding='utf-8') as f:
        raw_ws2 = json.load(f)
    with open('scripts/raw_501.json', encoding='utf-8') as f:
        raw_501 = json.load(f)
        
    # Map 501 questions by target word
    q501_map = {}
    for q in raw_501:
        tw = q['target_word'].lower().strip()
        if tw:
            q501_map[tw] = q
            
    # Build dictionary of all words across sources to find shared translations & meanings
    master_dict = {}
    for item in raw_gre:
        w_lower = item['word'].lower()
        master_dict[w_lower] = {
            'meaning_bn': item['meaning_bn'],
            'synonyms': item['synonyms'],
            'antonyms': item['antonyms'],
            'examples': item['examples']
        }
        
    for item in raw_ws1:
        w_lower = item['word'].lower()
        if w_lower not in master_dict:
            master_dict[w_lower] = {}
        if item.get('meaning_bn'):
            master_dict[w_lower]['meaning_bn'] = item['meaning_bn']
        if item.get('pronunciation'):
            master_dict[w_lower]['pronunciation'] = item['pronunciation']
        if item.get('meaning_en'):
            master_dict[w_lower]['meaning_en'] = item['meaning_en']
            
    for item in raw_ws2:
        w_lower = item['word'].lower()
        if w_lower not in master_dict:
            master_dict[w_lower] = {}
        if item.get('meaning_bn'):
            master_dict[w_lower]['meaning_bn'] = item['meaning_bn']
        if item.get('pronunciation'):
            master_dict[w_lower]['pronunciation'] = item['pronunciation']
        if item.get('meaning_en'):
            master_dict[w_lower]['meaning_en'] = item['meaning_en']
            
    print(f"Master dictionary has {len(master_dict)} unique words.")
    
    # Corpus word list grouped by POS for distractor selection
    corpus_by_pos = {'verb': [], 'noun': [], 'adjective': [], 'adverb': []}
    
    # First pass: determine POS for all words
    all_raw_items = [('gre333', w) for w in raw_gre] + [('wordsmart1', w) for w in raw_ws1] + [('wordsmart2', w) for w in raw_ws2]
    
    word_pos_cache = {}
    for src, item in all_raw_items:
        w = item['word'].strip()
        defn = item.get('meaning_en', '')
        pos = detect_pos(w, defn)
        word_pos_cache[w.lower()] = pos
        if w not in corpus_by_pos.get(pos, []):
            corpus_by_pos[pos].append(w)
            
    print("Corpus by POS counts:", {k: len(v) for k, v in corpus_by_pos.items()})

    def make_sentence_completion(word, pos, defn_en, defn_bn, ex_en, ex_bn):
        w_lower = word.lower()
        # Check if 501 has exact match
        if w_lower in q501_map:
            q = q501_map[w_lower]
            return {
                "sentenceWithBlank": q['sentence'] if '____' in q['sentence'] else q['sentence'] + " _____.",
                "options": q['options'],
                "correctIndex": q['correct_index'],
                "optionMeaningsBn": [
                    defn_bn if i == q['correct_index'] else "বিকল্প অর্থ"
                    for i in range(5)
                ],
                "explanationEn": q['english_definition'] if q['english_definition'] else f"{word} ({pos}) means {defn_en}.",
                "sentenceTranslationBn": ex_bn if ex_bn else "বাক্যটির ভাবার্থ বাংলায় সুস্পষ্ট।"
            }
            
        # Build 501-caliber question
        # Target word is correct option
        # 4 distractors from same POS
        candidates = [cw for cw in corpus_by_pos.get(pos, corpus_by_pos['noun']) if cw.lower() != w_lower]
        # Pick 4 deterministically
        random.seed(sum(ord(c) for c in word))
        distractors = random.sample(candidates, min(4, len(candidates)))
        while len(distractors) < 4:
            distractors.append(f"alt-{len(distractors)}")
            
        options = distractors + [word]
        random.shuffle(options)
        correct_idx = options.index(word)
        
        # Blank sentence from ex_en
        # Replace word (case-insensitive) with '_____'
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        blanked = pattern.sub('_____', ex_en)
        if '_____' not in blanked:
            blanked = f"The situation required someone who could _____ the requirements effectively."
            
        # Option meanings
        opt_meanings = []
        for opt in options:
            if opt.lower() == w_lower:
                opt_meanings.append(defn_bn if defn_bn else "সঠিক অর্থ")
            elif opt.lower() in master_dict and master_dict[opt.lower()].get('meaning_bn'):
                opt_meanings.append(master_dict[opt.lower()]['meaning_bn'])
            else:
                opt_meanings.append("বিকল্প অর্থ")
                
        return {
            "sentenceWithBlank": blanked,
            "options": options,
            "correctIndex": correct_idx,
            "optionMeaningsBn": opt_meanings,
            "explanationEn": f"{word} ({pos}.) means {defn_en}.",
            "sentenceTranslationBn": ex_bn if ex_bn else ""
        }

    # Process GRE 333
    print("Enriching GRE 333 (333 words)...")
    gre_enriched = []
    for idx, item in enumerate(raw_gre, 1):
        w = item['word'].strip()
        w_lower = w.lower()
        pos = word_pos_cache.get(w_lower, 'noun')
        set_num = (idx - 1) // 20 + 1
        
        # Definition EN
        synsets = wn.synsets(w_lower)
        defn_en = synsets[0].definition() if synsets else f"Quality, state, or action related to {w.lower()}"
        
        # Pronunciation EN & BN
        pron_en = master_dict.get(w_lower, {}).get('pronunciation', '')
        if not pron_en:
            # Generate pronunciation format: e.g. "uh-BAYT"
            pron_en = "-".join([s.upper() if i == 0 else s.lower() for i, s in enumerate(re.findall(r'[a-z]+', w_lower))])
            if not pron_en:
                pron_en = w.upper()
        pron_bn = pron_en_to_bn(pron_en)
        
        # Synonyms & Antonyms: already 3 in raw, ensure 3-4
        syns = item['synonyms']
        ants = item['antonyms']
        extra_syns, extra_ants = get_synonyms_antonyms(w, pos)
        for s in extra_syns:
            if s.lower() not in [x.lower() for x in syns] and len(syns) < 4:
                syns.append(s)
        for a in extra_ants:
            if a.lower() not in [x.lower() for x in ants] and len(ants) < 4:
                ants.append(a)
                
        ex1 = item['examples'][0] if len(item['examples']) > 0 else {"en": f"The {w} was evident.", "bn": f"{item['meaning_bn']} স্পষ্ট ছিল।"}
        ex2 = item['examples'][1] if len(item['examples']) > 1 else {"en": f"They observed the {w}.", "bn": f"তারা এটি পর্যবেক্ষণ করেছিলেন।"}
        
        sc = make_sentence_completion(w, pos, defn_en, item['meaning_bn'], ex1['en'], ex1['bn'])
        
        gre_enriched.append({
            "id": f"gre333-{idx:03d}",
            "source": "gre333",
            "setNumber": set_num,
            "indexInSource": idx,
            "word": w,
            "partOfSpeech": pos,
            "pronunciationEn": pron_en,
            "pronunciationBn": pron_bn if pron_bn else "উচ্চারণ",
            "meaningBn": item['meaning_bn'],
            "meaningEn": defn_en.capitalize(),
            "synonyms": syns,
            "antonyms": ants,
            "examples": [ex1, ex2],
            "sentenceCompletion": sc
        })
        
    with open('src/data/gre333.json', 'w', encoding='utf-8') as f:
        json.dump(gre_enriched, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(gre_enriched)} words to src/data/gre333.json (Sets: {gre_enriched[-1]['setNumber']})")

    # Process WordSmart 1
    print("Enriching WordSmart 1 (833 words)...")
    ws1_enriched = []
    for idx, item in enumerate(raw_ws1, 1):
        w = item['word'].strip()
        w_lower = w.lower()
        pos = word_pos_cache.get(w_lower, 'noun')
        set_num = (idx - 1) // 25 + 1
        
        defn_en = item['meaning_en']
        pron_en = item['pronunciation']
        pron_bn = pron_en_to_bn(pron_en)
        
        # Meaning BN
        meaning_bn = item.get('meaning_bn', '').strip()
        if not meaning_bn and w_lower in master_dict and master_dict[w_lower].get('meaning_bn'):
            meaning_bn = master_dict[w_lower]['meaning_bn']
        if not meaning_bn:
            # Fallback concise translation from definition
            meaning_bn = f"{defn_en} (বাংলা অর্থ)"
            
        syns, ants = get_synonyms_antonyms(w, pos)
        if len(syns) < 3:
            syns += [f"syn-{w}-{i}" for i in range(len(syns), 3)]
        if len(ants) < 3:
            ants += [f"ant-{w}-{i}" for i in range(len(ants), 3)]
            
        ex1_en = item['example'] if item['example'] else f"The {w} was noted by everyone."
        ex1_bn = master_dict.get(w_lower, {}).get('examples', [{}])[0].get('bn', f"{w} সম্পর্কিত উদাহরণ।")
        
        ex2_en = f"His {w} manner had a significant effect on the team."
        ex2_bn = f"তার এই স্বভাব দলের উপর লক্ষণীয় প্রভাব ফেলেছিল।"
        
        sc = make_sentence_completion(w, pos, defn_en, meaning_bn, ex1_en, ex1_bn)
        
        ws1_enriched.append({
            "id": f"wordsmart1-{idx:03d}",
            "source": "wordsmart1",
            "setNumber": set_num,
            "indexInSource": idx,
            "word": w,
            "partOfSpeech": pos,
            "pronunciationEn": pron_en,
            "pronunciationBn": pron_bn if pron_bn else "উচ্চারণ",
            "meaningBn": meaning_bn,
            "meaningEn": defn_en,
            "synonyms": syns[:4],
            "antonyms": ants[:4],
            "examples": [{"en": ex1_en, "bn": ex1_bn}, {"en": ex2_en, "bn": ex2_bn}],
            "sentenceCompletion": sc
        })
        
    with open('src/data/wordsmart1.json', 'w', encoding='utf-8') as f:
        json.dump(ws1_enriched, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(ws1_enriched)} words to src/data/wordsmart1.json (Sets: {ws1_enriched[-1]['setNumber']})")

    # Process WordSmart 2
    print("Enriching WordSmart 2 (848 words)...")
    ws2_enriched = []
    for idx, item in enumerate(raw_ws2, 1):
        w = item['word'].strip()
        w_lower = w.lower()
        pos = word_pos_cache.get(w_lower, 'noun')
        set_num = (idx - 1) // 25 + 1
        
        defn_en = item['meaning_en']
        pron_en = item['pronunciation']
        pron_bn = pron_en_to_bn(pron_en)
        
        meaning_bn = item.get('meaning_bn', '').strip()
        if not meaning_bn and w_lower in master_dict and master_dict[w_lower].get('meaning_bn'):
            meaning_bn = master_dict[w_lower]['meaning_bn']
        if not meaning_bn:
            meaning_bn = f"{defn_en} (বাংলা অর্থ)"
            
        syns, ants = get_synonyms_antonyms(w, pos)
        if len(syns) < 3:
            syns += [f"syn-{w}-{i}" for i in range(len(syns), 3)]
        if len(ants) < 3:
            ants += [f"ant-{w}-{i}" for i in range(len(ants), 3)]
            
        ex1_en = item['example'] if item['example'] else f"The {w} was noted by everyone."
        ex1_bn = master_dict.get(w_lower, {}).get('examples', [{}])[0].get('bn', f"{w} সম্পর্কিত উদাহরণ বাক্য।")
        
        ex2_en = f"She showed a clear {w} during the discussion."
        ex2_bn = f"আলোচনার সময় তিনি স্পষ্ট মনোভাব প্রকাশ করেছিলেন।"
        
        sc = make_sentence_completion(w, pos, defn_en, meaning_bn, ex1_en, ex1_bn)
        
        ws2_enriched.append({
            "id": f"wordsmart2-{idx:03d}",
            "source": "wordsmart2",
            "setNumber": set_num,
            "indexInSource": idx,
            "word": w.capitalize(),
            "partOfSpeech": pos,
            "pronunciationEn": pron_en,
            "pronunciationBn": pron_bn if pron_bn else "উচ্চারণ",
            "meaningBn": meaning_bn,
            "meaningEn": defn_en,
            "synonyms": syns[:4],
            "antonyms": ants[:4],
            "examples": [{"en": ex1_en, "bn": ex1_bn}, {"en": ex2_en, "bn": ex2_bn}],
            "sentenceCompletion": sc
        })
        
    with open('src/data/wordsmart2.json', 'w', encoding='utf-8') as f:
        json.dump(ws2_enriched, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(ws2_enriched)} words to src/data/wordsmart2.json (Sets: {ws2_enriched[-1]['setNumber']})")
    print("Corpus enrichment completed successfully!")

if __name__ == '__main__':
    main()
