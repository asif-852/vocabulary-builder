import { useState, useCallback } from 'react';
import { VocabSourceId } from '../data/vocabSchema';
import { getSourceWordIds, getSetWordIds } from '../data/catalog';

const STORAGE_KEY = 'vocab_builder_studied_words_v1';

export type SetStudyStatus = 'not_started' | 'in_progress' | 'completed';

export interface SetProgressInfo {
  studiedCount: number;
  totalCount: number;
  status: SetStudyStatus;
  percentage: number;
}

export interface SourceProgressInfo {
  studiedCount: number;
  totalCount: number;
  percentage: number;
}

export function useStudyProgress() {
  const [studiedWordIds, setStudiedWordIds] = useState<Set<string>>(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const arr = JSON.parse(saved);
        if (Array.isArray(arr)) {
          return new Set<string>(arr);
        }
      }
    } catch (e) {
      console.error('Failed to load studied words from localStorage:', e);
    }
    return new Set<string>();
  });

  // Sync to localStorage
  const saveToStorage = useCallback((ids: Set<string>) => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(Array.from(ids)));
    } catch (e) {
      console.error('Failed to save studied words to localStorage:', e);
    }
  }, []);

  const isWordStudied = useCallback((wordId: string): boolean => {
    return studiedWordIds.has(wordId);
  }, [studiedWordIds]);

  const markWordStudied = useCallback((wordId: string, studied = true) => {
    setStudiedWordIds(prev => {
      const next = new Set(prev);
      if (studied) {
        next.add(wordId);
      } else {
        next.delete(wordId);
      }
      saveToStorage(next);
      return next;
    });
  }, [saveToStorage]);

  const markMultipleWordsStudied = useCallback((wordIds: string[], studied = true) => {
    setStudiedWordIds(prev => {
      const next = new Set(prev);
      for (const id of wordIds) {
        if (studied) next.add(id);
        else next.delete(id);
      }
      saveToStorage(next);
      return next;
    });
  }, [saveToStorage]);

  const getSetProgress = useCallback((sourceId: VocabSourceId, setNumber: number): SetProgressInfo => {
    const wordIds = getSetWordIds(sourceId, setNumber);
    const totalCount = wordIds.length;
    if (totalCount === 0) {
      return { studiedCount: 0, totalCount: 0, status: 'not_started', percentage: 0 };
    }

    let studiedCount = 0;
    for (const id of wordIds) {
      if (studiedWordIds.has(id)) {
        studiedCount++;
      }
    }

    let status: SetStudyStatus = 'not_started';
    if (studiedCount === totalCount) {
      status = 'completed';
    } else if (studiedCount > 0) {
      status = 'in_progress';
    }

    const percentage = Math.round((studiedCount / totalCount) * 100);
    return { studiedCount, totalCount, status, percentage };
  }, [studiedWordIds]);

  const getSourceProgress = useCallback((sourceId: VocabSourceId): SourceProgressInfo => {
    const wordIds = getSourceWordIds(sourceId);
    const totalCount = wordIds.length;
    if (totalCount === 0) {
      return { studiedCount: 0, totalCount: 0, percentage: 0 };
    }

    let studiedCount = 0;
    for (const id of wordIds) {
      if (studiedWordIds.has(id)) {
        studiedCount++;
      }
    }

    const percentage = Math.round((studiedCount / totalCount) * 100);
    return { studiedCount, totalCount, percentage };
  }, [studiedWordIds]);

  const resetSourceProgress = useCallback((sourceId: VocabSourceId) => {
    const idsToRemove = new Set(getSourceWordIds(sourceId));

    setStudiedWordIds(prev => {
      const next = new Set(prev);
      for (const id of idsToRemove) {
        next.delete(id);
      }
      saveToStorage(next);
      return next;
    });
  }, [saveToStorage]);

  const resetAllProgress = useCallback(() => {
    const next = new Set<string>();
    setStudiedWordIds(next);
    saveToStorage(next);
  }, [saveToStorage]);

  return {
    studiedWordIds,
    isWordStudied,
    markWordStudied,
    markMultipleWordsStudied,
    getSetProgress,
    getSourceProgress,
    resetSourceProgress,
    resetAllProgress
  };
}
