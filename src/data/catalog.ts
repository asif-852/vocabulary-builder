import { VocabSourceId } from './vocabSchema';

export interface SourceInfo {
  id: VocabSourceId;
  title: string;
  shortTitle: string;
  totalWords: number;
  totalSets: number;
  wordsPerSet: number;
  lastSetWords: number;
  description: string;
}

export interface VocabSetMeta {
  sourceId: VocabSourceId;
  setNumber: number;
  wordCount: number;
  startWordIndex: number;
  endWordIndex: number;
}

export const SOURCES_INFO: Record<VocabSourceId, SourceInfo> = {
  gre333: {
    id: 'gre333',
    title: 'GRE 333',
    shortTitle: 'GRE 333',
    totalWords: 333,
    totalSets: 17,
    wordsPerSet: 20,
    lastSetWords: 13,
    description: "Barron's 333 high-frequency words"
  },
  wordsmart1: {
    id: 'wordsmart1',
    title: 'Word Smart I',
    shortTitle: 'Word Smart 1',
    totalWords: 833,
    totalSets: 34,
    wordsPerSet: 25,
    lastSetWords: 8,
    description: 'The Princeton Review Word Smart I'
  },
  wordsmart2: {
    id: 'wordsmart2',
    title: 'Word Smart II',
    shortTitle: 'Word Smart 2',
    totalWords: 848,
    totalSets: 34,
    wordsPerSet: 25,
    lastSetWords: 23,
    description: 'The Princeton Review Word Smart II'
  }
};

function formatWordId(sourceId: VocabSourceId, indexInSource: number): string {
  return `${sourceId}-${String(indexInSource).padStart(3, '0')}`;
}

export function getSetWordRange(sourceId: VocabSourceId, setNumber: number): VocabSetMeta {
  const info = SOURCES_INFO[sourceId];
  if (setNumber < 1 || setNumber > info.totalSets) {
    return { sourceId, setNumber, wordCount: 0, startWordIndex: 0, endWordIndex: 0 };
  }
  const startWordIndex = (setNumber - 1) * info.wordsPerSet + 1;
  const wordCount = setNumber === info.totalSets ? info.lastSetWords : info.wordsPerSet;
  const endWordIndex = startWordIndex + wordCount - 1;
  return { sourceId, setNumber, wordCount, startWordIndex, endWordIndex };
}

export function getSourceSetsMeta(sourceId: VocabSourceId): VocabSetMeta[] {
  const info = SOURCES_INFO[sourceId];
  const sets: VocabSetMeta[] = [];
  for (let s = 1; s <= info.totalSets; s++) {
    sets.push(getSetWordRange(sourceId, s));
  }
  return sets;
}

export function getSetWordIds(sourceId: VocabSourceId, setNumber: number): string[] {
  const { startWordIndex, endWordIndex, wordCount } = getSetWordRange(sourceId, setNumber);
  if (wordCount === 0) return [];
  const ids: string[] = [];
  for (let i = startWordIndex; i <= endWordIndex; i++) {
    ids.push(formatWordId(sourceId, i));
  }
  return ids;
}

export function getSourceWordIds(sourceId: VocabSourceId): string[] {
  const { totalWords } = SOURCES_INFO[sourceId];
  const ids: string[] = [];
  for (let i = 1; i <= totalWords; i++) {
    ids.push(formatWordId(sourceId, i));
  }
  return ids;
}
