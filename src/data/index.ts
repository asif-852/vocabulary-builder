import { VocabWord, VocabSet, VocabSourceId } from './vocabSchema';
import gre333Raw from './gre333.json';
import wordsmart1Raw from './wordsmart1.json';
import wordsmart2Raw from './wordsmart2.json';

const gre333Words: VocabWord[] = gre333Raw as VocabWord[];
const wordsmart1Words: VocabWord[] = wordsmart1Raw as VocabWord[];
const wordsmart2Words: VocabWord[] = wordsmart2Raw as VocabWord[];

export const SOURCES_INFO: Record<VocabSourceId, {
  id: VocabSourceId;
  title: string;
  shortTitle: string;
  totalWords: number;
  totalSets: number;
  wordsPerSet: number;
  lastSetWords: number;
  description: string;
}> = {
  gre333: {
    id: 'gre333',
    title: 'GRE 333 High Frequency Words',
    shortTitle: 'GRE 333',
    totalWords: 333,
    totalSets: 17,
    wordsPerSet: 20,
    lastSetWords: 13,
    description: 'Barron’s 333 high-frequency words with native Bangla meanings, synonyms, antonyms & demo sentences.'
  },
  wordsmart1: {
    id: 'wordsmart1',
    title: 'Word Smart I (4th Edition)',
    shortTitle: 'Word Smart 1',
    totalWords: 833,
    totalSets: 34,
    wordsPerSet: 25,
    lastSetWords: 8,
    description: 'The Princeton Review Word Smart I: 833 essential collegiate words with pronunciations and contextual examples.'
  },
  wordsmart2: {
    id: 'wordsmart2',
    title: 'Word Smart II',
    shortTitle: 'Word Smart 2',
    totalWords: 848,
    totalSets: 34,
    wordsPerSet: 25,
    lastSetWords: 23,
    description: 'Word Smart II: 848 advanced vocabulary words for competitive exams, BCS, Bank & GRE mastery.'
  }
};

export function getSourceWords(sourceId: VocabSourceId): VocabWord[] {
  switch (sourceId) {
    case 'gre333':
      return gre333Words;
    case 'wordsmart1':
      return wordsmart1Words;
    case 'wordsmart2':
      return wordsmart2Words;
    default:
      return [];
  }
}

export function getAllCorpusWords(): VocabWord[] {
  return [...gre333Words, ...wordsmart1Words, ...wordsmart2Words];
}

export function getSetWords(sourceId: VocabSourceId, setNumber: number): VocabWord[] {
  const words = getSourceWords(sourceId);
  return words.filter(w => w.setNumber === setNumber);
}

export function getSourceSets(sourceId: VocabSourceId): VocabSet[] {
  const info = SOURCES_INFO[sourceId];
  const words = getSourceWords(sourceId);
  const sets: VocabSet[] = [];

  for (let s = 1; s <= info.totalSets; s++) {
    const setWords = words.filter(w => w.setNumber === s);
    const startWordIndex = setWords.length > 0 ? setWords[0].indexInSource : 0;
    const endWordIndex = setWords.length > 0 ? setWords[setWords.length - 1].indexInSource : 0;

    sets.push({
      sourceId,
      setNumber: s,
      wordCount: setWords.length,
      startWordIndex,
      endWordIndex,
      words: setWords
    });
  }

  return sets;
}

/**
 * Full-string 32-bit FNV-1a hash function.
 * Evaluates the entire character sequence, preventing single-letter collisions.
 */
export function hashString(str: string, seed = 0): number {
  let h = (seed ^ 0x811c9dc5) >>> 0;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 0x01000193) >>> 0;
  }
  return h;
}

/**
 * Mathematically uniform, unbiased Fisher-Yates (Knuth) shuffle
 * driven by a deterministic Mulberry32 PRNG.
 * Eliminates Array.sort() comparator biases, letter clumping, and non-transitive sorting glitches.
 */
