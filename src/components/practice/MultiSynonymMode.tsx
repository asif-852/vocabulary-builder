import React, { useState, useMemo } from 'react';
import { VocabWord, VocabSourceId } from '../../data/vocabSchema';
import { getSetWords, getMultiSynonymOptions } from '../../data/index';
import { ArrowLeft, ArrowRight, RotateCcw, Check, X, AlertCircle } from 'lucide-react';

interface MultiSynonymModeProps {
  sourceId: VocabSourceId;
  setNumber: number;
  onBackToHub: () => void;
}

interface QuestionState {
  selectedIds: string[];
  isSubmitted: boolean;
  isPerfect: boolean;
}

export const MultiSynonymMode: React.FC<MultiSynonymModeProps> = ({
  sourceId,
  setNumber,
  onBackToHub
}) => {
  const words = getSetWords(sourceId, setNumber);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, QuestionState>>({});

  const questions = useMemo(() => {
    return words.map(w => ({
      targetWord: w,
      options: getMultiSynonymOptions(w)
    }));
  }, [words]);

  const currentQ = questions[currentIndex];
  const currentState = answers[currentIndex] || { selectedIds: [], isSubmitted: false, isPerfect: false };

  const totalAnswered = Object.values(answers).filter(a => a.isSubmitted).length;
  const totalCorrect = Object.values(answers).filter(a => a.isPerfect).length;
  const isComplete = currentIndex >= questions.length;

  const handleToggleOption = (optId: string) => {
    if (currentState.isSubmitted) return;

    setAnswers(prev => {
      const prevSelected = prev[currentIndex]?.selectedIds || [];
      const nextSelected = prevSelected.includes(optId)
        ? prevSelected.filter(id => id !== optId)
        : [...prevSelected, optId];

      return {
        ...prev,
        [currentIndex]: {
          selectedIds: nextSelected,
          isSubmitted: false,
          isPerfect: false
        }
      };
    });
  };

  const handleCheckAnswer = () => {
    if (currentState.isSubmitted) return;

    const selectedSet = new Set(currentState.selectedIds);
    const trueSynonymIds = currentQ.options.filter(o => o.isSynonym).map(o => o.id);
    const distractorIds = currentQ.options.filter(o => !o.isSynonym).map(o => o.id);

    // 100% correct if selected all true synonyms and 0 distractors
    const selectedAllTrue = trueSynonymIds.every(id => selectedSet.has(id));
    const selectedZeroDistractors = distractorIds.every(id => !selectedSet.has(id));
    const isPerfect = selectedAllTrue && selectedZeroDistractors;

    setAnswers(prev => ({
      ...prev,
      [currentIndex]: {
        selectedIds: currentState.selectedIds,
        isSubmitted: true,
        isPerfect
      }
    }));
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(prev => prev + 1);
    } else {
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
            Set {setNumber} — Synonyms Finding Complete!
          </h2>

          <p style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>
            You got <strong>{totalCorrect}</strong> out of <strong>{questions.length}</strong> fully correct.
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
          Set {setNumber}: Synonyms Finding (Multiple)
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
        {/* Header & Prompt */}
        <div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>
            Select all correct synonyms for the word below:
          </div>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: '10px', marginTop: '4px', flexWrap: 'wrap' }}>
            <h2 style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '0.02em' }}>
              {currentQ.targetWord.word.toUpperCase()}
            </h2>
            {currentState.isSubmitted && (
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

        {/* 6 to 7 Checkbox Options */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {currentQ.options.map(opt => {
            const isChecked = currentState.selectedIds.includes(opt.id);

            let bg = isChecked ? '#eff6ff' : '#ffffff';
            let borderColor = isChecked ? '#3b82f6' : 'var(--border-color)';
            let statusText = '';
            let statusColor = '';

            if (currentState.isSubmitted) {
              if (isChecked && opt.isSynonym) {
                // Correctly checked
                bg = 'var(--success-bg)';
                borderColor = 'var(--success)';
                statusText = '✓ Correct Synonym';
                statusColor = '#15803d';
              } else if (!isChecked && opt.isSynonym) {
                // Missed synonym
                bg = '#fffbeb';
                borderColor = '#f59e0b';
                statusText = 'Missed Synonym';
                statusColor = '#b45309';
              } else if (isChecked && !opt.isSynonym) {
                // Wrongly checked distractor
                bg = 'var(--danger-bg)';
                borderColor = 'var(--danger)';
                statusText = '✗ Not a synonym';
                statusColor = '#b91c1c';
              } else {
                // Correctly avoided distractor
                bg = '#ffffff';
                borderColor = '#e2e8f0';
              }
            }

            return (
              <div
                key={opt.id}
                className="multi-syn-option"
                onClick={() => handleToggleOption(opt.id)}
                style={{
                  backgroundColor: bg,
                  border: `1.5px solid ${borderColor}`,
                  borderRadius: 'var(--radius-md)',
                  padding: '10px 14px',
                  cursor: currentState.isSubmitted ? 'default' : 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  gap: '12px',
                  transition: 'background-color 0.15s, border-color 0.15s'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <div style={{
                    width: '18px',
                    height: '18px',
                    borderRadius: '4px',
                    border: isChecked ? '2px solid #2563eb' : '2px solid #94a3b8',
                    backgroundColor: isChecked ? '#2563eb' : '#ffffff',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: '#ffffff'
                  }}>
                    {isChecked && <Check size={12} strokeWidth={3} />}
                  </div>

                  <span style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-primary)' }}>
                    {opt.word}
                  </span>

                  {currentState.isSubmitted && opt.meaningBn && (
                    <span className="bangla-text" style={{ fontSize: '0.85rem', color: '#64748b' }}>
                      ({opt.meaningBn})
                    </span>
                  )}
                </div>

                {statusText && (
                  <span style={{ fontSize: '0.8rem', fontWeight: 600, color: statusColor }}>
                    {statusText}
                  </span>
                )}
              </div>
            );
          })}
        </div>

        {/* Check Answer Button */}
        {!currentState.isSubmitted ? (
          <button
            onClick={handleCheckAnswer}
            disabled={currentState.selectedIds.length === 0}
            className="check-answer-btn pill-button active"
            style={{
              backgroundColor: currentState.selectedIds.length === 0 ? '#94a3b8' : '#2563eb',
              borderColor: currentState.selectedIds.length === 0 ? '#94a3b8' : '#2563eb',
              color: '#ffffff',
              padding: '10px 20px',
              fontWeight: 600,
              fontSize: '0.95rem',
              alignSelf: 'flex-start',
              cursor: currentState.selectedIds.length === 0 ? 'not-allowed' : 'pointer'
            }}
          >
            Check Answer
          </button>
        ) : (
          <div style={{
            backgroundColor: currentState.isPerfect ? '#f0fdf4' : '#fef2f2',
            border: `1px solid ${currentState.isPerfect ? '#bbf7d0' : '#fecaca'}`,
            borderRadius: 'var(--radius-md)',
            padding: '14px 16px',
            display: 'flex',
            flexDirection: 'column',
            gap: '6px'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              {currentState.isPerfect ? (
                <>
                  <Check size={18} color="#16a34a" />
                  <strong style={{ color: '#15803d' }}>Perfect! (+1 Score)</strong>
                </>
              ) : (
                <>
                  <AlertCircle size={18} color="#dc2626" />
                  <strong style={{ color: '#b91c1c' }}>Not quite complete.</strong>
                </>
              )}
            </div>

            <div style={{ fontSize: '0.9rem', color: '#1e293b' }}>
              Target Word: <strong>{currentQ.targetWord.word}</strong> ({currentQ.targetWord.meaningEn})
            </div>
            <div className="bangla-text" style={{ fontSize: '0.9rem', color: '#334155' }}>
              বাংলা অর্থ: <strong>{currentQ.targetWord.meaningBn}</strong> | সকল সমার্থক শব্দ:{' '}
              {currentQ.targetWord.synonyms.join(', ')}
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
