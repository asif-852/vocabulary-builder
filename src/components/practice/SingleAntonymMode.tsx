import React, { useState, useMemo } from 'react';
import { VocabWord, VocabSourceId } from '../../data/vocabSchema';
import { getSetWords, getSingleAntonymQuestion } from '../../data/index';
import { ArrowLeft, ArrowRight, RotateCcw, Check, X } from 'lucide-react';

interface SingleAntonymModeProps {
  sourceId: VocabSourceId;
  setNumber: number;
  onBackToHub: () => void;
}

interface QuestionState {
  selectedIndex: number | null;
  isAnswered: boolean;
  isCorrect: boolean;
}

export const SingleAntonymMode: React.FC<SingleAntonymModeProps> = ({
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
      qData: getSingleAntonymQuestion(w)
    }));
  }, [words]);

  const currentQ = questions[currentIndex];
  const currentState = answers[currentIndex] || { selectedIndex: null, isAnswered: false, isCorrect: false };

  const totalAnswered = Object.values(answers).filter(a => a.isAnswered).length;
  const totalCorrect = Object.values(answers).filter(a => a.isCorrect).length;
  const isComplete = currentIndex >= questions.length;

  const handleSelectOption = (optIndex: number) => {
    if (currentState.isAnswered) return;

    const isCorrect = currentQ.qData.options[optIndex].isCorrect;
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
            Set {setNumber} — Antonym Finding Complete!
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
          Set {setNumber}: Antonym Finding (Single)
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
        {/* Exam Stem Prompt */}
        <div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>
            Competitive Exam Question:
          </div>
          <div style={{ fontSize: '1.15rem', color: 'var(--text-primary)', marginTop: '4px' }}>
            Choose the word that is most nearly <strong style={{ color: '#dc2626' }}>opposite in meaning</strong> to{' '}
            <strong style={{ color: '#0f172a' }}>"{currentQ.targetWord.word.toUpperCase()}"</strong>:
          </div>
        </div>

        {/* 4 Options */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '10px' }}>
          {currentQ.qData.options.map((opt, optIdx) => {
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
                  padding: '12px 14px',
                  cursor: currentState.isAnswered ? 'default' : 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  transition: 'background-color 0.15s, border-color 0.15s'
                }}
              >
                <div style={{
                  width: '24px',
                  height: '24px',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '0.8rem',
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

                <div style={{ fontSize: '0.95rem', fontWeight: 600, color: textColor }}>
                  {opt.word}
                </div>
              </div>
            );
          })}
        </div>

        {/* Post-Answer Explanation Table */}
        {currentState.isAnswered && (
          <div style={{
            backgroundColor: '#f8fafc',
            border: '1px solid #cbd5e1',
            borderRadius: 'var(--radius-md)',
            padding: '16px',
            display: 'flex',
            flexDirection: 'column',
            gap: '10px'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              {currentState.isCorrect ? (
                <>
                  <Check size={18} color="#16a34a" />
                  <strong style={{ color: '#15803d' }}>
                    Correct! The antonym of "{currentQ.targetWord.word}" is "{currentQ.qData.correctAntonym}".
                  </strong>
                </>
              ) : (
                <>
                  <X size={18} color="#dc2626" />
                  <strong style={{ color: '#b91c1c' }}>
                    Incorrect. The correct antonym is "{currentQ.qData.correctAntonym}".
                  </strong>
                </>
              )}
            </div>

            {/* Structured Table */}
            <div style={{ overflowX: 'auto' }}>
              <table style={{
                width: '100%',
                borderCollapse: 'collapse',
                fontSize: '0.875rem',
                backgroundColor: '#ffffff',
                border: '1px solid #e2e8f0',
                borderRadius: '6px'
              }}>
                <thead>
                  <tr style={{ backgroundColor: '#f1f5f9', borderBottom: '1px solid #cbd5e1', textAlign: 'left' }}>
                    <th style={{ padding: '8px 12px' }}>Word (মূল শব্দ)</th>
                    <th style={{ padding: '8px 12px' }}>Meaning (অর্থ)</th>
                    <th style={{ padding: '8px 12px' }}>Antonyms (বিপরীত)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style={{ padding: '8px 12px', fontWeight: 700, color: '#1e3a8a' }}>
                      {currentQ.targetWord.word}
                    </td>
                    <td className="bangla-text" style={{ padding: '8px 12px', color: '#334155' }}>
                      {currentQ.targetWord.meaningBn}
                    </td>
                    <td style={{ padding: '8px 12px', color: '#dc2626' }}>
                      {currentQ.targetWord.antonyms.join(', ')}
                    </td>
                  </tr>
                </tbody>
              </table>
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
