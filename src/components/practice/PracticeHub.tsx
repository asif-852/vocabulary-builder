import React from 'react';
import { VocabSourceId } from '../../data/vocabSchema';
import { SOURCES_INFO, getSetWords } from '../../data/index';
import { ArrowLeft, BookOpen, FileText, CheckSquare, Sparkles, Split } from 'lucide-react';

export type PracticeModeId = 'meaning' | 'sentence' | 'multi_synonym' | 'single_synonym' | 'single_antonym';

interface PracticeHubProps {
  sourceId: VocabSourceId;
  setNumber: number;
  onBackToSet: () => void;
  onSelectMode: (mode: PracticeModeId) => void;
}

export const PracticeHub: React.FC<PracticeHubProps> = ({
  sourceId,
  setNumber,
  onBackToSet,
  onSelectMode
}) => {
  const sourceInfo = SOURCES_INFO[sourceId];
  const setWords = getSetWords(sourceId, setNumber);
  const startIdx = setWords.length > 0 ? setWords[0].indexInSource : 0;
  const endIdx = setWords.length > 0 ? setWords[setWords.length - 1].indexInSource : 0;

  const modes: {
    id: PracticeModeId;
    title: string;
    description: string;
    icon: React.ReactNode;
    badge: string;
  }[] = [
    {
      id: 'meaning',
      title: '1. Find the Meaning',
      description: 'Choose the correct dictionary definition among 4 plausible options.',
      icon: <BookOpen size={20} color="#2563eb" />,
      badge: '4 Options'
    },
    {
      id: 'sentence',
      title: '2. Sentence Completion',
      description: 'Exam-style sentences with blanks and 5 plausible options. Includes full Bangla option breakdowns.',
      icon: <FileText size={20} color="#059669" />,
      badge: '5 Options'
    },
    {
      id: 'multi_synonym',
      title: '3. Synonyms Finding (Multiple Options)',
      description: 'Select all correct synonyms among the checkboxes. Comprehensive test of lexical range.',
      icon: <CheckSquare size={20} color="#d97706" />,
      badge: '6-7 Checkboxes'
    },
    {
      id: 'single_synonym',
      title: '4. Synonym Finding (One Option)',
      description: 'Competitive exam style (Bank, BCS, GRE): pick the closest synonym among 4 options with trap distractors.',
      icon: <Sparkles size={20} color="#7c3aed" />,
      badge: '4 Options (Exam Style)'
    },
    {
      id: 'single_antonym',
      title: '5. Antonym Finding (One Option)',
      description: 'Pick the word most nearly opposite in meaning among 4 options, including synonym trap distractors.',
      icon: <Split size={20} color="#dc2626" />,
      badge: '4 Options (Opposite Meaning)'
    }
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div>
        <button
          onClick={onBackToSet}
          className="pill-button"
          style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}
        >
          <ArrowLeft size={16} />
          <span>Back to Set</span>
        </button>
      </div>

      <div style={{
        backgroundColor: '#ffffff',
        border: '1px solid var(--border-color)',
        borderRadius: 'var(--radius-lg)',
        padding: '24px',
        boxShadow: 'var(--shadow-sm)',
        display: 'flex',
        flexDirection: 'column',
        gap: '20px'
      }}>
        <div>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase' }}>
            {sourceInfo.title}
          </div>
          <h2 style={{ fontSize: '1.6rem', fontWeight: 700, color: 'var(--text-primary)', marginTop: '4px' }}>
            Set {setNumber} — Practice Modes
          </h2>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Words {startIdx}–{endIdx} ({setWords.length} questions per mode) · Test your mastery with competitive exam drills
          </p>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
          gap: '14px'
        }}>
          {modes.map(m => (
            <div
              key={m.id}
              onClick={() => onSelectMode(m.id)}
              style={{
                backgroundColor: '#ffffff',
                border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-md)',
                padding: '18px 16px',
                cursor: 'pointer',
                display: 'flex',
                flexDirection: 'column',
                gap: '10px',
                transition: 'all 0.15s ease',
                boxShadow: 'var(--shadow-sm)'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = 'var(--accent-primary)';
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow = 'var(--shadow-md)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = 'var(--border-color)';
                e.currentTarget.style.transform = 'none';
                e.currentTarget.style.boxShadow = 'var(--shadow-sm)';
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  {m.icon}
                  <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                    {m.title}
                  </h3>
                </div>
              </div>

              <p style={{ fontSize: '0.825rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                {m.description}
              </p>

              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 'auto', paddingTop: '6px' }}>
                <span style={{
                  fontSize: '0.725rem',
                  fontWeight: 600,
                  backgroundColor: '#f1f5f9',
                  color: '#475569',
                  padding: '2px 8px',
                  borderRadius: '4px'
                }}>
                  {m.badge}
                </span>
                <span style={{ fontSize: '0.825rem', fontWeight: 600, color: 'var(--accent-primary)' }}>
                  Start →
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
