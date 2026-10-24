import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

keywords = ['501', 'on/off', 'on / off', 'Explanation on', 'Explanation off', 'toggleExplanation', 'vocab_builder_explanation_pref', 'explanationOn', 'banglaOn', 'Bangla on', 'Bangla off', 'showBangla']

for root, dirs, files in os.walk('src'):
    for f in files:
        if f.endswith(('.tsx', '.ts', '.css')):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    for kw in keywords:
                        if kw.lower() in line.lower():
                            print(f"{path}:{i+1} [{kw}] -> {line.strip()}")
