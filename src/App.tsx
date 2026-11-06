import React, { useState, useEffect, useLayoutEffect, useRef } from 'react';
import { VocabSourceId } from './data/vocabSchema';
import { useStudyProgress } from './hooks/useStudyProgress';
import { Header } from './components/Header';
import { HomeView } from './components/HomeView';
import { SetHubView } from './components/SetHubView';
import { StudyView } from './components/StudyView';
import { PracticeHub, PracticeModeId } from './components/practice/PracticeHub';
import { FindMeaningMode } from './components/practice/FindMeaningMode';
import { SentenceCompletionMode } from './components/practice/SentenceCompletionMode';
import { MultiSynonymMode } from './components/practice/MultiSynonymMode';
import { SingleSynonymMode } from './components/practice/SingleSynonymMode';
import { SingleAntonymMode } from './components/practice/SingleAntonymMode';

type AppView =
  | { type: 'home' }
  | { type: 'set_hub'; sourceId: VocabSourceId; setNumber: number }
  | { type: 'study'; sourceId: VocabSourceId; setNumber: number }
  | { type: 'practice_hub'; sourceId: VocabSourceId; setNumber: number }
  | { type: 'practice_drill'; sourceId: VocabSourceId; setNumber: number; mode: PracticeModeId };

const SCROLL_STORAGE_KEY = 'vocab_builder_scroll_positions';

