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

export interface MultiSynonymOption {
  word: string;
  isSynonym: boolean;
  meaningBn: string;
}

export interface MultiSynonymData {
  options: MultiSynonymOption[];
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
  meaningEn: string;          // Concise source meaning
  synonyms: string[];         // Minimum 3-4 accurate synonyms
  antonyms: string[];         // Minimum 3-4 accurate antonyms
  examples: [ExampleSentence, ExampleSentence]; // 2 contextual demo sentences with Bangla translations
  sentenceCompletion: SentenceCompletionQuestion; // 5-option sentence completion question
  multiSynonyms?: MultiSynonymData; // High-caliber multi-synonym question options
}

export interface VocabSet {
  sourceId: VocabSourceId;
  setNumber: number;
  wordCount: number;
  startWordIndex: number;
  endWordIndex: number;
  words: VocabWord[];
}
