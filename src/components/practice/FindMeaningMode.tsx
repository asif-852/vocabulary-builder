import React, { useState, useMemo } from 'react';
import { VocabWord, VocabSourceId } from '../../data/vocabSchema';
import { getSetWords, getMeaningDistractors, deterministicShuffle, hashString } from '../../data/index';
import { ArrowLeft, ArrowRight, RotateCcw, Check, X } from 'lucide-react';

interface FindMeaningModeProps {
  sourceId: VocabSourceId;
  setNumber: number;
  onBackToHub: () => void;
}

interface QuestionState {
  selectedIndex: number | null;
  isAnswered: boolean;
  isCorrect: boolean;
}

export const FindMeaningMode: React.FC<FindMeaningModeProps> = ({
  sourceId,
  setNumber,
  onBackToHub
}) => {
  const words = getSetWords(sourceId, setNumber);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, QuestionState>>({});

  // Prepare questions with deterministic 4 options
  const questions = useMemo(() => {
    return words.map((word, qIdx) => {
      const distractors = getMeaningDistractors(word, 3);
      const rawOptions = [
        { text: word.meaningEn, isCorrect: true, word },
        ...distractors.map(d => ({ text: d.meaningEn, isCorrect: false, word: d }))
      ];

      // Shuffle deterministically using uniform Fisher-Yates PRNG
      const seed = hashString(word.word, word.indexInSource + 307);
      const shuffled = deterministicShuffle(rawOptions, seed);

      return {
        targetWord: word,
        options: shuffled
      };
    });
  }, [words]);

  const currentQ = questions[currentIndex];
  const currentState = answers[currentIndex] || { selectedIndex: null, isAnswered: false, isCorrect: false };

  // Calculate score
  const totalAnswered = Object.values(answers).filter(a => a.isAnswered).length;
  const totalCorrect = Object.values(answers).filter(a => a.isCorrect).length;
  const isComplete = currentIndex >= questions.length;

  const handleSelectOption = (optIndex: number) => {
    if (currentState.isAnswered) return; // Already answered

    const isCorrect = currentQ.options[optIndex].isCorrect;
    setAnswers(prev => ({
      ...prev,
      [currentIndex]: {
        selectedIndex: optIndex,
        isAnswered: true,
        isCorrect
      }
    }));
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(prev => prev + 1);
    } else {
      // Completed Set Screen
      setCurrentIndex(questions.length);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex(prev => prev - 1);
    }
  };

  const handleRetry = () => {
    setAnswers({});
    setCurrentIndex(0);
  };

  // Completion View
  if (isComplete) {
    const scorePct = Math.round((totalCorrect / questions.length) * 100);
    return (
      <div style={{ maxWidth: '640px', margin: '0 auto', textAlign: 'center', padding: '32px 16px' }}>
        <div style={{
          backgroundColor: '#ffffff',
          borderRadius: 'var(--radius-lg)',
          border: '1px solid var(--border-color)',
          padding: '36px 24px',
          boxShadow: 'var(--shadow-md)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '16px'
        }}>
          <div style={{
            width: '64px',
            height: '64px',
            borderRadius: '50%',
            backgroundColor: scorePct >= 70 ? '#f0fdf4' : '#eff6ff',
            color: scorePct >= 70 ? '#16a34a' : '#2563eb',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.5rem',
            fontWeight: 700
          }}>
            {scorePct}%
          </div>

          <h2 style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)' }}>
            Set {setNumber} — Find the Meaning Complete!
          </h2>

          <p style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>
            You scored <strong>{totalCorrect}</strong> out of <strong>{questions.length}</strong> correct.
          </p>

          <div style={{ display: 'flex', gap: '12px', marginTop: '12px' }}>
            <button
              onClick={handleRetry}
              className="pill-button"
              style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}
            >
              <RotateCcw size={16} />
              <span>Retry this set</span>
            </button>
            <button
              onClick={onBackToHub}
              className="pill-button active"
              style={{ backgroundColor: '#0f172a', borderColor: '#0f172a' }}
            >
              Back to Practice Modes
            </button>
          </div>
        </div>
      </div>
    );
  }

  const letters = ['A', 'B', 'C', 'D'];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', maxWidth: '720px', margin: '0 auto', width: '100%' }}>
      {/* 6.1 Top Bar */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '8px'
      }}>
        <button
          onClick={onBackToHub}
          className="pill-button"
          style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}
        >
          <ArrowLeft size={16} />
          <span>Practice Modes</span>
        </button>

        <div style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
          Set {setNumber}: Find the Meaning
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span style={{ fontSize: '0.85rem', fontWeight: 600, color: '#2563eb' }}>
            Score: {totalCorrect}
          </span>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
            Q {currentIndex + 1} of {questions.length}
          </span>
        </div>
      </div>

      {/* Main Question Card */}
      <div style={{
        backgroundColor: '#ffffff',
        border: '1px solid var(--border-color)',
        borderRadius: 'var(--radius-lg)',
        padding: '24px',
        boxShadow: 'var(--shadow-sm)',
        display: 'flex',
        flexDirection: 'column',
        gap: '18px'
      }}>
        {/* Prompt */}
        <div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>
            Choose the correct definition:
          </div>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: '10px', marginTop: '4px', flexWrap: 'wrap' }}>
            <h2 style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '0.02em' }}>
              {currentQ.targetWord.word.toUpperCase()}
            </h2>
            {currentState.isAnswered && (
              <>
                <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)', fontStyle: 'italic' }}>
                  ({currentQ.targetWord.partOfSpeech})
                </span>
                <span className="bangla-text" style={{ fontSize: '1.1rem', color: '#15803d', fontWeight: 600 }}>
                  ({currentQ.targetWord.meaningBn})
                </span>
              </>
            )}
          </div>
        </div>

        {/* Options */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {currentQ.options.map((opt, optIdx) => {
            let bg = '#ffffff';
            let borderColor = 'var(--border-color)';
            let textColor = 'var(--text-primary)';

            if (currentState.isAnswered) {
              if (opt.isCorrect) {
                bg = 'var(--success-bg)';
                borderColor = 'var(--success)';
                textColor = '#15803d';
              } else if (currentState.selectedIndex === optIdx) {
                bg = 'var(--danger-bg)';
                borderColor = 'var(--danger)';
                textColor = '#b91c1c';
              } else {
                textColor = 'var(--text-muted)';
              }
            }

            return (
              <div
                key={optIdx}
                onClick={() => handleSelectOption(optIdx)}
                style={{
                  backgroundColor: bg,
                  border: `1.5px solid ${borderColor}`,
                  borderRadius: 'var(--radius-md)',
                  padding: '12px 16px',
                  cursor: currentState.isAnswered ? 'default' : 'pointer',
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '12px',
                  transition: 'background-color 0.15s, border-color 0.15s'
                }}
              >
                <div style={{
                  width: '26px',
                  height: '26px',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '0.85rem',
                  fontWeight: 700,
                  backgroundColor: currentState.isAnswered && opt.isCorrect
                    ? '#16a34a'
                    : currentState.isAnswered && currentState.selectedIndex === optIdx
                    ? '#dc2626'
                    : '#f1f5f9',
                  color: (currentState.isAnswered && (opt.isCorrect || currentState.selectedIndex === optIdx))
                    ? '#ffffff'
                    : 'var(--text-secondary)',
                  flexShrink: 0
                }}>
                  {letters[optIdx]}
                </div>

                <div style={{ fontSize: '0.95rem', color: textColor, lineHeight: 1.45, flex: 1, paddingTop: '2px' }}>
                  {opt.text}
                </div>
              </div>
            );
          })}
        </div>

        {/* Post-Answer Feedback Box */}
        {currentState.isAnswered && (
          <div style={{
            backgroundColor: currentState.isCorrect ? '#f0fdf4' : '#fef2f2',
            border: `1px solid ${currentState.isCorrect ? '#bbf7d0' : '#fecaca'}`,
            borderRadius: 'var(--radius-md)',
            padding: '14px 16px',
            display: 'flex',
            flexDirection: 'column',
            gap: '6px'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              {currentState.isCorrect ? (
                <>
                  <Check size={18} color="#16a34a" />
                  <strong style={{ color: '#15803d' }}>Correct!</strong>
                </>
              ) : (
                <>
                  <X size={18} color="#dc2626" />
                  <strong style={{ color: '#b91c1c' }}>Incorrect.</strong>
                </>
              )}
            </div>
            <div style={{ fontSize: '0.9rem', color: '#1e293b' }}>
              <strong>{currentQ.targetWord.word}</strong> means: <em>{currentQ.targetWord.meaningEn}</em>
            </div>
            <div className="bangla-text" style={{ fontSize: '0.95rem', color: '#334155' }}>
              বাংলা অর্থ: <strong>{currentQ.targetWord.meaningBn}</strong>
              {currentQ.targetWord.synonyms.length > 0 && (
                <span style={{ marginLeft: '8px' }}>
                  (Synonyms: {currentQ.targetWord.synonyms.join(', ')})
                </span>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Bottom Nav */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <button
          onClick={handlePrev}
          disabled={currentIndex === 0}
          className="pill-button"
          style={{ opacity: currentIndex === 0 ? 0.4 : 1, cursor: currentIndex === 0 ? 'not-allowed' : 'pointer' }}
        >
          <ArrowLeft size={16} />
          <span>Previous</span>
        </button>

        <button
          onClick={handleNext}
          className="pill-button active"
          style={{ backgroundColor: '#2563eb', borderColor: '#2563eb' }}
        >
          <span>{currentIndex === questions.length - 1 ? 'Finish Drill' : 'Next'}</span>
          <ArrowRight size={16} />
        </button>
      </div>
    </div>
  );
};
