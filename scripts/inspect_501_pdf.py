import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open('501 Sentence Completion Career Mentor.pdf')
print("Total pages in 501 book:", len(doc))

# Print pages where actual questions begin (e.g. pages 5-15)
for page_num in range(min(15, len(doc))):
    text = doc[page_num].get_text()
    if '1.' in text or 'sentence' in text.lower():
        print(f"\n--- PAGE {page_num + 1} ---")
        lines = text.split('\n')
        for l in lines[:50]:
            print(l)
