# -*- coding: utf-8 -*-
"""
Mode 2: Sentence Completion - Sets 6 to 10 (Words 101 to 200)
Merges SET_6, SET_7, SET_8, SET_9, and SET_10 into MODE2_SETS_6_TO_10.
"""

from mode2_set6 import SET_6
from mode2_set7 import SET_7
from mode2_set8 import SET_8
from mode2_set9 import SET_9
from mode2_set10 import SET_10

MODE2_SETS_6_TO_10 = {}
MODE2_SETS_6_TO_10.update(SET_6)
MODE2_SETS_6_TO_10.update(SET_7)
MODE2_SETS_6_TO_10.update(SET_8)
MODE2_SETS_6_TO_10.update(SET_9)
MODE2_SETS_6_TO_10.update(SET_10)

if __name__ == '__main__':
    print(f"Total entries in Sets 6 to 10: {len(MODE2_SETS_6_TO_10)}")
