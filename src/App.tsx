import React, { useState } from 'react';
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

  const handleSelectSource = (sourceId: VocabSourceId) => {
    setActiveSource(sourceId);
    try {
      localStorage.setItem('vocab_builder_active_source', sourceId);
    } catch (e) {
      console.error(e);
    }
  };

  const handleGoHome = () => {
    setView({ type: 'home' });
  };

  const handleSelectSet = (sourceId: VocabSourceId, setNumber: number) => {
    handleSelectSource(sourceId);
    setView({ type: 'set_hub', sourceId, setNumber });
  };

  const handleStartStudy = (sourceId: VocabSourceId, setNumber: number) => {
    handleSelectSource(sourceId);
    setView({ type: 'study', sourceId, setNumber });
  };

  const handleStartPractice = (sourceId: VocabSourceId, setNumber: number) => {
    handleSelectSource(sourceId);
    setView({ type: 'practice_hub', sourceId, setNumber });
  };

  const handleSelectPracticeMode = (sourceId: VocabSourceId, setNumber: number, mode: PracticeModeId) => {
    handleSelectSource(sourceId);
    setView({ type: 'practice_drill', sourceId, setNumber, mode });
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
            sourceId={view.sourceId}
            setNumber={view.setNumber}
            onBackToSet={() => setView({ type: 'set_hub', sourceId: view.sourceId, setNumber: view.setNumber })}
            progress={progress}
          />
        )}

        {view.type === 'practice_hub' && (
          <PracticeHub
            sourceId={view.sourceId}
            setNumber={view.setNumber}
            onBackToSet={() => setView({ type: 'set_hub', sourceId: view.sourceId, setNumber: view.setNumber })}
            onSelectMode={(mode) => handleSelectPracticeMode(view.sourceId, view.setNumber, mode)}
          />
        )}

        {view.type === 'practice_drill' && (
          <>
            {view.mode === 'meaning' && (
              <FindMeaningMode
                sourceId={view.sourceId}
                setNumber={view.setNumber}
                onBackToHub={() => setView({ type: 'practice_hub', sourceId: view.sourceId, setNumber: view.setNumber })}
              />
            )}
            {view.mode === 'sentence' && (
              <SentenceCompletionMode
                sourceId={view.sourceId}
                setNumber={view.setNumber}
                onBackToHub={() => setView({ type: 'practice_hub', sourceId: view.sourceId, setNumber: view.setNumber })}
              />
            )}
            {view.mode === 'multi_synonym' && (
              <MultiSynonymMode
                sourceId={view.sourceId}
                setNumber={view.setNumber}
                onBackToHub={() => setView({ type: 'practice_hub', sourceId: view.sourceId, setNumber: view.setNumber })}
              />
            )}
            {view.mode === 'single_synonym' && (
              <SingleSynonymMode
                sourceId={view.sourceId}
                setNumber={view.setNumber}
                onBackToHub={() => setView({ type: 'practice_hub', sourceId: view.sourceId, setNumber: view.setNumber })}
              />
            )}
            {view.mode === 'single_antonym' && (
              <SingleAntonymMode
                sourceId={view.sourceId}
                setNumber={view.setNumber}
                onBackToHub={() => setView({ type: 'practice_hub', sourceId: view.sourceId, setNumber: view.setNumber })}
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
