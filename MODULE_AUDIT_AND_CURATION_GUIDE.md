# Vocabulary Builder — Data Curation & Quality Assurance Guide
**Standard Operating Procedures (SOP) for Reviewing & Curating Subsequent Sets**
*(Applicable to GRE 333 Sets 11–17, Word Smart I, and Word Smart II)*

---

## 1. Overview & Scope

This guide defines the exact content standards, auditing checks, and curation workflows required for reviewing and upgrading vocabulary sets in the application.

All application engine logic (layout stability, navigation, scoring, responsive design, and UI components) is already fixed and standardized. Any AI agent or developer working on remaining sets focuses exclusively on:
1. **Data Cleanliness, Linguistic Accuracy, and Question Quality** in the JSON datasets:
   - [`src/data/gre333.json`](file:///D:/Vocabulary%20Builder/src/data/gre333.json)
   - [`src/data/wordsmart1.json`](file:///D:/Vocabulary%20Builder/src/data/wordsmart1.json)
   - [`src/data/wordsmart2.json`](file:///D:/Vocabulary%20Builder/src/data/wordsmart2.json)
2. **Strict Adherence to Algorithmic Standards** (prohibiting naive pseudo-hashes and biased modulo sorts across the codebase).

---

## 2. Text Quality & Bengali Typography Standards

Raw scraped or legacy vocabulary data often contains OCR, Bijoy font mapping, or web scraping artifacts that must be corrected:

1. **Broken Conjuncts & Bijoy Glitches:**
   - `কাযকর` → `কার্যকর`
   - `উেখ` → `উল্লেখ`
   - `পূণ` → `পূর্ণ`
   - `সংখ্যাাবৃি` → `সংখ্যাবৃদ্ধি`
   - `দািক` → `দাম্ভিক`
   - `সেহ / সেহজনক / সেহপ্রবণ` → `সন্দেহ / সন্দেহজনক / সন্দেহপ্রবণ`
   - `িধাদ্বে` → `দ্বিধাদ্বন্দ্বে`
   - `নিিয়তা` → `নিষ্ক্রিয়তা`
   - `দীিমান` → `দীপ্তিমান`
   - `মানববিেষী` → `মানববিদ্বেষী`
   - `বহুবষজীবী` → `বহুবর্ষজীবী`
2. **Duplicate Diacritics:**
   - Strip all stacked/double vowel signs: `াা` → `া`, `ীী` → `ী`, `ুু` → `ু`, `ূূ` → `ূ`, `েে` → `ে`.
3. **Purity of Meaning Fields:**
   - Bengali definitions (`meaningBn`) must contain natural, accurate Bengali with **zero English characters**, zero trailing punctuation artifacts, and zero generic placeholders.

---

## 3. Module-by-Module Content Standards

---

### Module 0: Study View Content

Each word entry in the dataset must provide complete, high-register study material:

1. **Header Representation:**
   - `word`: English headword in Title Case.
   - `meaningBn`: Clear, precise Bengali meaning displayed in parentheses alongside the headword.
2. **Phonetics & Pronunciation:**
   - `partOfSpeech`: Grammatical class in lowercase (`verb`, `adjective`, `noun`, `adverb`).
   - `pronunciationEn`: Hyphenated syllable phonetics with capitalized stress (e.g. `uh-BAYT`, `AB-uh-ruhnt`).
   - `pronunciationBn`: Natural Bengali phonetic pronunciation (e.g. `আবেইট`, `অ্যাবোরান্ট`).
3. **Grammatical Alignment of Example Sentences (CRITICAL):**
   - Both contextual example sentences (`exampleEn1`, `exampleEn2`) must use the headword in its **exact grammatical part of speech**:
     - **Verb:** Sentences must use the word as a verb (`abate`, `abated`, `abating`). Never use noun or adjective forms!
     - **Noun:** Sentences must use the word as a noun.
     - **Adjective:** Sentences must use the word as an adjective.
   - Both sentences must have natural, fluent Bengali translations (`exampleBn1`, `exampleBn2`).
4. **Lexical Range:**
   - `synonyms`: High-caliber GRE synonyms as clean single words.
   - `antonyms`: High-caliber GRE antonyms as clean single words.

---

### Module 1: Find the Meaning (Definition Matching)

1. **Pristine Definitions (`meaningEn`):**
   - Clean up web-scraping baggage: remove author attributions (e.g. `- sir walter scott`, `- c.b.davis`), repeated semicolons (`; ; ;`), botanical/historical trivia, and volume numbers.
   - Grammatical parity: ensure definitions reflect the grammatical role of the headword (e.g. verbs start with "To...", nouns name entities/concepts, adjectives describe qualities).
2. **Conflict Prevention:**
   - Distractors are drawn dynamically from same-POS words in the corpus using [`getMeaningDistractors`](file:///D:/Vocabulary%20Builder/src/data/index.ts).
   - Distractors must never define a synonym or antonym of the target word, and must never contain the target word in the definition text.

---

### Module 2: Sentence Completion (Exam-Style 501 Standard)

1. **Sentence Caliber & Context:**
   - Sentences must be substantial, multi-clause, high-register sentences modeled after *501 Sentence Completion Questions*.
   - Must contain rich contextual clues: contrast markers (*although*, *despite*, *whereas*), cause-and-effect markers (*because*, *consequently*, *thereby*), or tone shifts.
   - Blank is represented by `______`.
2. **5 Distinct, Same-POS Options:**
   - Exactly 1 correct answer (the target word).
   - 4 sophisticated, challenging, unfamiliar GRE distractors sharing the exact same part of speech.
   - All 5 options must fit grammatically into the blank.
3. **Data Schema (`sentenceCompletion`):**
   ```json
   "sentenceCompletion": {
     "sentence": "Although the tempest battered the coastline for hours, its ferocious winds began to ______ by dawn.",
     "sentenceBn": "যদিও ঝড়টি ঘণ্টার পর ঘণ্টা উপকূলজুড়ে তাণ্ডব চালিয়েছিল, ভোরের মধ্যেই এর প্রচণ্ড বাতাস শান্ত হতে শুরু করে।",
     "options": [
       { "word": "Abate", "meaningEn": "To lessen in intensity", "meaningBn": "কমানো বা তীব্রতা হ্রাস পাওয়া", "isCorrect": true },
       { "word": "Proliferate", "meaningEn": "To increase rapidly", "meaningBn": "দ্রুত বিস্তার লাভ করা", "isCorrect": false },
       { "word": "Ameliorate", "meaningEn": "To make better", "meaningBn": "উন্নতিসাধন করা", "isCorrect": false },
       { "word": "Exacerbate", "meaningEn": "To make worse", "meaningBn": "অবনতি করা", "isCorrect": false },
       { "word": "Bolster", "meaningEn": "To support or strengthen", "meaningBn": "দৃঢ় বা শক্তিশালী করা", "isCorrect": false }
     ]
   }
   ```

---

### Module 3: Synonyms Finding — Multiple Checkboxes (6 Options)

Every question in Mode 3 consists of **6 options** (stored under `item.multiSynonyms`). This module requires the highest level of curation effort:

1. **Mandatory Individual Hand-Crafting (Zero Lazy Automation):**
   - **DO NOT** use automated hash-modulo scripts or bulk extraction scripts to populate Mode 3 distractors. Automated scripts inevitably pick clustered words from alphabetical sub-blocks of the corpus.
   - Every word must be individually curated and verified with deliberate linguistic care.
2. **Exactly 3 True Synonyms (Strict Tiered Difficulty):**
   - **1 Easy / Core synonym:** Widely recognized, fundamental meaning (e.g. for *Pungent* → *Sharp*; for *Dormant* → *Inactive*).
   - **1 Medium / Collegiate synonym:** Standard academic synonym (e.g. for *Pungent* → *Biting*; for *Dormant* → *Latent*).
   - **1 Hard / Sophisticated synonym:** Advanced GRE/literary synonym (e.g. for *Pungent* → *Caustic*; for *Dormant* → *Quiescent*).
3. **Exactly 3 Distractors (Strict Randomness & Non-Predictability):**
   - **Strictly ZERO Antonyms:** Under NO circumstances may distractors be antonyms or opposite words (e.g., for *Innocuous*, NEVER use *Pernicious* or *Deleterious*; for *Appease*, NEVER use *Provoke* or *Agitate*). Antonyms make questions childishly predictable.
   - **Strictly ZERO Semantic Overlap:** Distractors must be completely unrelated to the target word's semantic field.
   - **First-Letter Diversity Rule (CRITICAL):**
     - The 3 distractors must have **3 completely distinct starting letters**.
     - **Strictly prohibit letter clustering:** Never have 2 or 3 distractors starting with the same letter (e.g., three words starting with `A`, `R`, or `F`).
     - When distractors cluster on identical initial letters, learners immediately eliminate them without even reading, defeating the entire learning objective.
     - Distractors should be drawn from diverse sections of the alphabet (e.g., `P`, `C`, `T`, `M`, `V`, `D`, `G`, `L`, etc.).
   - **No Repeated Early Words:** Avoid repeatedly recycling early corpus words like *Abate*, *Aberrant*, or *Admonish*. Distribute distractor choices evenly across the whole vocabulary universe.
   - **Exact Part of Speech Match:** All 3 distractors must share the target word's part of speech.
4. **Authentic Bengali Meaning for Every Option:**
   - All 6 options (both correct synonyms and distractors) must have accurate, dedicated Bengali definitions (`meaningBn`).
   - Zero English characters and zero generic placeholders.
5. **Data Schema (`multiSynonyms`):**
   ```json
   "multiSynonyms": {
     "options": [
       { "word": "Subside", "isSynonym": true, "meaningBn": "তীব্রতা হ্রাস পাওয়া বা কমে যাওয়া" },
       { "word": "Dwindle", "isSynonym": true, "meaningBn": "ক্রমশ ক্ষীণ হওয়া বা হ্রাস পাওয়া" },
       { "word": "Wane", "isSynonym": true, "meaningBn": "ক্রমান্বয়ে ক্ষয় হওয়া বা দুর্বল হওয়া" },
       { "word": "Divest", "isSynonym": false, "meaningBn": "বঞ্চিত করা বা প্রত্যাহার করা" },
       { "word": "Ameliorate", "isSynonym": false, "meaningBn": "উন্নতিসাধন করা বা অবস্থার উন্নতি করা" },
       { "word": "Stipulate", "isSynonym": false, "meaningBn": "শর্তারোপ করা বা চুক্তিতে উল্লেখ করা" }
     ]
   }
   ```

---

### Modules 4 & 5: Single Synonym & Single Antonym (4 Options)

The dynamic engines in `src/data/index.ts` automatically assemble the 4-choice questions ([`getSingleSynonymQuestion`](file:///D:/Vocabulary%20Builder/src/data/index.ts) and [`getSingleAntonymQuestion`](file:///D:/Vocabulary%20Builder/src/data/index.ts)) using each word's `synonyms` and `antonyms` arrays.

#### Content Standards for the Word Data:
1. **Primary Synonym (`synonyms[0]`):**
   - Must be a clean, single vocabulary word (e.g. *Understatement*, never a two-word phrase like *polite term*).
   - Must be an unambiguous, accurate synonym of the headword.
2. **Primary Antonym (`antonyms[0]`):**
   - Must be a clean, single vocabulary word (e.g. *Flexible*, not hyphenated *open-minded*; *Cosmopolitanism*, not *broad-mindedness*).
   - Must be an unambiguous, accurate antonym of the headword.
3. **No Empty Lists:**
   - Every word must have at least 1 valid synonym and 1 valid antonym.
4. **No Semantic Cross-Collisions:**
   - `synonyms[0]` and `antonyms[0]` must never be the headword itself, and must never equal each other.

---

## 4. Codebase Algorithm & Randomization Standards

**CRITICAL POLICY: Never use naive, hardcoded, or single-character modulo pseudo-randomization anywhere in this codebase.**

### 1. The Prohibited Anti-Pattern:
```ts
// ❌ STRICTLY FORBIDDEN:
const shuffled = [...options].sort((a, b) => {
  const hashA = (a.text.charCodeAt(0) * 19 + seed) % 43;
  const hashB = (b.text.charCodeAt(0) * 19 + seed) % 43;
  return hashA - hashB;
});
```
**Why this is prohibited:**
- **Severe Bucket Collisions:** `charCodeAt(0)` only inspects the first character, meaning all words starting with the same letter get the exact same hash value.
- **Alphabetical Clumping:** Modulo arithmetic on character codes naturally preserves alphabetical sub-blocks, causing words starting with `A`, `R`, or `F` to cluster together.
- **Violates Comparator Transitivity:** Returning pseudo-hash differences inside `Array.prototype.sort()` violates mathematical transitivity requirements (`if A > B and B > C, then A > C`). Different JavaScript engines handle non-transitive comparators unpredictably, leading to UI flicker, non-deterministic bugs, and biased distributions.

### 2. The Mandated Solution:
All randomization, option shuffling, and distractor sampling must use the standardized utilities in [`src/data/index.ts`](file:///D:/Vocabulary%20Builder/src/data/index.ts):

1. **32-bit FNV-1a String Hash ([`hashString`](file:///D:/Vocabulary%20Builder/src/data/index.ts#L101-L108)):**
   Evaluates the entire string character sequence using FNV-1a prime multiplication, ensuring avalanche entropy across all characters.
2. **Uniform Fisher-Yates PRNG Shuffle ([`deterministicShuffle`](file:///D:/Vocabulary%20Builder/src/data/index.ts#L115-L129)):**
   Uses Knuth/Fisher-Yates with a Mulberry32 PRNG. Guarantees mathematical uniformity ($O(N)$), absolute transitivity, zero engine bias, and perfect determinism for a given seed.
   ```ts
   // ✅ MANDATORY PATTERN:
   const seed = hashString(word.word, word.indexInSource + 307);
   const shuffled = deterministicShuffle(rawOptions, seed);
   ```
3. **Initial-Letter Diversity Enforcement ([`selectDiverseDistractors`](file:///D:/Vocabulary%20Builder/src/data/index.ts#L135-L167)):**
   Filters candidates so that chosen distractors never share identical starting letters with each other or with excluded headword letters.

---

## 5. Quality Audit & Verification Scripts

Use the automated Python audit tools in `scripts/` to validate every set before finalizing:

| Tool | Purpose | Passing Benchmark |
| :--- | :--- | :--- |
| `scripts/scan_and_clean_all_bn.py` | Scans for Bijoy/OCR artifacts and double vowels | 0 warnings, 0 broken conjuncts |
| `scripts/audit_applied_mode3.py` | Audits Mode 3 multiple synonyms and distractors across all 333 words | Exactly 3 true syns, 3 distractors, 0 antonyms, 0 violations |
| `scripts/verify_distractor_diversity.py` | Audits initial-letter diversity for Mode 3 distractors | 0 duplicate initial letters, 0 letter clumping |
| `scripts/audit_modes_4_5_deep.py` | Audits single synonym and single antonym data | Exactly 4 options for all words, 0 single-word violations |
| `npm run build` | Compiles TypeScript and production bundle | Clean build, 0 errors |
| `python scripts/test_app.py` | Runs headless browser test suite | 100% pass, 0 console errors |

---

## 6. Summary Checklist for Each Set

Before marking any new set complete, verify:
- [ ] Bengali meanings in Study View have 0 OCR or Bijoy artifacts.
- [ ] Example sentences strictly match the headword's base part of speech.
- [ ] Sentence completion questions are substantial, multi-clause, with 5 same-POS options and full option breakdown.
- [ ] Multi-synonym questions have 3 tiered true synonyms + 3 purely random zero-relation distractors (strictly zero antonyms).
- [ ] Multi-synonym distractors strictly adhere to the First-Letter Diversity Rule (3 distinct starting letters, zero clumping on A/R/F).
- [ ] `synonyms[0]` and `antonyms[0]` are clean single words with no multi-word phrases.
- [ ] Zero naive `charCodeAt(0) % N` or pseudo-hash comparator sorting anywhere in the code.
- [ ] `npm run build` passes with zero errors.
- [ ] `python scripts/test_app.py` passes with 100% success.
