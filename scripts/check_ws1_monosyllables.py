import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = fitz.open('WordSmart1_Corrected.pdf')
for page in doc:
    text = page.get_text()
    for line in text.split('\n'):
        # look for words like bland, blunt, apt, terse, trite, etc.
        for w in ['Bland', 'Blunt', 'Apt', 'Terse', 'Trite', 'Spartan', 'Spurious']:
            if line.strip() == w:
                print(f"Found {w} in WS1")
                # print next 5 lines
                lines = text.split('\n')
                idx = lines.index(line)
                for j in range(idx, min(len(lines), idx + 6)):
                    print("  ", lines[j])
                break
