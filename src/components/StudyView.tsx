import React, { useState, useEffect, useCallback } from 'react';
import { VocabWord, VocabSourceId } from '../data/vocabSchema';
import { getSetWords } from '../data/index';
import { useStudyProgress } from '../hooks/useStudyProgress';
import { ArrowLeft, ArrowRight, Check, Eye, EyeOff } from 'lucide-react';

interface StudyViewProps {
  sourceId: VocabSourceId;
  setNumber: number;
  onBackToSet: () => void;
  progress: ReturnType<typeof useStudyProgress>;
}

export const StudyView: React.FC<StudyViewProps> = ({
  sourceId,
  setNumber,
  onBackToSet,
  progress
}) => {
  const words = getSetWords(sourceId, setNumber);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [explanationOn, setExplanationOn] = useState<boolean>(() => {
    try {
      const saved = localStorage.getItem('vocab_builder_explanation_pref');
      return saved !== null ? JSON.parse(saved) : true;
    } catch {
      return true;
    }
  });

  const currentWord: VocabWord | undefined = words[currentIndex];

  const toggleExplanation = useCallback(() => {
    setExplanationOn(prev => {
      const next = !prev;
      try {
        localStorage.setItem('vocab_builder_explanation_pref', JSON.stringify(next));
      } catch (e) {
        console.error(e);
      }
      return next;
    });
  }, []);

  const handleNext = useCallback(() => {
    if (currentWord) {
      progress.markWordStudied(currentWord.id, true);
    }
    if (currentIndex < words.length - 1) {
      setCurrentIndex(prev => prev + 1);
    } else {
      // Finished set
      onBackToSet();
    }
  }, [currentIndex, words.length, currentWord, progress, onBackToSet]);

  const handlePrev = useCallback(() => {
    if (currentIndex > 0) {
      setCurrentIndex(prev => prev - 1);
    }
  }, [currentIndex]);

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) {
        return;
      }
      if (e.key === ' ' || e.key === 'e' || e.key === 'E') {
        e.preventDefault();
        toggleExplanation();
      } else if (e.key === 'ArrowRight') {
        e.preventDefault();
        handleNext();
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        handlePrev();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [toggleExplanation, handleNext, handlePrev]);

  if (!currentWord) {
    return (
      <div style={{ padding: '24px', textAlign: 'center' }}>
        <p>No words found for this set.</p>
        <button onClick={onBackToSet} className="pill-button" style={{ marginTop: '12px' }}>
          Back to Set
        </button>
      </div>
    );
  }

  const isStudied = progress.isWordStudied(currentWord.id);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', maxWidth: '760px', margin: '0 auto', width: '100%' }}>
      {/* 5.1 Top Control Bar */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '12px'
      }}>
        {/* Left: Back to Set */}
        <button
          onClick={onBackToSet}
          className="pill-button"
          style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}
        >
          <ArrowLeft size={16} />
          <span>Back to Set</span>
        </button>

        {/* Center: Set X · Word Y of Z */}
        <div style={{
          fontSize: '0.9rem',
          fontWeight: 600,
          color: 'var(--text-secondary)'
        }}>
          Set {setNumber} · Word {currentIndex + 1} of {words.length}
        </div>

        {/* Right: Explanation Toggle Switch */}
        <button
          onClick={toggleExplanation}
          className={`pill-button ${explanationOn ? 'active' : ''}`}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            backgroundColor: explanationOn ? '#0f172a' : '#ffffff',
            color: explanationOn ? '#ffffff' : '#0f172a',
            borderColor: '#0f172a'
          }}
          title="Toggle Explanation (Shortcut: Space or E)"
        >
          {explanationOn ? <Eye size={15} /> : <EyeOff size={15} />}
          <span>{explanationOn ? '• Explanation on' : '• Explanation off'}</span>
        </button>
      </div>

      {/* 5.2 The Study Word Card */}
      {/* ZERO-JUMP LAYOUT STABILITY CONTAINER */}
      <div
        style={{
          backgroundColor: '#ffffff',
          border: '1px solid var(--border-color)',
          borderLeft: '4px solid #2563eb',
          borderRadius: 'var(--radius-md)',
          boxShadow: 'var(--shadow-sm)',
          padding: '28px 24px',
          minHeight: '380px',
          display: 'flex',
          flexDirection: 'column',
          position: 'relative'
        }}
      >
        {/* WORD HEADER ROW: English word is anchored at top-left.
            Bangla meaning appears inline beside it when explanation is on.
            Word never jumps! */}
        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            alignItems: 'baseline',
            gap: '8px',
            lineHeight: 1.2
          }}
        >
          <h2
            style={{
              fontSize: '2rem',
              fontWeight: 700,
              color: 'var(--text-primary)',
              letterSpacing: '-0.02em',
              margin: 0,
              padding: 0
            }}
          >
            {currentWord.word}
          </h2>

          {/* Inline Bangla meaning: only visible when explanation is ON */}
          {explanationOn && currentWord.meaningBn && (
            <span
              className="bangla-text"
              style={{
                fontSize: '1.25rem',
                color: '#334155',
                fontWeight: 500
              }}
            >
              ({currentWord.meaningBn})
            </span>
          )}
        </div>

        {/* EXPLANATION BODY:
            Hidden or rendered when Explanation is On.
            Because it is placed strictly BELOW the Word Header Row,
            toggling it on/off does not alter the (X, Y) top-left coordinates of currentWord.word! */}
        {explanationOn ? (
          <div style={{ marginTop: '8px', display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {/* Metadata Sub-header (Small & Muted) */}
            <div style={{
              fontSize: '0.85rem',
              color: 'var(--text-muted)',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              fontWeight: 400
            }}>
              <span>{currentWord.partOfSpeech}</span>
              <span>|</span>
              <span style={{ fontFamily: 'monospace', fontSize: '0.9rem' }}>{currentWord.pronunciationEn}</span>
              {currentWord.pronunciationBn && (
                <>
                  <span>|</span>
                  <span className="bangla-text">{currentWord.pronunciationBn}</span>
                </>
              )}
            </div>

            {/* Concise Meaning */}
            <div style={{ fontSize: '1.05rem', lineHeight: 1.5, color: 'var(--text-primary)' }}>
              <strong style={{ color: '#0f172a' }}>Meaning: </strong>
              <span>{currentWord.meaningEn}</span>
            </div>

            {/* Synonyms & Antonyms Block */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '0.95rem' }}>
              <div>
                <strong style={{ color: '#166534' }}>Synonyms: </strong>
                <span style={{ color: '#1f2937' }}>
                  {currentWord.synonyms.join(', ')}
                </span>
              </div>
              <div>
                <strong style={{ color: '#991b1b' }}>Antonyms: </strong>
                <span style={{ color: '#1f2937' }}>
                  {currentWord.antonyms.join(', ')}
                </span>
              </div>
            </div>

            {/* Contextual Demo Sentences (Bulleted List) */}
            <div style={{
              marginTop: '12px',
              paddingTop: '14px',
              borderTop: '1px solid #f1f5f9',
              display: 'flex',
              flexDirection: 'column',
              gap: '10px'
            }}>
              {currentWord.examples.map((ex, exIdx) => (
                <div key={exIdx} style={{ fontSize: '0.95rem', lineHeight: 1.55 }}>
                  <span style={{ color: '#334155', marginRight: '6px' }}>•</span>
                  <span style={{ color: '#0f172a' }}>{ex.en} </span>
                  {ex.bn && (
                    <span className="bangla-text" style={{ color: '#475569' }}>
                      ({ex.bn})
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>
        ) : (
          /* When explanation is OFF, show an empty placeholder or subtle prompt that keeps layout clean */
          <div style={{
            marginTop: '24px',
            color: 'var(--text-light)',
            fontSize: '0.85rem',
            userSelect: 'none'
          }}>
            <em>(Explanation is off · Press Space or E or toggle button to reveal meaning)</em>
          </div>
        )}
      </div>

      {/* 5.3 Bottom Navigation & Study Progress Tracking */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '12px',
        paddingTop: '6px'
      }}>
        {/* Previous Button */}
        <button
          onClick={handlePrev}
          disabled={currentIndex === 0}
          className="pill-button"
          style={{
            opacity: currentIndex === 0 ? 0.4 : 1,
            cursor: currentIndex === 0 ? 'not-allowed' : 'pointer'
          }}
        >
          <ArrowLeft size={16} />
          <span>Previous</span>
        </button>

        {/* Studied Toggle Pill */}
        <button
          onClick={() => progress.markWordStudied(currentWord.id, !isStudied)}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            padding: '6px 12px',
            borderRadius: 'var(--radius-full)',
            fontSize: '0.825rem',
            fontWeight: 500,
            border: isStudied ? '1px solid #86efac' : '1px solid var(--border-color)',
            backgroundColor: isStudied ? '#f0fdf4' : '#ffffff',
            color: isStudied ? '#15803d' : 'var(--text-secondary)',
            cursor: 'pointer'
          }}
        >
          <div style={{
            width: '14px',
            height: '14px',
            borderRadius: '3px',
            border: isStudied ? '1px solid #16a34a' : '1px solid #94a3b8',
            backgroundColor: isStudied ? '#16a34a' : '#ffffff',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#ffffff'
          }}>
            {isStudied && <Check size={10} strokeWidth={3} />}
          </div>
          <span>{isStudied ? 'Marked as studied' : 'Mark as studied'}</span>
        </button>

        {/* Next / Finish Button */}
        <button
          onClick={handleNext}
          className="pill-button active"
          style={{
            backgroundColor: '#2563eb',
            borderColor: '#2563eb',
            color: '#ffffff',
            padding: '8px 18px',
            fontWeight: 600
          }}
        >
          <span>{currentIndex === words.length - 1 ? 'Finish Set ✓' : 'Next →'}</span>
        </button>
      </div>
    </div>
  );
};