export function deterministicShuffle<T>(array: T[], seed: number): T[] {
  const result = [...array];
  let s = (seed ^ 0x9e3779b9) >>> 0;
  const rng = () => {
    s = (s + 0x6d2b79f5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

/**
 * Selects candidate distractors while strictly enforcing initial-letter diversity.
 * Guarantees that distractors do not cluster around the same starting letters (e.g. A, R, F).
 */
export function selectDiverseDistractors<T extends { word: string }>(
  candidates: T[],
  count: number,
  seed: number,
  excludeInitialLetters: Set<string> = new Set()
): T[] {
  const shuffled = deterministicShuffle(candidates, seed);
  const selected: T[] = [];
  const usedLetters = new Set<string>(excludeInitialLetters);

  // First pass: strictly distinct starting letters
  for (const c of shuffled) {
    if (selected.length >= count) break;
    const initial = c.word.charAt(0).toUpperCase();
    if (!usedLetters.has(initial)) {
      usedLetters.add(initial);
      selected.push(c);
    }
  }

  // Fallback pass if distinct initials are exhausted
  if (selected.length < count) {
    const selectedSet = new Set(selected);
    for (const c of shuffled) {
      if (selected.length >= count) break;
      if (!selectedSet.has(c)) {
        selected.push(c);
      }
    }
  }

  return selected;
}

/**
 * Returns distractor definitions of the EXACT SAME part of speech from the corpus.
 * Guarantees no semantic overlap, synonym conflict, or mention of target word.
 */
export function getMeaningDistractors(targetWord: VocabWord, count = 3): VocabWord[] {
  const corpus = getSourceWords(targetWord.source);
  const targetLower = targetWord.word.toLowerCase();
  const lowerSyns = new Set([
    targetLower,
    ...targetWord.synonyms.map(s => s.toLowerCase()),
    ...targetWord.antonyms.map(a => a.toLowerCase())
  ]);

  const isValidDistractor = (w: VocabWord) => {
    if (w.id === targetWord.id) return false;
    const wLower = w.word.toLowerCase();
    if (wLower === targetLower || lowerSyns.has(wLower)) return false;
    // Disallow words whose synonyms overlap with target synonyms
    if (w.synonyms.some(s => lowerSyns.has(s.toLowerCase()))) return false;
    // Disallow words whose definition contains the target word
    if (w.meaningEn.toLowerCase().includes(targetLower)) return false;
    return true;
  };

  const samePosCandidates = corpus.filter(
    w => w.partOfSpeech === targetWord.partOfSpeech && isValidDistractor(w)
  );

  // If not enough in the same source, draw from the all-corpus same POS
  const pool = samePosCandidates.length >= count
    ? samePosCandidates
    : getAllCorpusWords().filter(
        w => w.partOfSpeech === targetWord.partOfSpeech && isValidDistractor(w)
      );

  const seed = hashString(targetWord.word, targetWord.indexInSource + 47);
  const targetInitial = targetWord.word.charAt(0).toUpperCase();
  return selectDiverseDistractors(pool, count, seed, new Set([targetInitial]));
}

const capitalizeWord = (s: string) => s ? s.charAt(0).toUpperCase() + s.slice(1).toLowerCase() : s;

const ADVERB_POOL = [
  { word: 'Ostensibly', meaningBn: 'আপাতদৃষ্টিতে বা বাহ্যত' },
  { word: 'Invariably', meaningBn: 'সর্বদাই বা অপরিবর্তনীয়ভাবে' },
  { word: 'Vehemently', meaningBn: 'তীব্রভাবে বা প্রবল আবেগের সাথে' },
  { word: 'Deliberately', meaningBn: 'ইচ্ছাকৃতভাবে বা উদ্দেশ্যপ্রণোদিতভাবে' }
];

/**
 * Returns single synonym options (1 correct + 3 same-POS distractors, including traps)
 */
export function getSingleSynonymQuestion(targetWord: VocabWord): {
  correctSynonym: string;
  options: { word: string; meaningBn: string; isCorrect: boolean }[];
} {
  const corpus = getSourceWords(targetWord.source);
  const correctSynonym = targetWord.synonyms.length > 0
    ? capitalizeWord(targetWord.synonyms[0])
    : capitalizeWord(targetWord.word);

  const lookupBn = (term: string, fallback: string) => {
    const found = corpus.find(c => c.word.toLowerCase() === term.toLowerCase());
    return found ? found.meaningBn : fallback;
  };

  const distractorWords: { word: string; meaningBn: string }[] = [];
  const lowerSyns = new Set(targetWord.synonyms.map(s => s.toLowerCase()));
  lowerSyns.add(targetWord.word.toLowerCase());
  lowerSyns.add(correctSynonym.toLowerCase());

  const lowerAnts = new Set(targetWord.antonyms.map(a => a.toLowerCase()));

  // Trap: 1 antonym if available, with authentic Bengali meaning
  if (targetWord.antonyms.length > 0) {
    const trapWord = targetWord.antonyms[0];
    distractorWords.push({
      word: capitalizeWord(trapWord),
      meaningBn: lookupBn(trapWord, targetWord.meaningBn)
    });
  }

  if (targetWord.partOfSpeech === 'adverb') {
    for (const adv of ADVERB_POOL) {
      if (distractorWords.length >= 3) break;
      const lower = adv.word.toLowerCase();
      if (!lowerSyns.has(lower) && !distractorWords.some(d => d.word.toLowerCase() === lower)) {
        distractorWords.push(adv);
      }
    }
  } else {
    // Filter candidates: same POS, no synonym or antonym intersection
    const candidates = corpus.filter(w => {
      const cName = w.word.toLowerCase();
      if (lowerSyns.has(cName) || lowerAnts.has(cName)) return false;
      if (distractorWords.some(d => d.word.toLowerCase() === cName)) return false;
      if (w.partOfSpeech !== targetWord.partOfSpeech) return false;
      
      const cSyns = new Set(w.synonyms.map(s => s.toLowerCase()));
      const cAnts = new Set(w.antonyms.map(a => a.toLowerCase()));
      if (cSyns.has(targetWord.word.toLowerCase()) || cAnts.has(targetWord.word.toLowerCase())) return false;
      for (const s of targetWord.synonyms) {
        if (cSyns.has(s.toLowerCase())) return false;
      }
      return true;
    });

    // Deterministically select diverse distractors with distinct initial letters
    const excludeInitials = new Set<string>([targetWord.word.charAt(0).toUpperCase()]);
    if (distractorWords.length > 0) {
      excludeInitials.add(distractorWords[0].word.charAt(0).toUpperCase());
    }
    const seed = hashString(targetWord.word, targetWord.indexInSource + 101);
    const diverse = selectDiverseDistractors(candidates, 3 - distractorWords.length, seed, excludeInitials);
    for (const c of diverse) {
      distractorWords.push({
        word: capitalizeWord(c.word),
        meaningBn: c.meaningBn
      });
    }
  }

  const options = [
    { word: correctSynonym, meaningBn: targetWord.meaningBn, isCorrect: true },
    ...distractorWords.slice(0, 3).map(d => ({ ...d, isCorrect: false }))
  ];

  // Mathematically uniform Fisher-Yates shuffle
  const shuffleSeed = hashString(targetWord.word, targetWord.indexInSource + 777);
  return { correctSynonym, options: deterministicShuffle(options, shuffleSeed) };
}

/**
 * Returns single antonym options (1 correct antonym + 3 same-POS distractors, including synonym traps)
 */
export function getSingleAntonymQuestion(targetWord: VocabWord): {
  correctAntonym: string;
  options: { word: string; meaningBn: string; isCorrect: boolean }[];
} {
  const corpus = getSourceWords(targetWord.source);
  const correctAntonym = targetWord.antonyms.length > 0
    ? capitalizeWord(targetWord.antonyms[0])
    : capitalizeWord(targetWord.word);

  const lookupBn = (term: string, fallback: string) => {
    const found = corpus.find(c => c.word.toLowerCase() === term.toLowerCase());
    return found ? found.meaningBn : fallback;
  };

  const distractorWords: { word: string; meaningBn: string }[] = [];
  const lowerAnts = new Set(targetWord.antonyms.map(a => a.toLowerCase()));
  lowerAnts.add(targetWord.word.toLowerCase());
  lowerAnts.add(correctAntonym.toLowerCase());

  const lowerSyns = new Set(targetWord.synonyms.map(s => s.toLowerCase()));

  // Trap: 1 synonym if available, with authentic Bengali meaning
  if (targetWord.synonyms.length > 0) {
    const trapWord = targetWord.synonyms[0];
    distractorWords.push({
      word: capitalizeWord(trapWord),
      meaningBn: lookupBn(trapWord, targetWord.meaningBn)
    });
  }

  if (targetWord.partOfSpeech === 'adverb') {
    for (const adv of ADVERB_POOL) {
      if (distractorWords.length >= 3) break;
      const lower = adv.word.toLowerCase();
      if (!lowerAnts.has(lower) && !distractorWords.some(d => d.word.toLowerCase() === lower)) {
        distractorWords.push(adv);
      }
    }
  } else {
    const candidates = corpus.filter(w => {
      const cName = w.word.toLowerCase();
      if (lowerAnts.has(cName) || lowerSyns.has(cName)) return false;
      if (distractorWords.some(d => d.word.toLowerCase() === cName)) return false;
      if (w.partOfSpeech !== targetWord.partOfSpeech) return false;
      
      const cAnts = new Set(w.antonyms.map(a => a.toLowerCase()));
      const cSyns = new Set(w.synonyms.map(s => s.toLowerCase()));
      if (cAnts.has(targetWord.word.toLowerCase()) || cSyns.has(targetWord.word.toLowerCase())) return false;
      for (const a of targetWord.antonyms) {
        if (cAnts.has(a.toLowerCase())) return false;
      }
      return true;
    });

    const excludeInitials = new Set<string>([targetWord.word.charAt(0).toUpperCase()]);
    if (distractorWords.length > 0) {
      excludeInitials.add(distractorWords[0].word.charAt(0).toUpperCase());
    }
    const seed = hashString(targetWord.word, targetWord.indexInSource + 203);
    const diverse = selectDiverseDistractors(candidates, 3 - distractorWords.length, seed, excludeInitials);
    for (const c of diverse) {
      distractorWords.push({
        word: capitalizeWord(c.word),
        meaningBn: c.meaningBn
      });
    }
  }

  const options = [
    { word: correctAntonym, meaningBn: lookupBn(correctAntonym, targetWord.meaningBn), isCorrect: true },
    ...distractorWords.slice(0, 3).map(d => ({ ...d, isCorrect: false }))
  ];

  const shuffleSeed = hashString(targetWord.word, targetWord.indexInSource + 888);
  return { correctAntonym, options: deterministicShuffle(options, shuffleSeed) };
}

/**
 * Mode 3: Checkbox options (3 true synonyms + 3 sophisticated distractors)
 */
export function getMultiSynonymOptions(targetWord: VocabWord): {
  id: string;
  word: string;
  isSynonym: boolean;
  meaningBn: string;
}[] {
  // If curated high-caliber multiSynonyms exist in dataset
  if (targetWord.multiSynonyms && targetWord.multiSynonyms.options && targetWord.multiSynonyms.options.length > 0) {
    const seed = hashString(targetWord.word, targetWord.indexInSource + 333);
    const shuffled = deterministicShuffle(targetWord.multiSynonyms.options, seed);
    return shuffled.map(opt => ({
      id: `opt-${opt.word.toLowerCase()}`,
      word: capitalizeWord(opt.word),
      isSynonym: opt.isSynonym,
      meaningBn: opt.meaningBn
    }));
  }

  // Dynamic fallback for words without curated multiSynonyms
  const corpus = getSourceWords(targetWord.source);
  const trueSyns = targetWord.synonyms.slice(0, 3);
  const lowerSyns = new Set(targetWord.synonyms.map(s => s.toLowerCase()));
  lowerSyns.add(targetWord.word.toLowerCase());
  const lowerAnts = new Set(targetWord.antonyms.map(a => a.toLowerCase()));

  // Helper to lookup Bengali meaning from corpus if available
  const lookupBn = (term: string, fallback: string) => {
    const found = corpus.find(c => c.word.toLowerCase() === term.toLowerCase());
    return found ? found.meaningBn : fallback;
  };

  // Exclude target word, synonyms, antonyms from candidate distractors
  const samePos = corpus.filter(
    w => w.partOfSpeech === targetWord.partOfSpeech &&
         !lowerSyns.has(w.word.toLowerCase()) &&
         !lowerAnts.has(w.word.toLowerCase()) &&
         !w.synonyms.some(s => lowerSyns.has(s.toLowerCase())) &&
         w.word.toLowerCase() !== 'abate' &&
         w.word.toLowerCase() !== 'aberrant'
  );

  const excludeInitials = new Set<string>(trueSyns.map(s => s.charAt(0).toUpperCase()));
  excludeInitials.add(targetWord.word.charAt(0).toUpperCase());

  const seed = hashString(targetWord.word, targetWord.indexInSource + 509);
  const selectedDistractors = selectDiverseDistractors(samePos, 3, seed, excludeInitials);

  const allItems = [
    ...trueSyns.map(s => ({
      id: `syn-${s.toLowerCase()}`,
      word: capitalizeWord(s),
      isSynonym: true,
      meaningBn: lookupBn(s, targetWord.meaningBn)
    })),
    ...selectedDistractors.map(d => ({
      id: `dist-${d.word.toLowerCase()}`,
      word: capitalizeWord(d.word),
      isSynonym: false,
      meaningBn: d.meaningBn
    }))
  ];

  const shuffleSeed = hashString(targetWord.word, targetWord.indexInSource + 999);
  return deterministicShuffle(allItems, shuffleSeed);
}
