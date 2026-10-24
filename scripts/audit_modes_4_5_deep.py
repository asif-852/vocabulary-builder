# -*- coding: utf-8 -*-
"""
Audits Mode 4 (Single Synonym) and Mode 5 (Single Antonym) for all 333 words in gre333.json
using the exact logic from src/data/index.ts.
"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

def capitalize_word(w):
    if not w:
        return ''
    return w[0].upper() + w[1:].lower()

def hash_string(s, seed=0):
    h = (seed ^ 0x811c9dc5) & 0xFFFFFFFF
    for char in s:
        h ^= ord(char)
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h

def deterministic_shuffle(arr, seed):
    res = list(arr)
    s = (seed ^ 0x9e3779b9) & 0xFFFFFFFF
    def rng():
        nonlocal s
        s = (s + 0x6d2b79f5) & 0xFFFFFFFF
        t = (s ^ (s >> 15)) & 0xFFFFFFFF
        t = (t * ((1 | s) & 0xFFFFFFFF)) & 0xFFFFFFFF
        t = (t + (((t ^ (t >> 7)) & 0xFFFFFFFF) * 61)) & 0xFFFFFFFF
        t = (t ^ (t >> 14)) & 0xFFFFFFFF
        return (t / 4294967296.0)

    for i in range(len(res) - 1, 0, -1):
        j = int(rng() * (i + 1))
        res[i], res[j] = res[j], res[i]
    return res

def select_diverse_distractors(candidates, count, seed, exclude_initials=None):
    if exclude_initials is None:
        exclude_initials = set()
    shuffled = deterministic_shuffle(candidates, seed)
    selected = []
    used_letters = set(exclude_initials)

    for c in shuffled:
        if len(selected) >= count:
            break
        initial = c['word'][0].upper()
        if initial not in used_letters:
            used_letters.add(initial)
            selected.append(c)

    if len(selected) < count:
        selected_set = set(id(c) for c in selected)
        for c in shuffled:
            if len(selected) >= count:
                break
            if id(c) not in selected_set:
                selected.append(c)
    return selected

ADVERB_POOL = [
    {'word': 'Ostensibly', 'meaningBn': 'আপাতদৃষ্টিতে বা বাহ্যত'},
    {'word': 'Invariably', 'meaningBn': 'সর্বদাই বা অপরিবর্তনীয়ভাবে'},
    {'word': 'Vehemently', 'meaningBn': 'তীব্রভাবে বা প্রবল আবেগের সাথে'},
    {'word': 'Deliberately', 'meaningBn': 'ইচ্ছাকৃতভাবে বা উদ্দেশ্যপ্রণোদিতভাবে'}
]

def audit_mode4():
    print("=== AUDITING MODE 4 (Single Synonym) FOR ALL 333 WORDS ===")
    violations = 0
    repetitive = {}
    for idx, target in enumerate(corpus, 1):
        t_word = target['word']
        syns = target.get('synonyms', [])
        ants = target.get('antonyms', [])
        correct_syn = capitalize_word(syns[0]) if syns else capitalize_word(t_word)
        lower_syns = set(s.lower() for s in syns)
        lower_syns.add(t_word.lower())
        lower_syns.add(correct_syn.lower())
        lower_ants = set(a.lower() for a in ants)

        distractors = []
        if ants:
            trap = capitalize_word(ants[0])
            distractors.append(trap)

        if target.get('partOfSpeech') == 'adverb':
            for adv in ADVERB_POOL:
                if len(distractors) >= 3:
                    break
                lower = adv['word'].lower()
                if lower not in lower_syns and not any(d.lower() == lower for d in distractors):
                    distractors.append(adv['word'])
        else:
            candidates = [
                w for w in corpus
                if w['partOfSpeech'] == target.get('partOfSpeech')
                and w['word'].lower() not in lower_syns
                and w['word'].lower() not in lower_ants
                and not any(d.lower() == w['word'].lower() for d in distractors)
                and target['word'].lower() not in [s.lower() for s in w.get('synonyms', [])]
                and not any(s.lower() in [ws.lower() for ws in w.get('synonyms', [])] for s in target.get('synonyms', []))
            ]
            exclude = {target['word'][0].upper()}
            if distractors:
                exclude.add(distractors[0][0].upper())
            seed = hash_string(target['word'], target.get('indexInSource', idx) + 101)
            diverse = select_diverse_distractors(candidates, 3 - len(distractors), seed, exclude)
            for c in diverse:
                distractors.append(capitalize_word(c['word']))

        opts = [correct_syn] + distractors[:3]
        if len(opts) != 4:
            print(f"Word {idx} ({t_word}): Mode 4 does not have 4 options! Got {len(opts)}")
            violations += 1
        if len(set(o.lower() for o in opts)) != 4:
            print(f"Word {idx} ({t_word}): Mode 4 has duplicate options! {opts}")
            violations += 1
        for d in distractors[:3]:
            repetitive[d] = repetitive.get(d, 0) + 1

    print(f"Mode 4 total violations: {violations}")
    print(f"Mode 4 Top 5 most repeated distractors: {sorted(repetitive.items(), key=lambda x: -x[1])[:5]}")
    return violations

def audit_mode5():
    print("\n=== AUDITING MODE 5 (Single Antonym) FOR ALL 333 WORDS ===")
    violations = 0
    repetitive = {}
    for idx, target in enumerate(corpus, 1):
        t_word = target['word']
        syns = target.get('synonyms', [])
        ants = target.get('antonyms', [])
        correct_ant = capitalize_word(ants[0]) if ants else capitalize_word(t_word)
        lower_ants = set(a.lower() for a in ants)
        lower_ants.add(t_word.lower())
        lower_ants.add(correct_ant.lower())
        lower_syns = set(s.lower() for s in syns)

        distractors = []
        if syns:
            trap = capitalize_word(syns[0])
            distractors.append(trap)

        if target.get('partOfSpeech') == 'adverb':
            for adv in ADVERB_POOL:
                if len(distractors) >= 3:
                    break
                lower = adv['word'].lower()
                if lower not in lower_ants and not any(d.lower() == lower for d in distractors):
                    distractors.append(adv['word'])
        else:
            candidates = [
                w for w in corpus
                if w['partOfSpeech'] == target.get('partOfSpeech')
                and w['word'].lower() not in lower_ants
                and w['word'].lower() not in lower_syns
                and not any(d.lower() == w['word'].lower() for d in distractors)
                and target['word'].lower() not in [a.lower() for a in w.get('antonyms', [])]
                and not any(a.lower() in [wa.lower() for wa in w.get('antonyms', [])] for a in target.get('antonyms', []))
            ]
            exclude = {target['word'][0].upper()}
            if distractors:
                exclude.add(distractors[0][0].upper())
            seed = hash_string(target['word'], target.get('indexInSource', idx) + 203)
            diverse = select_diverse_distractors(candidates, 3 - len(distractors), seed, exclude)
            for c in diverse:
                distractors.append(capitalize_word(c['word']))

        opts = [correct_ant] + distractors[:3]
        if len(opts) != 4:
            print(f"Word {idx} ({t_word}): Mode 5 does not have 4 options! Got {len(opts)}")
            violations += 1
        if len(set(o.lower() for o in opts)) != 4:
            print(f"Word {idx} ({t_word}): Mode 5 has duplicate options! {opts}")
            violations += 1
        for d in distractors[:3]:
            repetitive[d] = repetitive.get(d, 0) + 1

    print(f"Mode 5 total violations: {violations}")
    print(f"Mode 5 Top 5 most repeated distractors: {sorted(repetitive.items(), key=lambda x: -x[1])[:5]}")
    return violations

if __name__ == '__main__':
    v4 = audit_mode4()
    v5 = audit_mode5()
    if v4 == 0 and v5 == 0:
        print("\nALL 333 WORDS PASS MODES 4 & 5 VALIDATION CLEANLY!")
