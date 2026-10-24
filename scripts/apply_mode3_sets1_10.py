# -*- coding: utf-8 -*-
"""
Applies high-caliber multi-synonym questions to Sets 1 to 10 (Words 1 to 200) in src/data/gre333.json.
"""

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('scripts')

from mode3_set1 import SET_1
from mode3_set2 import SET_2
from mode3_set3 import SET_3
from mode3_set4 import SET_4
from mode3_set5 import SET_5
from mode3_set6 import SET_6
from mode3_set7 import SET_7
from mode3_set8 import SET_8
from mode3_set9 import SET_9
from mode3_set10 import SET_10

all_mode3 = {}
all_mode3.update(SET_1)
all_mode3.update(SET_2)
all_mode3.update(SET_3)
all_mode3.update(SET_4)
all_mode3.update(SET_5)
all_mode3.update(SET_6)
all_mode3.update(SET_7)
all_mode3.update(SET_8)
all_mode3.update(SET_9)
all_mode3.update(SET_10)

print(f"Total Mode 3 curated entries to apply: {len(all_mode3)}")
assert len(all_mode3) == 200, f"Expected 200, got {len(all_mode3)}"

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    gre_data = json.load(f)

for idx in range(1, 201):
    item = gre_data[idx - 1]
    curated = all_mode3[idx]
    
    # Store multiSynonyms in item
    item['multiSynonyms'] = {
        'options': curated['options']
    }

with open('src/data/gre333.json', 'w', encoding='utf-8') as f:
    json.dump(gre_data, f, ensure_ascii=False, indent=2)

print("SUCCESS: Successfully applied Mode 3 high-caliber questions to Words 1 to 200 in gre333.json!")
