import fitz
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/gre333.json', 'r', encoding='utf-8') as f:
    gre_words = [d['word'] for d in json.load(f)[:200]]

print(f"Checking 501 PDF for matches among first 200 GRE words...")
doc = fitz.open('501 Sentence Completion Career Mentor.pdf')

pdf_text = ""
for page in doc:
    pdf_text += page.get_text() + "\n"

matches = {}
for w in gre_words:
    # search for whole word in pdf
    pattern = re.compile(r'\b' + re.escape(w) + r'\b', re.IGNORECASE)
    count = len(pattern.findall(pdf_text))
    if count > 0:
        matches[w] = count

print(f"Words found in 501 PDF: {len(matches)} / {len(gre_words)}")
for w, c in sorted(matches.items(), key=lambda x: -x[1])[:30]:
    print(f"  {w}: {c} occurrences")
