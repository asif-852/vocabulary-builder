# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

# Find entries by id
corpus_by_id = {w['id']: w for w in corpus}

fixes = [
    {
        'id': 'gre333-229',
        'word': 'Partisan',
        'meaningBn': 'অন্ধ সমর্থক বা দলকানা ব্যক্তি',
        'synonyms': ['supporter', 'adherent', 'devotee', 'champion'],
        'antonyms': ['opponent', 'adversary', 'critic', 'moderate']
    },
    {
        'id': 'gre333-232',
        'word': 'Pedantic',
        'antonyms': ['unconventional', 'informal', 'practical']
    },
    {
        'id': 'gre333-235',
        'word': 'Perennial',
        'antonyms': ['ephemeral', 'fleeting', 'temporary']
    },
    {
        'id': 'gre333-239',
        'word': 'Pervasive',
        'synonyms': ['ubiquitous', 'widespread', 'permeating', 'omnipresent']
    },
    {
        'id': 'gre333-244',
        'word': 'Platitude',
        'synonyms': ['banality', 'truism', 'cliche', 'commonplace']
    },
    {
        'id': 'gre333-248',
        'word': 'Pragmatic',
        'synonyms': ['practical', 'sensible', 'realistic', 'utilitarian']
    },
    {
        'id': 'gre333-251',
        'word': 'Precipitate',
        'meaningBn': 'হঠাৎ ঘটানো বা ত্বরান্বিত করা',
        'synonyms': ['trigger', 'hasten', 'accelerate', 'instigate'],
        'antonyms': ['impede', 'hinder', 'delay', 'forestall']
    },
    {
        'id': 'gre333-257',
        'word': 'Problematic',
        'antonyms': ['certain', 'settled', 'unambiguous', 'straightforward']
    },
    {
        'id': 'gre333-258',
        'word': 'Prodigal',
        'synonyms': ['wasteful', 'extravagant', 'profligate', 'reckless']
    },
    {
        'id': 'gre333-268',
        'word': 'Quibble',
        'synonyms': ['cavil', 'nitpick', 'complain', 'bicker']
    },
    {
        'id': 'gre333-282',
        'word': 'Resolution',
        'antonyms': ['indecision', 'hesitation', 'wavering', 'vacillation']
    },
    {
        'id': 'gre333-283',
        'word': 'Resolve',
        'meaningBn': 'মীমাংসা করা বা দৃঢ় সংকল্প গ্রহণ করা',
        'synonyms': ['settle', 'determine', 'decide', 'adjudicate'],
        'antonyms': ['waver', 'hesitate', 'vacillate', 'complicate']
    },
    {
        'id': 'gre333-286',
        'word': 'Sage',
        'meaningBn': 'বিজ্ঞ বা গভীর প্রজ্ঞাপূর্ণ',
        'synonyms': ['wise', 'prudent', 'sagacious', 'judicious'],
        'antonyms': ['foolish', 'unwise', 'imprudent', 'fatuous']
    },
    {
        'id': 'gre333-288',
        'word': 'Sanction',
        'synonyms': ['authorize', 'approve', 'permit', 'endorse']
    },
    {
        'id': 'gre333-291',
        'word': 'Savor',
        'synonyms': ['relish', 'enjoy', 'appreciate', 'taste']
    },
    {
        'id': 'gre333-296',
        'word': 'Soporific',
        'synonyms': ['sedative', 'somniferous', 'somnolent', 'hypnotic']
    },
    {
        'id': 'gre333-301',
        'word': 'Stint',
        'synonyms': ['skimp', 'limit', 'scrimp', 'grudge']
    },
    {
        'id': 'gre333-306',
        'word': 'Strut',
        'synonyms': ['brace', 'prop', 'support', 'reinforcement']
    },
    {
        'id': 'gre333-307',
        'word': 'Subpoena',
        'meaningBn': 'আদালতি সমন বা সাক্ষ্য দেওয়ার তলবপত্র'
    },
    {
        'id': 'gre333-327',
        'word': 'Vituperative',
        'synonyms': ['abusive', 'scathing', 'insulting', 'scolding']
    },
    {
        'id': 'gre333-329',
        'word': 'Warranted',
        'synonyms': ['justified', 'authorized', 'defensible', 'grounded'],
        'antonyms': ['unjustified', 'baseless', 'groundless', 'unwarranted']
    }
]

applied_count = 0
for f in fixes:
    w_id = f['id']
    if w_id not in corpus_by_id:
        print(f"ERROR: {w_id} not found in corpus!")
        continue
    w = corpus_by_id[w_id]
    assert w['word'] == f['word'], f"Word mismatch for {w_id}: {w['word']} != {f['word']}"
    
    if 'meaningBn' in f:
        print(f"[{w['word']}] meaningBn: '{w['meaningBn']}' -> '{f['meaningBn']}'")
        w['meaningBn'] = f['meaningBn']
    if 'synonyms' in f:
        print(f"[{w['word']}] synonyms: {w['synonyms']} -> {f['synonyms']}")
        w['synonyms'] = f['synonyms']
    if 'antonyms' in f:
        print(f"[{w['word']}] antonyms: {w['antonyms']} -> {f['antonyms']}")
        w['antonyms'] = f['antonyms']
    applied_count += 1

with open('src/data/gre333.json', 'w', encoding='utf-8') as f:
    json.dump(corpus, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully applied {applied_count} curated fixes to src/data/gre333.json")