function loadSavedScrolls(): Record<string, number> {
  try {
    const raw = sessionStorage.getItem(SCROLL_STORAGE_KEY) || localStorage.getItem(SCROLL_STORAGE_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

function saveScrolls(data: Record<string, number>) {
  try {
    const serialized = JSON.stringify(data);
    sessionStorage.setItem(SCROLL_STORAGE_KEY, serialized);
    localStorage.setItem(SCROLL_STORAGE_KEY, serialized);
  } catch {
    // ignore
  }
}

function getViewKey(v: AppView, source: VocabSourceId): string {
  switch (v.type) {
    case 'home':
      return `home_${source}`;
    case 'set_hub':
      return `set_hub_${v.sourceId}_${v.setNumber}`;
    case 'study':
      return `study_${v.sourceId}_${v.setNumber}`;
    case 'practice_hub':
      return `practice_hub_${v.sourceId}_${v.setNumber}`;
    case 'practice_drill':
      return `drill_${v.sourceId}_${v.setNumber}_${v.mode}`;
  }
}

export const App: React.FC = () => {
  const [view, setView] = useState<AppView>({ type: 'home' });
  const [activeSource, setActiveSource] = useState<VocabSourceId>(() => {
    try {
      const saved = localStorage.getItem('vocab_builder_active_source');
      if (saved === 'gre333' || saved === 'wordsmart1' || saved === 'wordsmart2') {
        return saved as VocabSourceId;
      }
    } catch {
      // ignore
    }
    return 'gre333';
  });
  const progress = useStudyProgress();

  const scrollPositions = useRef<Record<string, number>>(loadSavedScrolls());
  const isRestoringRef = useRef<boolean>(false);
  const currentKey = getViewKey(view, activeSource);

  // Disable browser automatic scroll restoration to maintain full SPA control
  useEffect(() => {
    if ('scrollRestoration' in history) {
      history.scrollRestoration = 'manual';
    }
  }, []);

  // Continuously record scroll position of the active view
  useEffect(() => {
    const handleScroll = () => {
      if (isRestoringRef.current) return;
      scrollPositions.current[currentKey] = window.scrollY;
      saveScrolls(scrollPositions.current);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, [currentKey]);

  // Restore scroll position when transitioning views
  useLayoutEffect(() => {
    const targetY = scrollPositions.current[currentKey] ?? 0;
    isRestoringRef.current = true;

    // Immediate restore attempt
    window.scrollTo({ top: targetY, behavior: 'instant' });

    let attempts = 0;
    let timerId: number | null = null;

    const tryRestore = () => {
      window.scrollTo({ top: targetY, behavior: 'instant' });
      attempts++;
      // If layout height hasn't caught up, retry for a few frames
      if (attempts < 5 && Math.abs(window.scrollY - targetY) > 5) {
        timerId = window.setTimeout(tryRestore, 30);
      } else {
        isRestoringRef.current = false;
      }
    };

    const rafId = requestAnimationFrame(tryRestore);

    return () => {
      cancelAnimationFrame(rafId);
      if (timerId !== null) clearTimeout(timerId);
      isRestoringRef.current = false;
    };
  }, [currentKey]);

  const navigateTo = (newView: AppView) => {
    scrollPositions.current[currentKey] = window.scrollY;
    saveScrolls(scrollPositions.current);
    setView(newView);
  };

  const handleSelectSource = (sourceId: VocabSourceId) => {
    if (sourceId !== activeSource) {
      scrollPositions.current[currentKey] = window.scrollY;
      saveScrolls(scrollPositions.current);
    }
    setActiveSource(sourceId);
    try {
      localStorage.setItem('vocab_builder_active_source', sourceId);
    } catch (e) {
      console.error(e);
    }
  };

  const handleGoHome = () => {
    if (view.type === 'home') {
      scrollPositions.current[currentKey] = 0;
      saveScrolls(scrollPositions.current);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      navigateTo({ type: 'home' });
    }
  };

  const handleSelectSet = (sourceId: VocabSourceId, setNumber: number) => {
    handleSelectSource(sourceId);
    navigateTo({ type: 'set_hub', sourceId, setNumber });
  };

  const handleStartStudy = (sourceId: VocabSourceId, setNumber: number) => {
    handleSelectSource(sourceId);
    navigateTo({ type: 'study', sourceId, setNumber });
  };

  const handleStartPractice = (sourceId: VocabSourceId, setNumber: number) => {
    handleSelectSource(sourceId);
    navigateTo({ type: 'practice_hub', sourceId, setNumber });
  };

  const handleSelectPracticeMode = (sourceId: VocabSourceId, setNumber: number, mode: PracticeModeId) => {
    handleSelectSource(sourceId);
    navigateTo({ type: 'practice_drill', sourceId, setNumber, mode });
  };

  return (
    <div className="app-container">
      <Header onGoHome={handleGoHome} />

      <main style={{ flex: 1 }}>
        {view.type === 'home' && (
          <HomeView
            activeSource={activeSource}
            onSelectSource={handleSelectSource}
            onSelectSet={handleSelectSet}
            progress={progress}
          />
        )}

        {view.type === 'set_hub' && (
          <SetHubView
            sourceId={view.sourceId}
            setNumber={view.setNumber}
            onBackToHome={() => {
              handleSelectSource(view.sourceId);
              handleGoHome();
            }}
            onStartStudy={() => handleStartStudy(view.sourceId, view.setNumber)}
            onStartPractice={() => handleStartPractice(view.sourceId, view.setNumber)}
            progress={progress}
          />
        )}

        {view.type === 'study' && (
          <StudyView
            key={`study_${view.sourceId}_${view.setNumber}`}
            sourceId={view.sourceId}
            setNumber={view.setNumber}
            onBackToSet={() => navigateTo({ type: 'set_hub', sourceId: view.sourceId, setNumber: view.setNumber })}
            progress={progress}
          />
        )}

        {view.type === 'practice_hub' && (
          <PracticeHub
            sourceId={view.sourceId}
            setNumber={view.setNumber}
            onBackToSet={() => navigateTo({ type: 'set_hub', sourceId: view.sourceId, setNumber: view.setNumber })}
            onSelectMode={(mode) => handleSelectPracticeMode(view.sourceId, view.setNumber, mode)}
          />
        )}

        {view.type === 'practice_drill' && (
          <>
            {view.mode === 'meaning' && (
              <FindMeaningMode
                sourceId={view.sourceId}
                setNumber={view.setNumber}
                onBackToHub={() => navigateTo({ type: 'practice_hub', sourceId: view.sourceId, setNumber: view.setNumber })}
              />
            )}
            {view.mode === 'sentence' && (
              <SentenceCompletionMode
                sourceId={view.sourceId}
                setNumber={view.setNumber}
                onBackToHub={() => navigateTo({ type: 'practice_hub', sourceId: view.sourceId, setNumber: view.setNumber })}
              />
            )}
            {view.mode === 'multi_synonym' && (
              <MultiSynonymMode
                sourceId={view.sourceId}
                setNumber={view.setNumber}
                onBackToHub={() => navigateTo({ type: 'practice_hub', sourceId: view.sourceId, setNumber: view.setNumber })}
              />
            )}
            {view.mode === 'single_synonym' && (
              <SingleSynonymMode
                sourceId={view.sourceId}
                setNumber={view.setNumber}
                onBackToHub={() => navigateTo({ type: 'practice_hub', sourceId: view.sourceId, setNumber: view.setNumber })}
              />
            )}
            {view.mode === 'single_antonym' && (
              <SingleAntonymMode
                sourceId={view.sourceId}
                setNumber={view.setNumber}
                onBackToHub={() => navigateTo({ type: 'practice_hub', sourceId: view.sourceId, setNumber: view.setNumber })}
              />
            )}
          </>
        )}
      </main>

      <footer style={{
        marginTop: '48px',
        borderTop: '1px solid var(--border-color)',
        paddingTop: '16px',
        textAlign: 'center',
        fontSize: '0.8rem',
        color: 'var(--text-muted)'
      }}>
        Vocabulary Builder · Active-recall vocabulary training
      </footer>
    </div>
  );
};

export default App;
