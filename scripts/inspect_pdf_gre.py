import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open('GRE 333 High Frequency Words - Enhanced Edition.pdf')
print(f"Total pages: {len(doc)}")

for page_idx in range(min(5, len(doc))):
    print(f"\n--- PAGE {page_idx + 1} ---")
    text = doc[page_idx].get_text()
    for line in text.split('\n')[:40]:
        print(line)
