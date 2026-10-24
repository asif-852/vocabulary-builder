import React from 'react';
import { VocabSourceId } from '../data/vocabSchema';
import { SOURCES_INFO, getSetWords } from '../data/index';
import { useStudyProgress } from '../hooks/useStudyProgress';
import { ArrowLeft, BookOpen, CheckCircle, GraduationCap } from 'lucide-react';

interface SetHubViewProps {
  sourceId: VocabSourceId;
  setNumber: number;
  onBackToHome: () => void;
  onStartStudy: () => void;
  onStartPractice: () => void;
  progress: ReturnType<typeof useStudyProgress>;
}

export const SetHubView: React.FC<SetHubViewProps> = ({
  sourceId,
  setNumber,
  onBackToHome,
  onStartStudy,
  onStartPractice,
  progress
}) => {
  const sourceInfo = SOURCES_INFO[sourceId];
  const setWords = getSetWords(sourceId, setNumber);
  const startWordIndex = setWords.length > 0 ? setWords[0].indexInSource : 0;
  const endWordIndex = setWords.length > 0 ? setWords[setWords.length - 1].indexInSource : 0;
  const setProgress = progress.getSetProgress(sourceId, setNumber);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Top back navigation */}
      <div>
        <button
          onClick={onBackToHome}
          className="pill-button"
          style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}
        >
          <ArrowLeft size={16} />
          <span>Back to Set List</span>
        </button>
      </div>

      {/* Set Details Card */}
      <div style={{
        backgroundColor: '#ffffff',
        border: '1px solid var(--border-color)',
        borderRadius: 'var(--radius-lg)',
        padding: '24px 24px',
        boxShadow: 'var(--shadow-sm)',
        display: 'flex',
        flexDirection: 'column',
        gap: '16px'
      }}>
        <div>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            {sourceInfo.title}
          </div>
          <h2 style={{ fontSize: '1.75rem', fontWeight: 700, color: 'var(--text-primary)', marginTop: '4px' }}>
            Set {setNumber}
          </h2>
          <p style={{ fontSize: '0.95rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Words {startWordIndex}–{endWordIndex} · {setWords.length} Words in this set
          </p>
        </div>

        {/* Study Progress Indicator */}
        <div style={{
          backgroundColor: '#f8fafc',
          border: '1px solid #e2e8f0',
          borderRadius: 'var(--radius-md)',
          padding: '12px 16px',
          display: 'flex',
          flexDirection: 'column',
          gap: '8px'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', fontWeight: 500 }}>
              Set Study Status
            </span>
            <span style={{
              fontSize: '0.8rem',
              fontWeight: 600,
              color: setProgress.status === 'completed' ? 'var(--success)' : 'var(--accent-primary)'
            }}>
              {setProgress.studiedCount} / {setProgress.totalCount} words studied ({setProgress.percentage}%)
            </span>
          </div>
          <div className="progress-bar-track">
            <div
              className="progress-bar-fill"
              style={{
                width: `${setProgress.percentage}%`,
                backgroundColor: setProgress.status === 'completed' ? 'var(--success)' : 'var(--accent-primary)'
              }}
            />
          </div>
        </div>

        {/* Two Primary Action Cards */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
          gap: '16px',
          marginTop: '8px'
        }}>
          {/* 1. Study Card */}
          <div
            onClick={onStartStudy}
            style={{
              border: '2px solid #2563eb',
              backgroundColor: '#eff6ff',
              borderRadius: 'var(--radius-md)',
              padding: '20px',
              cursor: 'pointer',
              display: 'flex',
              flexDirection: 'column',
              gap: '10px',
              transition: 'transform 0.15s ease, box-shadow 0.15s ease'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = 'var(--shadow-md)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'none';
              e.currentTarget.style.boxShadow = 'none';
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{
                backgroundColor: '#2563eb',
                color: '#ffffff',
                padding: '6px',
                borderRadius: '6px',
                display: 'flex'
              }}>
                <BookOpen size={20} />
              </div>
              <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#1e3a8a' }}>
                1. Study
              </h3>
            </div>
            <p style={{ fontSize: '0.875rem', color: '#1e40af', lineHeight: 1.5 }}>
              Learn words one by one with pronunciation, concise meaning, synonyms, antonyms, and contextual sentences.
            </p>
            <div style={{
              marginTop: 'auto',
              paddingTop: '8px',
              display: 'flex',
              alignItems: 'center',
              fontWeight: 600,
              fontSize: '0.875rem',
              color: '#2563eb'
            }}>
              Start Studying →
            </div>
          </div>

          {/* 2. Practice Card */}
          <div
            onClick={onStartPractice}
            style={{
              border: '2px solid #0f172a',
              backgroundColor: '#ffffff',
              borderRadius: 'var(--radius-md)',
              padding: '20px',
              cursor: 'pointer',
              display: 'flex',
              flexDirection: 'column',
              gap: '10px',
              transition: 'transform 0.15s ease, box-shadow 0.15s ease'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = 'var(--shadow-md)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'none';
              e.currentTarget.style.boxShadow = 'none';
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{
                backgroundColor: '#0f172a',
                color: '#ffffff',
                padding: '6px',
                borderRadius: '6px',
                display: 'flex'
              }}>
                <GraduationCap size={20} />
              </div>
              <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#0f172a' }}>
                2. Practice
              </h3>
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
              Test your mastery of this set across 5 exam-style practice modes: Meaning, Sentence Completion, and Synonyms/Antonyms.
            </p>
            <div style={{
              marginTop: 'auto',
              paddingTop: '8px',
              display: 'flex',
              alignItems: 'center',
              fontWeight: 600,
              fontSize: '0.875rem',
              color: '#0f172a'
            }}>
              Choose Practice Mode →
            </div>
          </div>
        </div>

        {/* Word preview list within set */}
        <div style={{ marginTop: '16px', borderTop: '1px solid #e2e8f0', paddingTop: '16px' }}>
          <div style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '8px' }}>
            Words in Set {setNumber} ({setWords.length}):
          </div>
          <div style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '6px'
          }}>
            {setWords.map(w => {
              const studied = progress.isWordStudied(w.id);
              return (
                <span
                  key={w.id}
                  style={{
                    fontSize: '0.8rem',
                    padding: '3px 8px',
                    borderRadius: '4px',
                    backgroundColor: studied ? '#f0fdf4' : '#f1f5f9',
                    color: studied ? '#15803d' : 'var(--text-secondary)',
                    border: studied ? '1px solid #bbf7d0' : '1px solid #e2e8f0',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '4px'
                  }}
                >
                  {studied && <CheckCircle size={10} />}
                  {w.word}
                </span>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};
