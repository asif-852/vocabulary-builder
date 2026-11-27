import { useState, useEffect, useCallback } from 'react';
import { VocabWord, VocabSourceId } from '../data/vocabSchema';
import {
  isSourceLoaded,
  areAllSourcesLoaded,
  getSetWords,
  loadSourceWords,
  loadAllCorpusWords,
  setNeedsAllCorporaForMeaning,
  prefetchBanglaFont
} from '../data/index';

interface UseSetWordsOptions {
  /** Set true in FindMeaningMode so rare POS cross-corpus distractor fallbacks are loaded if needed. */
  ensureMeaningCrossCorpus?: boolean;
}

interface UseSetWordsResult {
  words: VocabWord[];
  loading: boolean;
  error: string | null;
  retry: () => void;
}

function getReadyWords(
  sourceId: VocabSourceId,
  setNumber: number,
  ensureMeaningCrossCorpus: boolean
): VocabWord[] | null {
  if (!isSourceLoaded(sourceId)) return null;
  if (
    ensureMeaningCrossCorpus &&
    setNeedsAllCorporaForMeaning(sourceId, setNumber) &&
    !areAllSourcesLoaded()
  ) {
    return null;
  }
  return getSetWords(sourceId, setNumber);
}

export function useSetWords(
  sourceId: VocabSourceId,
  setNumber: number,
  options: UseSetWordsOptions = {}
): UseSetWordsResult {
  const ensureMeaningCrossCorpus = Boolean(options.ensureMeaningCrossCorpus);
  const [attempt, setAttempt] = useState(0);

  const [state, setState] = useState<{
    key: string;
    words: VocabWord[];
    loading: boolean;
    error: string | null;
  }>(() => {
    const ready = getReadyWords(sourceId, setNumber, ensureMeaningCrossCorpus);
    return {
      key: `${sourceId}:${setNumber}:${ensureMeaningCrossCorpus}`,
      words: ready ?? [],
      loading: ready === null,
      error: null
    };
  });

  useEffect(() => {
    prefetchBanglaFont();
  }, []);

  useEffect(() => {
    const currentKey = `${sourceId}:${setNumber}:${ensureMeaningCrossCorpus}`;
    const ready = getReadyWords(sourceId, setNumber, ensureMeaningCrossCorpus);
    if (ready !== null) {
      setState({ key: currentKey, words: ready, loading: false, error: null });
      return;
    }

    let cancelled = false;
    setState(prev => ({ ...prev, key: currentKey, loading: true, error: null }));

    (async () => {
      await loadSourceWords(sourceId);
      if (ensureMeaningCrossCorpus && setNeedsAllCorporaForMeaning(sourceId, setNumber)) {
        await loadAllCorpusWords();
      }
      if (!cancelled) {
        setState({
          key: currentKey,
          words: getSetWords(sourceId, setNumber),
          loading: false,
          error: null
        });
      }
    })().catch(err => {
      if (!cancelled) {
        setState({
          key: currentKey,
          words: [],
          loading: false,
          error: err instanceof Error ? err.message : 'Failed to load vocabulary data.'
        });
      }
    });

    return () => {
      cancelled = true;
    };
  }, [sourceId, setNumber, ensureMeaningCrossCorpus, attempt]);

  const retry = useCallback(() => {
    setAttempt(a => a + 1);
  }, []);

  const currentKey = `${sourceId}:${setNumber}:${ensureMeaningCrossCorpus}`;
  if (state.key !== currentKey) {
    const ready = getReadyWords(sourceId, setNumber, ensureMeaningCrossCorpus);
    return {
      words: ready ?? [],
      loading: ready === null,
      error: null,
      retry
    };
  }

  return {
    words: state.words,
    loading: state.loading,
    error: state.error,
    retry
  };
}
