import React, { useState } from 'react';
import { VocabSourceId } from '../data/vocabSchema';
import { SOURCES_INFO, getSourceSets } from '../data/index';
import { useStudyProgress } from '../hooks/useStudyProgress';
import { RotateCcw, CheckCircle2, BookMarked } from 'lucide-react';

interface HomeViewProps {
  onSelectSet: (sourceId: VocabSourceId, setNumber: number) => void;
  progress: ReturnType<typeof useStudyProgress>;
}

export const HomeView: React.FC<HomeViewProps> = ({ onSelectSet, progress }) => {
  const [activeSource, setActiveSource] = useState<VocabSourceId>('gre333');
  const sources: VocabSourceId[] = ['gre333', 'wordsmart1', 'wordsmart2'];

  const handleReset = (sourceId: VocabSourceId, title: string) => {
    if (window.confirm(`Are you sure you want to reset all Study progress for ${title}? This cannot be undone.`)) {
      progress.resetSourceProgress(sourceId);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Top Source Switcher Pills */}
      <div style={{
        display: 'flex',
        gap: '8px',
        flexWrap: 'wrap',
        borderBottom: '1px solid var(--border-color)',
        paddingBottom: '14px'
      }}>
        {sources.map(src => {
          const info = SOURCES_INFO[src];
          const isSelected = activeSource === src;
          const srcProg = progress.getSourceProgress(src);
          return (
            <button
              key={src}
              className={`pill-button ${isSelected ? 'active' : ''}`}
              onClick={() => setActiveSource(src)}
              style={{
                fontSize: '0.9rem',
                padding: '8px 16px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}
            >
              <span>{info.shortTitle}</span>
              <span style={{
                fontSize: '0.75rem',
                opacity: 0.8,
                backgroundColor: isSelected ? 'rgba(255, 255, 255, 0.2)' : '#e2e8f0',
                padding: '1px 6px',
                borderRadius: '999px',
                color: isSelected ? '#ffffff' : 'var(--text-secondary)'
              }}>
                {srcProg.studiedCount}/{info.totalWords}
              </span>
            </button>
          );
        })}
      </div>

      {/* Active Source Section */}
      {(() => {
        const info = SOURCES_INFO[activeSource];
        const sets = getSourceSets(activeSource);
        const sourceProg = progress.getSourceProgress(activeSource);

        return (
          <section style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
            {/* Source Header & Progress Card */}
            <div style={{
              backgroundColor: '#ffffff',
              border: '1px solid var(--border-color)',
              borderRadius: 'var(--radius-md)',
              padding: '18px 20px',
              display: 'flex',
              flexDirection: 'column',
              gap: '12px',
              boxShadow: 'var(--shadow-sm)'
            }}>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'flex-start',
                flexWrap: 'wrap',
                gap: '12px'
              }}>
                <div>
                  <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                    {info.title}
                  </h2>
                  <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                    {info.totalWords} words · {info.totalSets} sets ({info.wordsPerSet} words/set) · {info.description}
                  </p>
                </div>

                <button
                  onClick={() => handleReset(activeSource, info.shortTitle)}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '4px',
                    fontSize: '0.8rem',
                    color: 'var(--text-muted)',
                    padding: '4px 8px',
                    borderRadius: 'var(--radius-sm)',
                    border: '1px solid #e2e8f0',
                    backgroundColor: '#f8fafc',
                    cursor: 'pointer'
                  }}
                  title="Reset study progress for this source"
                >
                  <RotateCcw size={12} />
                  <span>Reset progress</span>
                </button>
              </div>

              {/* Progress Summary */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  fontSize: '0.85rem',
                  fontWeight: 500
                }}>
                  <span style={{ color: 'var(--text-secondary)' }}>
                    Study Progress: <strong>{sourceProg.studiedCount}</strong> / {sourceProg.totalCount} words
                  </span>
                  <span style={{ color: 'var(--accent-primary)', fontWeight: 600 }}>
                    {sourceProg.percentage}%
                  </span>
                </div>
                <div className="progress-bar-track">
                  <div
                    className="progress-bar-fill"
                    style={{ width: `${sourceProg.percentage}%` }}
                  />
                </div>
              </div>
            </div>

            {/* Set Grid */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))',
              gap: '12px'
            }}>
              {sets.map(s => {
                const setProg = progress.getSetProgress(activeSource, s.setNumber);

                return (
                  <div
                    key={s.setNumber}
                    onClick={() => onSelectSet(activeSource, s.setNumber)}
                    style={{
                      backgroundColor: '#ffffff',
                      border: setProg.status === 'completed'
                        ? '1px solid #86efac'
                        : '1px solid var(--border-color)',
                      borderRadius: 'var(--radius-md)',
                      padding: '14px 12px',
                      cursor: 'pointer',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '8px',
                      transition: 'all 0.15s ease',
                      boxShadow: 'var(--shadow-sm)'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.borderColor = 'var(--accent-primary)';
                      e.currentTarget.style.transform = 'translateY(-1px)';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.borderColor = setProg.status === 'completed' ? '#86efac' : 'var(--border-color)';
                      e.currentTarget.style.transform = 'none';
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontWeight: 700, fontSize: '0.95rem', color: 'var(--text-primary)' }}>
                        Set {s.setNumber}
                      </span>
                      {setProg.status === 'completed' && (
                        <CheckCircle2 size={16} color="var(--success)" />
                      )}
                    </div>

                    <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                      Words {s.startWordIndex}–{s.endWordIndex}
                    </div>

                    <div>
                      {setProg.status === 'completed' && (
                        <span className="status-badge completed">
                          Completed ({setProg.studiedCount}/{setProg.totalCount})
                        </span>
                      )}
                      {setProg.status === 'in_progress' && (
                        <span className="status-badge in-progress">
                          In progress ({setProg.studiedCount}/{setProg.totalCount})
                        </span>
                      )}
                      {setProg.status === 'not_started' && (
                        <span className="status-badge not-started">
                          Not started ({s.wordCount})
                        </span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </section>
        );
      })()}
    </div>
  );
};
