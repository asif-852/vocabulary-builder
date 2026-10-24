import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open('WordSmart2_Corrected.pdf')
print("Total pages in WS2:", len(doc))

# Print first page
print(doc[0].get_text()[:1500])
