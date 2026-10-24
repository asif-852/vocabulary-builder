# -*- coding: utf-8 -*-
"""
Fixes all 55 corrupted, citation-laden, or POS-mismatched definitions in src/data/gre333.json.
"""

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

CLEAN_DEFINITIONS = {
    203: "Expressed clearly; easy to understand; clear and comprehensible.",
    210: "A complete and dramatic change in form, appearance, character, or condition.",
    213: "To make something bad or painful less severe, harmful, or painful; alleviate.",
    214: "To appease the anger or anxiety of someone; soothe or calm.",
    215: "Sullen, gloomy, and ill-tempered.",
    216: "Lacking interest or excitement; dull; ordinary and everyday.",
    217: "To deny the existence or truth of; nullify or make ineffective.",
    218: "A person who is new to a subject, skill, or belief; a beginner or novice.",
    221: "To remove or eliminate a need, difficulty, or obstacle; prevent.",
    222: "To stop, close up, or obstruct an opening, orifice, or passage.",
    226: "To swing or move back and forth continuously; waver indecisively between options.",
    235: "Lasting or existing for a long or apparently infinite time; continually recurring.",
    241: "The quality of being religious or reverent; devoutness.",
    242: "To soothe, calm, or appease someone, especially by conceding demands.",
    246: "To fall or drop straight down at high speed; plunge steeply.",
    248: "Dealing with matters sensibly and realistically based on practical considerations rather than theoretical ones.",
    251: "To cause an event or situation, typically bad or unexpected, to happen suddenly or prematurely.",
    252: "A person or thing that comes before another of the same kind; a forerunner.",
    254: "To speak or act evasively in order to deceive or avoid telling the truth.",
    258: "Spending money or resources recklessly and wastefully; extravagant.",
    261: "To increase rapidly in numbers; multiply or flourish.",
    263: "To win or regain the favor of a god, spirit, or person by doing something that pleases them; appease.",
    265: "To forbid or prohibit especially by law; denounce or condemn.",
    268: "To argue or raise petty, trivial objections about a minor matter.",
    272: "To formally withdraw, renounce, or disavow a statement or previously held belief.",
    275: "Stubbornly resistant to authority, control, or treatment; unmanageable.",
    276: "To prove a statement, theory, or argument to be wrong or false; disprove.",
    277: "To assign to a lower or less important position, rank, or category; demote.",
    278: "To express disapproval, criticism, or disappointment to someone.",
    280: "To refuse to accept, recognize, or be associated with; reject or disown.",
    281: "To revoke, repeal, or cancel a law, order, or agreement officially.",
    283: "To find a solution to a problem; to firmly decide upon a course of action.",
    286: "Having, showing, or indicating profound wisdom, sound judgment, and prudence.",
    287: "Health-giving, wholesome, and beneficial to physical wellbeing.",
    289: "To satisfy a desire or appetite to the full or to excess.",
    290: "To thoroughly soak with liquid; cause to be completely filled or permeated.",
    291: "To taste or smell with pleasure; to appreciate or enjoy something fully and thoroughly.",
    292: "To produce and discharge a substance, typically from a biological cell or gland; also to conceal.",
    296: "Tending to induce drowsiness or sleep; sleep-producing.",
    300: "A mark of disgrace or shame associated with a particular circumstance, quality, or person.",
    301: "To restrict, supply in an ungenerous manner, or be frugal with.",
    302: "To demand or specify a requirement as part of a formal agreement or contract.",
    303: "Calm, dependable, and showing little or no emotion or reaction.",
    304: "Marked with thin, parallel grooves, stripes, or bands.",
    305: "To walk with a proud, erect, pompous, and confident gait.",
    308: "To become less intense, severe, or violent; diminish or sink to a lower level.",
    309: "To provide evidence to support or prove the truth of an assertion; corroborate.",
    310: "To take the place of a person or thing previously in authority or use; supplant.",
    317: "Full of twists and turns; excessively lengthy, complex, and convoluted.",
    318: "Easily managed, influenced, controlled, or taught; docile.",
    321: "To waver between different opinions or actions; be indecisive.",
    322: "To regard someone or something with deep respect, reverence, or awe.",
    328: "Liable to change rapidly and unpredictably, especially for the worse; easily evaporated.",
    329: "Justified, reasonable, or necessary under the circumstances.",
    333: "A person who is fanatical and uncompromising in pursuit of their religious, political, or other ideals."
}

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

updated_count = 0
for idx, new_meaning in CLEAN_DEFINITIONS.items():
    item = data[idx - 1]
    old_meaning = item['meaningEn']
    item['meaningEn'] = new_meaning
    print(f"Updated [{idx}] {item['word']}: '{old_meaning}' -> '{new_meaning}'")
    updated_count += 1

with open('src/data/gre333.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSUCCESS: Updated {updated_count} definitions in src/data/gre333.json!")
