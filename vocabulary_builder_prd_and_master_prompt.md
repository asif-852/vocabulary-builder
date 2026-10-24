# Product Requirements Document (PRD) & Master Agent Prompt
## Project: Enhanced Vocabulary Builder Web App (GRE 333, Word Smart 1 & 2)

> **Instructions for the AI Coding Agent:**  
> You are an expert full-stack frontend engineer and computational linguist. Your task is to build a complete, production-ready, minimal, vanilla **React + Vite** web application inside the current working directory (`D:\Vocabulary Builder`).  
> Read this entire document carefully before writing any code. Execute the project **phase by phase** as outlined in **Section 9 (Step-by-Step Execution Plan)**. Do not skip data normalization or UI layout constraints.

---

## 1. Project Overview & Core Philosophy

### 1.1 Vision
Build a fast, distraction-free, minimal vocabulary learning and testing web application inspired by [https://wordsmart-1.netlify.app/](https://wordsmart-1.netlify.app/) and the visual typography of the *GRE 333 High Frequency Words - Enhanced Edition* book.

### 1.2 Core Design Principles
1. **Minimal, Vanilla UI:** Clean typography, neutral surfaces, subtle borders, high legibility, and zero bloat. No unnecessary animations, sidebars, login screens, or complex analytics dashboards.
2. **Mobile & Desktop Parity:** Every view (Home, Set Hub, Study Mode, and all 5 Practice Modes) must be 100% responsive and never overflow, clip, or shift awkwardly on mobile browsers (`320px` to `430px` width) or desktop monitors.
3. **Zero-Jump Layout Stability:** In Study Mode, toggling `Explanation Off` $\leftrightarrow$ `Explanation On` **must keep the main vocabulary word locked in its exact X/Y position** on the card—the word itself must never jump vertically or horizontally when the explanation expands below/beside it.
4. **Study-Only Progress Tracking:** Progress tracking in `localStorage` is tied **exclusively to the Study section**. Practice modes are for testing/drilling and do not alter the global or per-set progress bars.
5. **Exam-Caliber Practice Questions:** All 5 practice modes must feature substantial, high-probability distractors (matching the part of speech, register, and difficulty of the *501 Sentence Completion* and *Competitive Exams Vocabulary* PDFs).

---

## 2. Source Files in Project Directory (`D:\Vocabulary Builder`)

The project directory contains the following reference assets that you must inspect and use:

1. `GRE 333 High Frequency Words - Enhanced Edition.pdf`
   - **Content:** 333 Barron's High-Frequency GRE words.
   - **Included Fields:** Word, Bangla Meaning, Synonyms (3), Antonyms (3), and 2 contextual demo sentences with native Bangla translations.
   - **Set Size:** **20 words per set** (Sets 1–16 = 20 words each; Set 17 = 13 words; Total = 17 Sets).
2. `WordSmart1_Corrected.pdf`
   - **Content:** 833 words from *Word Smart I (4th Edition)*.
   - **Included Fields:** Word, Pronunciation (`ad-MON-ish`), Concise English Meaning, Bengali Meaning, and 1 Example Sentence.
   - **Set Size:** **25 words per set** (Sets 1–33 = 25 words each; Set 34 = 8 words; Total = 34 Sets).
3. `WordSmart2_Corrected.pdf`
   - **Content:** 848 words from *Word Smart II*.
   - **Included Fields:** `#`, Word, Pronunciation, Concise English Meaning, Bangla Meaning, and 1 Example Sentence.
   - **Set Size:** **25 words per set** (Sets 1–33 = 25 words each; Set 34 = 23 words; Total = 34 Sets).
4. `501 Sentence Completion Career Mentor.pdf`
   - **Content:** 501 Sentence Completion questions (5 options `A`–`E`, Bangla option meanings, and English definition explanations) + Chapter 23 Competitive Exam Synonym/Antonym MCQs with structured Bangla explanation tables.
   - **Usage:** Serves as the gold-standard benchmark for Sentence Completion difficulty, context clues, distractor quality, and post-answer explanation formatting.
5. `Explanation_off.jpg` & `Explanation_on.jpg`
   - **Content:** Handwritten wireframes specifying the exact layout and behavior of the **Study Mode** card when `Explanation off` vs. `Explanation on` is toggled.

---

## 3. Unified Data Schema & Enrichment Specification

Because each PDF provides slightly different fields, you must build a data extraction and enrichment pipeline so that **every single word across all 3 sources** conforms to the following unified TypeScript/JSON schema (`src/data/vocabSchema.ts`):

```typescript
export type VocabSourceId = 'gre333' | 'wordsmart1' | 'wordsmart2';

export interface ExampleSentence {
  en: string; // e.g., "Teachers often admonish students who arrive late."
  bn: string; // e.g., "দেরিতে আসা শিক্ষার্থীদের শিক্ষকরা প্রায়ই সতর্ক করেন।"
}

export interface SentenceCompletionQuestion {
  sentenceWithBlank: string; // Exam-standard sentence with "_____"
  options: [string, string, string, string, string]; // 5 options (A-E), 1 correct + 4 plausible same-POS distractors
  correctIndex: number; // 0 to 4
  optionMeaningsBn: [string, string, string, string, string]; // e.g., ["সতর্ক করা", "প্রশংসা করা", ...]
  explanationEn: string; // e.g., "To admonish (v.) means to express warning or disapproval gently."
  sentenceTranslationBn: string; // Full Bangla translation of the completed sentence
}

export interface VocabWord {
  id: string;                 // e.g., "gre333-006"
  source: VocabSourceId;      // "gre333" | "wordsmart1" | "wordsmart2"
  setNumber: number;          // 1-based set index (20/set for GRE333, 25/set for WS1 & WS2)
  indexInSource: number;      // 1-based index within the book
  word: string;               // e.g., "Admonish"
  partOfSpeech: string;       // e.g., "verb" | "noun" | "adjective"
  pronunciationEn: string;    // e.g., "ad-MON-ish"
  pronunciationBn: string;    // e.g., "অ্যাড-মনিশ"
  meaningBn: string;          // e.g., "সতর্ক করা বা মৃদু তিরস্কার করা"
  meaningEn: string;          // Concise source meaning, e.g., "To express warning or disapproval to (someone) about a fault or oversight especially in a gentle but serious way."
  synonyms: string[];         // Minimum 3-4 accurate synonyms (e.g., ["warn", "reprove", "scold", "chide"])
  antonyms: string[];         // Minimum 3-4 accurate antonyms (e.g., ["praise", "applaud", "commend", "extol"])
  examples: [ExampleSentence, ExampleSentence]; // 2 contextual demo sentences with Bangla translations
  sentenceCompletion: SentenceCompletionQuestion; // 501-standard 5-option question
}
```

### 3.1 Rules for Filling Missing Fields Across Sources
1. **Concise Meaning (`meaningEn`):**
   - For *Word Smart 1 & 2*, use the exact concise English meaning from the PDF table (expanded slightly only if a 1-word gloss needs a clear dictionary phrase for Mode 1).
   - For *GRE 333*, provide a concise, single-sense dictionary definition matching the exact sense used in the source's Bangla meaning and demo sentences (do not dump multiple unrelated dictionary definitions).
2. **Pronunciation & Part of Speech (`partOfSpeech`, `pronunciationEn`, `pronunciationBn`):**
   - *Word Smart 1 & 2* already have `pronunciationEn` (e.g., `ad-MON-ish`). Transliterate this into natural Bangla phonetics (`pronunciationBn`, e.g., `অ্যাড-মনিশ`) and supply the accurate `partOfSpeech` (`verb`, `noun`, `adjective`).
   - For *GRE 333*, generate the matching `partOfSpeech`, `pronunciationEn` (in `Word Smart` capitalized-stress format like `ad-MON-ish`), and `pronunciationBn`.
3. **Synonyms & Antonyms (`synonyms`, `antonyms`):**
   - *GRE 333* provides 3 synonyms and 3 antonyms per word. Add a 4th high-precision synonym where helpful so Mode 3 (Multiple-Choice Checkboxes with 3–4 correct synonyms) has rich variety.
   - For *Word Smart 1 & 2*, cross-reference overlapping words from *GRE 333* and generate 3–4 accurate synonyms and 3–4 accurate antonyms matching the exact part of speech and sense of the word.
4. **Demo Sentences (`examples`):**
   - *GRE 333* already has 2 English demo sentences with `(Bangla translation)`.
   - *Word Smart 1 & 2* have 1 English example sentence. Translate that 1st sentence into natural Bangla, and provide a 2nd contextual English example sentence with its Bangla translation.
5. **Sentence Completion (`sentenceCompletion`):**
   - Cross-reference `501 Sentence Completion Career Mentor.pdf` first: if a word appears as the answer in the 501 PDF, adapt or use that exact 501-style sentence, its 5 options (`A`–`E`), its Bangla option meanings (`ব্যাখ্যা`), and its English explanation.
   - For words not directly in the 501 PDF, craft a **501-standard sentence** (containing clear contextual logic such as contrast, cause-effect, or definition clues) with **5 substantial options (`A`–`E`)** of the **exact same part of speech and morphological form** (e.g., all past-tense verbs or all adjectives), along with Bangla meanings for all 5 options and a concise English explanation.

---

## 4. User Interface & Navigation Architecture

### 4.1 Aesthetic & Theme (Inspired by `wordsmart-1.netlify.app` & `GRE 333 PDF`)
- **Color Palette:**
  - Background: `#f8fafc` (soft off-white/slate) or `#ffffff` with `#f1f5f9` secondary containers.
  - Text Primary: `#0f172a` (deep slate/charcoal).
  - Text Secondary / Muted Metadata: `#64748b` (muted slate for part of speech, pronunciation, and subtle labels).
  - Accent / Primary Brand: `#2563eb` (clean royal blue) or `#1e293b` (minimalist dark slate) for active buttons/toggles.
  - Correct State: `#16a34a` border/text with `#f0fdf4` background.
  - Incorrect State: `#dc2626` border/text with `#fef2f2` background.
- **Typography:**
  - English UI & Text: `'Inter'`, `-apple-system`, `BlinkMacSystemFont`, `'Segoe UI'`, `sans-serif`.
  - Bangla Text: `'Hind Siliguri'`, `'Noto Sans Bengali'`, `sans-serif` (load via Google Fonts in `index.html` so Bangla script renders crisply on both PC and mobile).

### 4.2 View 1: Home Page (Source & Set Selection)
- **Header:**
  - App Title: **Vocabulary Builder**
  - Subtitle: Minimal summary (`GRE 333 · Word Smart 1 · Word Smart 2 · Progress saved in this browser`).
- **Source Sections:**
  - Display **3 distinct sections** (either stacked vertically with clean section headers or switchable via a minimal top pill-bar so the user can jump between sources effortlessly, while still seeing each source's dedicated overview):
    1. **GRE 333 High Frequency Words** (`333 words · 17 sets (20 words/set)`)
    2. **Word Smart I** (`833 words · 34 sets (25 words/set)`)
    3. **Word Smart II** (`848 words · 34 sets (25 words/set)`)
- **Per-Source Progress Bar & Reset:**
  - Shows **Study Progress only**: e.g., `40 / 333 words studied` with a minimal progress bar and a `Reset progress` button (with a simple confirmation prompt).
- **Set Grid:**
  - Responsive CSS Grid (`grid-template-columns: repeat(auto-fill, minmax(150px, 1fr))` on desktop, `2 columns` on mobile).
  - Each Set Card displays:
    - **Set Title:** e.g., `Set 4`
    - **Word Range:** e.g., `Words 61–80`
    - **Study Status Badge:**
      - `Not started` (gray text)
      - `In progress (7 / 20)` (blue/amber text)
      - `Completed ✓` (green text/border)

### 4.3 View 2: Set Action Selection (`Study` vs. `Practice`)
When a user clicks on a Set card (e.g., **GRE 333 — Set 4**):
- Display a clean Set Hub view (or centered minimal card/modal) showing:
  - Breadcrumb / Back button: `← Back to Set List`
  - Title: `GRE 333 — Set 4` (`Words 61–80 · 20 Words`)
  - Study Status: e.g., `12 / 20 words studied`
  - **Two Primary Action Cards / Buttons:**
    1. **1. Study** — *"Learn words one by one with pronunciation, concise meaning, synonyms, antonyms, and contextual sentences."*
    2. **2. Practice** — *"Test your mastery of this set across 5 exam-style practice modes."*

---

## 5. Detailed Specification: Study Mode

Clicking **1. Study** opens the one-word-per-page Study interface for the selected Set.

### 5.1 Top Control Bar
- Left: `← Back to Set` button.
- Center: `Set X · Word Y of Z` (e.g., `Set 4 · Word 6 of 20`).
- Right: **Explanation Toggle Switch** (`• Explanation off` / `• Explanation on`), styled like the `Bangla On/Off` pill button on `wordsmart-1.netlify.app`.
  - Default state can be persisted in `localStorage` or start as `Explanation off` (or `on`) as toggled by the user.
  - Also support keyboard shortcut `Space` or `E` to toggle Explanation on/off, and `ArrowLeft` / `ArrowRight` for Previous / Next word.

### 5.2 The Study Word Card (Strictly Following `Explanation_off.jpg` & `Explanation_on.jpg`)
- **Card Container:**
  - Fixed-width/max-width container (`max-width: 720px`, `margin: 0 auto`) with a **consistent top padding** (`padding: 28px 24px` on desktop, `20px 16px` on mobile) and a minimum height (`min-height: 380px`) so the card does not erratically resize.
  - Follow the **GRE 333 Enhanced Edition book aesthetic**: clean white card, subtle border (`1px solid #e2e8f0`), soft left accent bar (`4px solid #2563eb`), and clear typographic hierarchy.
- **Zero-Jump Word Header (CRITICAL):**
  - The main English word (e.g., `Admonish`) is placed at the top-left of the card content area.
  - **When `Explanation off` is active:**
    - Only `Admonish` is visible in the card body.
    - All elements below it (metadata line, meaning, synonyms, antonyms, examples) and the inline Bangla meaning are hidden (`visibility: hidden` or `opacity: 0; pointer-events: none` or rendered below a fixed-position header row).
  - **When `Explanation on` is active:**
    - `Admonish` **remains in the exact same pixel position** as it was in `Explanation off`.
    - Next to `Admonish`, display the Bangla meaning in parentheses: `(সতর্ক করা বা মৃদু তিরস্কার করা)`.
      - *Mobile Responsiveness Note:* Use `display: flex; flex-wrap: wrap; align-items: baseline; gap: 8px;` on the word header row so that on narrow mobile screens, if the Bangla meaning wraps to the next line, `Admonish` still stays anchored at the exact same top-left coordinates `(0, 0)` of the card content!
- **Metadata Sub-header (Small & Less Attention-Grabbing):**
  - Directly beneath the word header row:
  - Format: `verb | ad-MON-ish | অ্যাড-মনিশ`
  - Styling: `font-size: 0.85rem` (`13.5px`), `color: #64748b` (muted slate), `font-weight: 400`, `margin-top: 6px; margin-bottom: 18px;`.
- **Concise Meaning:**
  - Format: **`Meaning:`** `To express warning or disapproval to (someone) about a fault or oversight especially in a gentle but serious way.`
  - Styling: Clear, readable body font (`1.05rem`), single concise sense from the source.
- **Synonyms & Antonyms Block:**
  - Format:
    - **`Synonyms:`** `warn, reprove, scold`
    - **`Antonyms:`** `praise, applaud, commend`
  - Styling: Clean stacked rows (`margin-top: 14px`), with `Synonyms:` in subtle green-slate bold and `Antonyms:` in subtle rose-slate bold (matching the GRE 333 book style).
- **Contextual Demo Sentences (Bulleted List):**
  - Format:
    - `• Teachers often admonish students who arrive late. (দেরিতে আসা শিক্ষার্থীদের শিক্ষকরা প্রায়ই সতর্ক করেন।)`
    - `• I must admonish you about the risks of reckless spending. (বেপরোয়া খরচের ঝুঁকি সম্পর্কে আমাকে অবশ্যই আপনাকে সতর্ক করতে হবে।)`
  - Styling: `margin-top: 18px`, `padding-top: 14px`, `border-top: 1px solid #f1f5f9`. The target word inside the English sentence may be subtly bolded or underlined. Bangla translations in parentheses use `'Hind Siliguri'` in a slightly softer slate tone (`#334155`).

### 5.3 Bottom Navigation & Study Progress Recording
- Buttons: `← Previous` and `Next →` (or `Finish Set ✓` on the last word).
- **Progress Tracking Logic:**
  - Whenever a user views a word in Study Mode and clicks `Next →` (or clicks `Finish Set`), mark that `word.id` as **studied** in `localStorage` (`vocab_builder_studied_words`).
  - Also provide a small, unobtrusive checkbox or pill at the bottom (`✓ Marked as studied`) so the user can see or toggle whether the current word is counted toward their Study progress.

---

## 6. Detailed Specification: Practice Section (5 Modes)

When the user clicks **2. Practice** inside a Set, display the **Practice Mode Selector** showing the 5 available practice modes for that Set:

1. **Find the Meaning** *(4 dictionary-style definitions — pick 1)*
2. **Sentence Completion** *(5 options, 501-exam standard with Bangla On/Off switch)*
3. **Synonyms Finding (Multiple Options)** *(6–7 checkboxes — pick all 3–4 correct synonyms)*
4. **Synonym Finding (One Option)** *(4 exam-style options — pick 1)*
5. **Antonym Finding (One Option)** *(4 exam-style options — pick 1)*

### 6.1 Shared Practice UI Features (Across All 5 Modes)
- **Top Bar:**
  - `← Back to Practice Modes` | `Set X: [Mode Name]`
  - `Score: X` | `Question Y of Z`
  - **`Bangla On` / `Bangla Off` Toggle Button:** Works identically to `https://wordsmart-1.netlify.app/`.
- **Question Order & Option Shuffling:**
  - Shuffle the order of questions when starting/retrying a practice session (or allow sequential order with shuffled options), and deterministically/randomly shuffle option positions so the correct answer isn't always in the same slot.
- **Navigation & Completion:**
  - `← Previous` and `Next →` buttons to move between questions in the set (preserving the user's selected answer and feedback state for already-answered questions in the current session, just like `wordsmart-1.netlify.app`).
  - At the end of the set, show the **Set Complete Screen**:
    - `Set X [Mode Name] Complete!`
    - `Score: X / Z` (`Y% correct`)
    - Buttons: `Retry this set` and `Back to Set`.

---

### 6.2 Mode 1: Find the Meaning (4 Options)
- **Prompt:** Display the target word prominently (e.g., **`ADMONISH`**) along with its part of speech (`verb`).
  - If `Bangla On` is enabled *after* answering, show the Bangla meaning next to the word.
- **Options:** 4 radio/button options (`A`, `B`, `C`, `D`), each containing a concise dictionary-style definition.
  - **1 Correct Option:** The word's `meaningEn`.
  - **3 Distractor Options:** Drawn from other words of the **exact same `partOfSpeech`** within the same source (or adjacent sets) whose definitions are similar in length and tone so no option looks obviously fake.
- **Feedback on Selection:**
  - Immediately highlights the chosen option (Green if correct, Red if wrong + highlights the correct option in Green).
  - Shows a concise explanation box below with the word's Bangla meaning and synonyms when `Bangla On` is active.

---

### 6.3 Mode 2: Sentence Completion (5 Options — `501 Sentence Completion` Standard)
- **Reference Benchmark:** Replicates `https://wordsmart-1.netlify.app/` and `501 Sentence Completion Career Mentor.pdf`.
- **Prompt:** A high-quality, context-rich sentence with a blank (`_____`).
- **Options:** **5 button options (`A`, `B`, `C`, `D`, `E`)**.
  - **1 Correct Option:** The target word from the set (inflected appropriately if needed, or base form matching all 5 options).
  - **4 Distractor Options:** High-probability, competitive-exam-grade vocabulary words of the **same part of speech**.
- **`Bangla On / Off` Behavior:**
  - When `Bangla On` is active:
    - Before/after answering, or inside the post-answer explanation box (matching the reference app's behavior — let's support showing the Bangla meaning hints/explanations clearly):
    - Specifically, in `wordsmart-1.netlify.app`, toggling `Bangla On` displays the Bangla translation/meaning helper so learners can test themselves with or without Bangla support, and after selecting an option, the **Explanation Box** displays:
      1. **Bangla Explanation (`ব্যাখ্যা (উত্তর: C):`)** listing the Bangla meaning of all 5 options:  
         `A. blighted - বাধা দেওয়া; B. confutative - খন্ডন; C. ravenous - বুভুক্ষিত; D. ostentatious - ভানপূর্ণ; E. blissful - সুখী`
      2. **English Definition:** e.g., `C. Ravenous (adj.) means extremely hungry.`
      3. **Bangla Sentence Translation:** Full Bangla translation of the completed sentence.

---

### 6.4 Mode 3: Synonyms Finding — Multiple Options (Checkboxes)
- **Prompt:**
  - Display the target word (e.g., **`ADMONISH`**) and instruction:  
    *"Select all correct synonyms for the word above (3 to 4 correct answers)."*
- **Options:**
  - Render **6 to 7 checkbox options** (`[ ] Option`).
  - **3 to 4 options** are true synonyms of the target word.
  - **3 options** are plausible distractors of the **same part of speech** (e.g., antonyms or unrelated high-frequency words from the same source).
- **Interaction & Evaluation:**
  - User can check/uncheck multiple boxes.
  - User clicks a primary **`Check Answer`** button.
  - **Scoring & Visual Feedback:**
    - A question is marked **100% Correct (+1 Score)** only if the user selects **all** true synonyms and **zero** distractors.
    - Upon clicking `Check Answer`, highlight each option:
      - Correctly selected synonym: **Green** (`✓ Synonym`)
      - Missed synonym (not checked by user): **Amber/Dashed Green** (`Missed Synonym`)
      - Incorrectly checked distractor: **Red** (`✗ Not a synonym — means: ...`)
    - Display the explanation box below showing the Bangla meaning of the main word and each option (when `Bangla On` is active).

---

### 6.5 Mode 4: Synonym Finding — One Option (4 Options, Competitive Exam Style)
- **Reference Benchmark:** Chapter 23 of `501 Sentence Completion Career Mentor.pdf` (Combined Bank, BCS, IBA, University Admission exam style).
- **Prompt:**
  - Exam-style stem, e.g., *"Which of the following is closest in meaning to the word **'OBSCURE'**?"*
- **Options:** **4 options (`A`, `B`, `C`, `D`)**.
  - **1 Correct Option:** A primary synonym of the target word.
  - **3 Distractor Options:** Substantial, exam-grade words of the same part of speech (often including 1–2 antonyms or near-trap words, just like BCS/Bank exams where 3 options might be antonyms of the target word and 1 is the synonym).
- **Post-Answer Explanation Table:**
  - When answered, display a clean mini-table inspired by the *Eminent Competitive Exams* PDF:
    | Word (মূল শব্দ) | Meaning (অর্থ) | Synonyms |
    | :--- | :--- | :--- |
    | **Admonish** | সতর্ক করা বা মৃদু তিরস্কার করা | warn, reprove, scold |
    | **Praise** *(Option B)* | প্রশংসা করা | applaud, commend |
    *(If `Bangla Off` is active, hide the Bangla column or show English glosses instead).*

---

### 6.6 Mode 5: Antonym Finding — One Option (4 Options, Competitive Exam Style)
- **Reference Benchmark:** Chapter 23 of `501 Sentence Completion Career Mentor.pdf`.
- **Prompt:**
  - Exam-style stem, e.g., *"Choose the word that is most nearly opposite in meaning to **'AUDACIOUS'**:"*
- **Options:** **4 options (`A`, `B`, `C`, `D`)**.
  - **1 Correct Option:** A primary antonym of the target word.
  - **3 Distractor Options:** Substantial, exam-grade words of the same part of speech (including 1–2 synonyms of the target word as classic exam traps—e.g., for `Audacious`, distractors like `bold`, `fearless`, `daring`, and correct antonym `timid`).
- **Post-Answer Explanation Table:**
  - Same structured breakdown table as Mode 4, clearly highlighting why the chosen antonym is opposite in meaning.

---

## 7. Distractor Generation Engine (Quality & Substantiality Rules)

To ensure *"all the options should be substantial and should have a likelihood of being chosen"*:
1. **Strict Part-of-Speech Matching:** Never mix parts of speech in options. If the target word is an `adjective`, all 4 or 5 options (and all 6–7 checkboxes in Mode 3) **must be adjectives**. If the target word is a `verb`, all options **must be verbs**.
2. **Same Register & Length:** Distractors must be drawn from the vocabulary corpus (`GRE 333`, `Word Smart 1`, `Word Smart 2`, and `501 Sentence Completion`) so a test-taker cannot guess the answer by picking the only "GRE-sounding" word or the longest definition.
3. **No Overlap Collisions:** When picking distractors for Synonym/Antonym/Meaning modes, programmatically verify that none of the distractor words are listed in the target word's `synonyms` (for Synonym mode) or `antonyms` (for Antonym mode).
4. **Deterministic Per-Question Pool or Pre-computed JSON:** Either pre-compute the distractors in the JSON dataset or use a deterministic seeded generator backed by the full 2,014-word corpus (333 + 833 + 848 words) filtered by `partOfSpeech`.

---

## 8. Technical Stack & Project Structure

- **Framework:** React 18+ with Vite (`npm create vite@latest . -- --template react-ts` or `react`).
- **Styling:** Vanilla CSS (`src/index.css` / `src/App.css`) or CSS Modules using clean CSS custom properties. Keep it lightweight, responsive, and dependency-free.
- **State Persistence:** Browser `localStorage` only (`vocab_builder_studied_words_v1` and `vocab_builder_ui_prefs_v1`).
- **Recommended Directory Structure:**
  ```text
  D:\Vocabulary Builder\
  ├── scripts/
  │   ├── extract_pdfs.py          # Script to parse the 4 PDFs into raw JSON
  │   └── build_enriched_data.mjs  # Script to normalize & enrich all 2,014 words
  ├── src/
  │   ├── data/
  │   │   ├── gre333.json          # 333 words (17 sets of 20)
  │   │   ├── wordsmart1.json      # 833 words (34 sets of 25)
  │   │   ├── wordsmart2.json      # 848 words (34 sets of 25)
  │   │   └── index.ts             # Helper functions to load sets & distractors
  │   ├── components/
  │   │   ├── Header.tsx
  │   │   ├── HomeView.tsx         # 3 Source sections, progress bars, Set grids
  │   │   ├── SetHubView.tsx       # "1. Study" and "2. Practice" launcher
  │   │   ├── StudyView.tsx        # Zero-jump Study card with Explanation On/Off
  │   │   └── practice/
  │   │       ├── PracticeHub.tsx          # Selector for the 5 Practice Modes
  │   │       ├── FindMeaningMode.tsx      # Mode 1 (4 definition options)
  │   │       ├── SentenceCompletionMode.tsx # Mode 2 (5 options, 501 standard)
  │   │       ├── MultiSynonymMode.tsx     # Mode 3 (6-7 checkboxes, pick 3-4)
  │   │       ├── SingleSynonymMode.tsx    # Mode 4 (4 options, exam style)
  │   │       └── SingleAntonymMode.tsx    # Mode 5 (4 options, exam style)
  │   ├── hooks/
  │   │   └── useStudyProgress.ts  # localStorage hook for Study progress only
  │   ├── App.tsx
  │   ├── main.tsx
  │   └── index.css
  ├── index.html
  └── package.json
  ```

---

## 9. Step-by-Step Execution Plan for the AI Agent

Follow these steps in order:

### Phase 1: Data Extraction & Corpus Enrichment
1. Write a Python or Node script in `scripts/` to extract all entries from:
   - `GRE 333 High Frequency Words - Enhanced Edition.pdf` (333 words)
   - `WordSmart1_Corrected.pdf` (833 words)
   - `WordSmart2_Corrected.pdf` (848 words)
   - `501 Sentence Completion Career Mentor.pdf` (501 sentence completion questions + explanations)
2. Enrich and validate the extracted data so that every word in `gre333.json`, `wordsmart1.json`, and `wordsmart2.json` has:
   - Accurate `partOfSpeech`, `pronunciationEn`, and `pronunciationBn` (Bangla phonetic script).
   - Concise `meaningEn` and `meaningBn` (from the source).
   - At least 3–4 `synonyms` and 3–4 `antonyms` of the matching part of speech.
   - 2 contextual `examples` (each with `en` and `bn`).
   - A 501-standard `sentenceCompletion` object (`sentenceWithBlank`, 5 `options`, `correctIndex`, `optionMeaningsBn`, `explanationEn`, `sentenceTranslationBn`).
3. Verify set partitioning:
   - `gre333`: **20 words per set** (Sets 1–16 have 20 words; Set 17 has 13 words).
   - `wordsmart1`: **25 words per set** (Sets 1–33 have 25 words; Set 34 has 8 words).
   - `wordsmart2`: **25 words per set** (Sets 1–33 have 25 words; Set 34 has 23 words).

### Phase 2: Scaffolding & Core UI Setup
1. Initialize the Vite + React project in `D:\Vocabulary Builder` (if not already initialized) and include Google Fonts (`Inter` and `Hind Siliguri`) in `index.html`.
2. Implement `useStudyProgress` hook in `src/hooks/useStudyProgress.ts` to track studied word IDs in `localStorage`, calculate per-set status (`Not started`, `In progress (X/Y)`, `Completed`), calculate per-source totals (`X / 333 words studied`), and support resetting progress per source or globally.

### Phase 3: Home View & Set Hub View
1. Build `HomeView.tsx` replicating the clean, minimal aesthetic of `https://wordsmart-1.netlify.app/` with separate sections for **GRE 333**, **Word Smart 1**, and **Word Smart 2**.
2. Build `SetHubView.tsx` so clicking any Set card (e.g., Set 4 of GRE 333) presents the Set overview and the two clear choices: **1. Study** and **2. Practice**.

### Phase 4: Study Mode (`StudyView.tsx`)
1. Implement the one-word-per-page Study view with the `Explanation off` / `Explanation on` toggle switch.
2. **Verify the Zero-Jump Constraint:** Test toggling `Explanation off` $\leftrightarrow$ `Explanation on` on both desktop (`1280px`) and mobile (`375px`) viewports. Confirm that the main word (e.g., `Admonish`) does not shift by even `1px` vertically or horizontally when toggling.
3. Verify that `partOfSpeech | pronunciationEn | pronunciationBn` is rendered in a small, muted font directly under the word, followed by `Meaning:`, `Synonyms:`, `Antonyms:`, and the 2 bulleted demo sentences with Bangla translations.
4. Wire up the `Next →` / `Finish Set` actions to update `useStudyProgress`.

### Phase 5: Practice Section (All 5 Modes)
1. Build `PracticeHub.tsx` allowing the user to pick any of the 5 practice modes for the active Set.
2. Build **Mode 1 (`FindMeaningMode.tsx`)**: 4 dictionary-definition options of the same POS + `Bangla On/Off`.
3. Build **Mode 2 (`SentenceCompletionMode.tsx`)**: 5 options (`A`–`E`), 501 Sentence Completion standard, `Bangla On/Off` switch, and full post-answer explanation (`ব্যাখ্যা` with Bangla meanings of all 5 options + English definition).
4. Build **Mode 3 (`MultiSynonymMode.tsx`)**: 6–7 checkboxes per word (3–4 correct synonyms + 3 plausible same-POS distractors), `Check Answer` evaluation, and detailed per-option feedback.
5. Build **Mode 4 (`SingleSynonymMode.tsx`)** and **Mode 5 (`SingleAntonymMode.tsx`)**: 4 exam-style options (`A`–`D`) with competitive-exam trap distractors and post-answer summary tables.

### Phase 6: Final Verification & Polish
1. Run `npm run build` and test the app in a browser across desktop and mobile viewport sizes (`360x800`, `390x844`, `1440x900`).
2. Verify there are no broken layouts, no missing Bangla translations, no console errors, and that progress persists across page reloads.