import React, { useState } from 'react';
import { VocabWord, VocabSourceId } from '../../data/vocabSchema';
import { getSetWords } from '../../data/index';
import { ArrowLeft, ArrowRight, RotateCcw, Check, X } from 'lucide-react';

interface SentenceCompletionModeProps {
  sourceId: VocabSourceId;
  setNumber: number;
  onBackToHub: () => void;
}

interface QuestionState {
  selectedIndex: number | null;
  isAnswered: boolean;
  isCorrect: boolean;
}

export const SentenceCompletionMode: React.FC<SentenceCompletionModeProps> = ({
  sourceId,
  setNumber,
  onBackToHub
}) => {
  const words = getSetWords(sourceId, setNumber);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, QuestionState>>({});

  const currentWord = words[currentIndex];
  const sc = currentWord ? currentWord.sentenceCompletion : null;
  const currentState = answers[currentIndex] || { selectedIndex: null, isAnswered: false, isCorrect: false };

  const totalAnswered = Object.values(answers).filter(a => a.isAnswered).length;
  const totalCorrect = Object.values(answers).filter(a => a.isCorrect).length;
  const isComplete = currentIndex >= words.length;

  const handleSelectOption = (optIndex: number) => {
    if (!sc || currentState.isAnswered) return;

    const isCorrect = optIndex === sc.correctIndex;
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
    if (currentIndex < words.length - 1) {
      setCurrentIndex(prev => prev + 1);
    } else {
      setCurrentIndex(words.length);
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

  if (isComplete) {
    const scorePct = Math.round((totalCorrect / words.length) * 100);
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
            Set {setNumber} — Sentence Completion Complete!
          </h2>

          <p style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>
            You answered <strong>{totalCorrect}</strong> of <strong>{words.length}</strong> questions correctly.
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

  if (!sc) {
    return null;
  }

  const letters = ['A', 'B', 'C', 'D', 'E'];
  const correctLetter = letters[sc.correctIndex];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', maxWidth: '720px', margin: '0 auto', width: '100%' }}>
      {/* Top Bar */}
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
          Set {setNumber}: Sentence Completion
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span style={{ fontSize: '0.85rem', fontWeight: 600, color: '#2563eb' }}>
            Score: {totalCorrect}
          </span>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
            Q {currentIndex + 1} of {words.length}
          </span>
        </div>
      </div>

      {/* Main Card */}
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
        {/* Sentence Prompt */}
        <div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>
            Fill in the blank with the most appropriate word:
          </div>
          <div style={{
            fontSize: '1.15rem',
            lineHeight: 1.6,
            color: 'var(--text-primary)',
            marginTop: '8px',
            backgroundColor: '#f8fafc',
            padding: '16px 18px',
            borderRadius: 'var(--radius-md)',
            border: '1px solid #e2e8f0'
          }}>
            {sc.sentenceWithBlank}
          </div>
        </div>

        {/* 5 Options A-E */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {sc.options.map((opt, optIdx) => {
            const isSelected = currentState.selectedIndex === optIdx;
            const isCorrect = optIdx === sc.correctIndex;

            let bg = '#ffffff';
            let borderColor = 'var(--border-color)';
            let textColor = 'var(--text-primary)';

            if (currentState.isAnswered) {
              if (isCorrect) {
                bg = 'var(--success-bg)';
                borderColor = 'var(--success)';
                textColor = '#15803d';
              } else if (isSelected) {
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
                  alignItems: 'center',
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
                  backgroundColor: currentState.isAnswered && isCorrect
                    ? '#16a34a'
                    : currentState.isAnswered && isSelected
                    ? '#dc2626'
                    : '#f1f5f9',
                  color: (currentState.isAnswered && (isCorrect || isSelected))
                    ? '#ffffff'
                    : 'var(--text-secondary)',
                  flexShrink: 0
                }}>
                  {letters[optIdx]}
                </div>

                <div style={{ fontSize: '1rem', fontWeight: 600, color: textColor, flex: 1 }}>
                  {opt}
                </div>

                {/* Inline Bangla meaning hint if answered */}
                {currentState.isAnswered && sc.optionMeaningsBn[optIdx] && (
                  <span className="bangla-text" style={{ fontSize: '0.85rem', color: '#64748b' }}>
                    ({sc.optionMeaningsBn[optIdx]})
                  </span>
                )}
              </div>
            );
          })}
        </div>

        {/* 6.3 Post-Answer Explanation Box */}
        {currentState.isAnswered && (
          <div style={{
            backgroundColor: '#f8fafc',
            border: '1px solid #cbd5e1',
            borderRadius: 'var(--radius-md)',
            padding: '16px 18px',
            display: 'flex',
            flexDirection: 'column',
            gap: '12px'
          }}>
            {/* Header: Result */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              {currentState.isCorrect ? (
                <>
                  <Check size={18} color="#16a34a" />
                  <strong style={{ color: '#15803d' }}>Correct! Answer is {correctLetter}.</strong>
                </>
              ) : (
                <>
                  <X size={18} color="#dc2626" />
                  <strong style={{ color: '#b91c1c' }}>Incorrect. Correct Answer is {correctLetter} ({sc.options[sc.correctIndex]}).</strong>
                </>
              )}
            </div>

            {/* 1. Bangla Explanation (ব্যাখ্যা (উত্তর: C):) listing Bangla meanings of all 5 options */}
            <div style={{
              backgroundColor: '#ffffff',
              border: '1px solid #e2e8f0',
              borderRadius: '6px',
              padding: '10px 12px',
              fontSize: '0.9rem',
              lineHeight: 1.6
            }}>
              <span className="bangla-text" style={{ fontWeight: 700, color: '#1e3a8a' }}>
                ব্যাখ্যা (উত্তর: {correctLetter}):{' '}
              </span>
              <span className="bangla-text" style={{ color: '#334155' }}>
                {sc.options.map((opt, i) => `${letters[i]}. ${opt} - ${sc.optionMeaningsBn[i] || 'অর্থ'}`).join('; ')}
              </span>
            </div>

            {/* 2. English Definition */}
            <div style={{ fontSize: '0.95rem', color: '#1e293b' }}>
              <strong>Definition: </strong>
              <span>{sc.explanationEn}</span>
            </div>

            {/* 3. Bangla Sentence Translation */}
            {sc.sentenceTranslationBn && (
              <div className="bangla-text" style={{ fontSize: '0.925rem', color: '#475569', fontStyle: 'italic', borderTop: '1px solid #e2e8f0', paddingTop: '8px' }}>
                <strong>বঙ্গানুবাদ: </strong>
                <span>{sc.sentenceTranslationBn}</span>
              </div>
            )}
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
          <span>{currentIndex === words.length - 1 ? 'Finish Drill' : 'Next'}</span>
          <ArrowRight size={16} />
        </button>
      </div>
    </div>
  );
};
