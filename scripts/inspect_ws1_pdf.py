import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open('WordSmart1_Corrected.pdf')
print("Total pages in WS1:", len(doc))

# Print first 2 pages
for i in range(2):
    print(f"\n--- WS1 PAGE {i+1} ---")
    print(doc[i].get_text()[:1500])
