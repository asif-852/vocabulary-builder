import sys
import os
import re
import json
import fitz

# Ensure stdout handles UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def extract_gre333():
    print("Extracting GRE 333...")
    doc = fitz.open("GRE 333 High Frequency Words - Enhanced Edition.pdf")
    full_text = "\n".join(p.get_text() for p in doc)
    
    # Split by entries like "1. Abate (কমানো বা তীব্রতা হ্রাাস পাওয়া)"
    raw_entries = re.split(r'\n(?=\d+\.\s+[A-Za-z\-]+\s+\()', full_text)[1:]
    words = []
    
    for idx, entry in enumerate(raw_entries, 1):
        m = re.match(r'(\d+)\.\s+([A-Za-z\-]+)\s+\(([^)]+)\)', entry)
        if not m:
            print(f"Warning: Failed to parse header at index {idx}: {repr(entry[:60])}")
            continue
        num, word, bn_meaning = m.groups()
        
        syn_match = re.search(r'Synonyms:\s*([^\n]+)', entry)
        ant_match = re.search(r'Antonyms:\s*([^\n]+)', entry)
        
        synonyms = [s.strip() for s in syn_match.group(1).split(',')] if syn_match else []
        antonyms = [a.strip() for a in ant_match.group(1).split(',')] if ant_match else []
        
        # Examples
        example_matches = re.findall(r'•\s*(.*?)\s*\(([^)]+)\)', entry, re.DOTALL)
        examples = []
        for en_text, bn_text in example_matches:
            en_clean = " ".join(en_text.split())
            bn_clean = " ".join(bn_text.split())
            examples.append({"en": en_clean, "bn": bn_clean})
            
        words.append({
            "index": int(num),
            "word": word.strip(),
            "meaning_bn": bn_meaning.strip(),
            "synonyms": synonyms,
            "antonyms": antonyms,
            "examples": examples
        })
        
    print(f"Extracted {len(words)} GRE 333 words.")
    with open("scripts/raw_gre333.json", "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    return words

def extract_wordsmart1():
    print("Extracting WordSmart 1...")
    doc = fitz.open("WordSmart1_Corrected.pdf")
    words = []
    
    for page in doc:
        tabs = page.find_tables()
        for t in tabs.tables:
            for r in t.extract():
                if r[0] and r[0].strip() != "Word":
                    word = r[0].strip()
                    pron = " ".join(r[1].split()) if r[1] else ""
                    meaning_en = " ".join(r[2].split()) if r[2] else ""
                    meaning_bn = " ".join(r[3].split()) if r[3] else ""
                    example = " ".join(r[4].split()) if r[4] else ""
                    
                    words.append({
                        "index": len(words) + 1,
                        "word": word,
                        "pronunciation": pron,
                        "meaning_en": meaning_en,
                        "meaning_bn": meaning_bn,
                        "example": example
                    })
                    
    print(f"Extracted {len(words)} WordSmart 1 words.")
    with open("scripts/raw_wordsmart1.json", "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    return words

def extract_wordsmart2():
    print("Extracting WordSmart 2...")
    doc = fitz.open("WordSmart2_Corrected.pdf")
    words = []
    
    for pno, page in enumerate(doc):
        text = page.get_text()
        header_idx = text.find("Example Sentence")
        if header_idx != -1:
            text = text[header_idx + len("Example Sentence"):]
            
        parts = re.split(r'\n(?=\d+\n)', text)
        for p in parts:
            p = p.strip()
            if not p:
                continue
            lines = [l.strip() for l in p.split('\n') if l.strip()]
            if lines and lines[0].isdigit():
                num = int(lines[0])
                word = lines[1]
                pron = lines[2]
                rest = lines[3:]
                
                # Check for any Bangla characters in lines
                bn_lines = [l for l in rest if any('\u0980' <= c <= '\u09FF' for c in l)]
                meaning_bn = " ".join(bn_lines)
                
                non_bn = [l for l in rest if not any('\u0980' <= c <= '\u09FF' for c in l)]
                
                # Separate English meaning and example sentence
                # In WS2, the last line(s) ending with a period is the example sentence
                # Let's inspect where example sentence begins
                if len(non_bn) == 1:
                    meaning_en = non_bn[0]
                    example = ""
                else:
                    # Find candidate example split: usually starts with a capitalized word and ends with '.'
                    # Example sentences are complete sentences
                    # Check from backwards: lines ending with '.'
                    meaning_lines = []
                    example_lines = []
                    # In WS2, typically: lines 0..k are meaning, lines k+1..end are example
                    # Let's look for the start of the example sentence:
                    # An example usually contains the word (stem) or starts with Capitalized Subject
                    # And finishes at the last line.
                    found_split = False
                    for i in range(len(non_bn) - 1, 0, -1):
                        # If line before i ends in a semicolon or noun-phrase ending, or line i starts with capitalized sentence
                        # Let's check:
                        sub_ex = " ".join(non_bn[i:])
                        sub_mean = " ".join(non_bn[:i])
                        # If sub_ex ends with '.' and starts with capital
                        if non_bn[i][0].isupper() and (non_bn[-1].endswith('.') or non_bn[-1].endswith('"') or non_bn[-1].endswith('!')):
                            meaning_en = sub_mean
                            example = sub_ex
                            found_split = True
                            break
                    if not found_split:
                        meaning_en = non_bn[0]
                        example = " ".join(non_bn[1:])
                        
                words.append({
                    "index": num,
                    "word": word,
                    "pronunciation": pron,
                    "meaning_en": meaning_en,
                    "meaning_bn": meaning_bn,
                    "example": example
                })
                
    words.sort(key=lambda x: x["index"])
    print(f"Extracted {len(words)} WordSmart 2 words.")
    with open("scripts/raw_wordsmart2.json", "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    return words

def extract_501_questions():
    print("Extracting 501 Sentence Completion questions...")
    doc = fitz.open("501 Sentence Completion Career Mentor.pdf")
    # Chapters 1 to 22 span pages 0 to 79
    full_text = ""
    for i in range(80):
        full_text += f"\n--- PAGE {i+1} ---\n" + doc[i].get_text()
        
    # Split by questions:
    # Pattern: e¨vL¨v\s*[\(:]\s*DËi\s*[:\-]?\s*([A-Ea-e])\)?
    # Let's find question blocks
    q_blocks = re.split(r'\n(?=(?:\d+\.|\d+\s*\n[A-Z]))', full_text)
    print(f"Found {len(q_blocks)} raw question candidates.")
    
    questions = []
    # Search for explanation markers
    matches = list(re.finditer(r'e¨vL¨v\s*[\(:]\s*DËi\s*[:\-]?\s*([A-Ea-e])\)?', full_text))
    print(f"Found {len(matches)} explanation markers.")
    
    # Extract each question block between markers
    for idx in range(len(matches)):
        m = matches[idx]
        correct_letter = m.group(1).upper()
        start_exp = m.start()
        # End of explanation is next question or next marker
        end_exp = matches[idx+1].start() if idx + 1 < len(matches) else len(full_text)
        
        # Start of this question is after previous explanation (or page start)
        start_q = matches[idx-1].end() if idx > 0 else 0
        q_text = full_text[start_q:start_exp]
        exp_text = full_text[start_exp:end_exp]
        
        # Parse options from q_text: A., B., C., D., E.
        opt_matches = list(re.finditer(r'(?:^|\n)\s*([A-E])\.\s*([^\n]+)', q_text))
        options = {}
        if len(opt_matches) >= 5:
            for om in opt_matches[-5:]:
                options[om.group(1).upper()] = om.group(2).strip()
            # Sentence is text before the first of these 5 options
            sentence_part = q_text[:opt_matches[-5].start()]
        else:
            # Try looser option regex: e.g. A. B. C. D. E.
            opt_matches_loose = list(re.finditer(r'([A-E])\.\s*([A-Za-z\-]+)', q_text))
            if len(opt_matches_loose) >= 5:
                for om in opt_matches_loose[-5:]:
                    options[om.group(1).upper()] = om.group(2).strip()
                sentence_part = q_text[:opt_matches_loose[-5].start()]
            else:
                sentence_part = q_text
            
        # Clean sentence
        # Remove headers like 'Chapter ...', 'Eminent ...', '745'
        s_lines = []
        for line in sentence_part.split('\n'):
            line = line.strip()
            if not line:
                continue
            if re.match(r'^(?:Eminent|Vocab|Chapter|\d{3,4}|---\s*PAGE)', line):
                continue
            s_lines.append(line)
        cleaned_sentence = " ".join(s_lines)
        # Remove leading number like '01.', '1.', etc.
        cleaned_sentence = re.sub(r'^\d+\.\s*', '', cleaned_sentence).strip()
        
        # English definition inside exp_text
        # e.g. 'C. Ravenous (adj.) means extremely hungry.'
        # or 'd. To necessitate (v.) means...'
        def_match = re.search(r'(?:^|\n)\s*([A-Ea-e]\.?\s+[A-Z][a-zA-Z\s\(\)\.,\'-]+means[^\n\.]+[\.]?)', exp_text)
        eng_def = def_match.group(1).strip() if def_match else ""
        
        # Target word from correct option
        target_word = options.get(correct_letter, "")
        
        if cleaned_sentence and len(options) == 5:
            questions.append({
                "question_num": len(questions) + 1,
                "sentence": cleaned_sentence,
                "options": [options["A"], options["B"], options["C"], options["D"], options["E"]],
                "correct_letter": correct_letter,
                "correct_index": "ABCDE".index(correct_letter),
                "target_word": target_word,
                "english_definition": eng_def,
                "raw_explanation": exp_text[:300].strip()
            })
            
    print(f"Extracted {len(questions)} clean 501 questions.")
    with open("scripts/raw_501.json", "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    return questions

if __name__ == "__main__":
    gre = extract_gre333()
    ws1 = extract_wordsmart1()
    ws2 = extract_wordsmart2()
    q501 = extract_501_questions()
    print("All PDF extractions completed successfully!")
