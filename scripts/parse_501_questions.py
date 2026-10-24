import fitz
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open('501 Sentence Completion Career Mentor.pdf')

# Let's inspect pages 1 to 5 to see the question patterns
full_text = ""
for page_idx in range(len(doc)):
    t = doc[page_idx].get_text()
    full_text += f"\n=== PAGE {page_idx+1} ===\n" + t

# Find questions with numbering like "01." or "1." or "2." followed by text with blank, options A, B, C, D, E, and explanation
print(f"Total length: {len(full_text)} characters")

# Let's search for "Alleviate" or "Assuage" or "Abate" in full_text
for target in ['Alleviate', 'Assuage', 'Abate', 'Admonish', 'Apathy', 'Capricious']:
    print(f"\n=================== SEARCH: {target} ===================")
    for m in re.finditer(r'\b' + re.escape(target) + r'\b', full_text, re.IGNORECASE):
        start = max(0, m.start() - 300)
        end = min(len(full_text), m.end() + 300)
        print("MATCH SNIPPET:")
        print(full_text[start:end])
        print("-" * 50)
        break
