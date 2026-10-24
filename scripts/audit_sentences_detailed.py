import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)[:200]

print(f"Auditing all 200 words for POS consistency in both sentences...")

def check_pos_usage(word, pos, sentence):
    # returns list of potential issues
    issues = []
    # clean sentence
    s = sentence.strip()
    
    # check if word is used as noun when pos is verb:
    # "a/an/the [adj] word" (when word doesn't end in -ing or -ed acting as verbal noun/participle)
    if pos == 'verb':
        noun_det_match = re.search(r'\b(a|an|the|this|that|his|her|its|their|our)\s+(?:\w+\s+)?\b' + re.escape(word) + r'\b', s, re.IGNORECASE)
        if noun_det_match:
            issues.append(f"Used with determiner '{noun_det_match.group(0)}' (looks like noun)")
            
    # check if word is used as verb when pos is noun:
    # "to word", "will/would/can/could/should/did/does word"
    if pos == 'noun':
        verb_modal_match = re.search(r'\b(to|will|would|can|could|should|must|did|does|do)\s+\b' + re.escape(word) + r'\b', s, re.IGNORECASE)
        if verb_modal_match:
            issues.append(f"Preceded by '{verb_modal_match.group(0)}' (looks like verb)")
            
    # check if word is used as verb when pos is adjective:
    if pos == 'adjective':
        verb_match = re.search(r'\b(to|will|would|can|could|should|must)\s+\b' + re.escape(word) + r'\b', s, re.IGNORECASE)
        if verb_match:
            issues.append(f"Preceded by '{verb_match.group(0)}' (looks like verb)")
        # check if used with determiner as pure noun: "a/the <adj> of"
        det_noun_match = re.search(r'\b(a|an|the)\s+\b' + re.escape(word) + r'\s+of\b', s, re.IGNORECASE)
        if det_noun_match:
            issues.append(f"Used as '{det_noun_match.group(0)}' (looks like noun)")

    return issues

flagged_list = []
for d in data:
    word = d['word']
    pos = d['partOfSpeech']
    for i, ex in enumerate(d['examples']):
        iss = check_pos_usage(word, pos, ex['en'])
        if iss:
            flagged_list.append((d['id'], word, pos, i+1, iss, ex['en'], ex['bn']))

print(f"Total flagged sentences: {len(flagged_list)}")
for f in flagged_list:
    print(f"[{f[0]}] {f[1]} ({f[2]}) - Sent {f[3]}: {f[4]}")
    print(f"   EN: {f[5]}")
    print(f"   BN: {f[6]}")
