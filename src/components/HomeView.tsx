import React, { useEffect, useRef } from 'react';
import { VocabSourceId } from '../data/vocabSchema';
import { SOURCES_INFO, getSourceSetsMeta } from '../data/catalog';
import { useStudyProgress } from '../hooks/useStudyProgress';
import { RotateCcw, CheckCircle2, Lock, X, BookOpen } from 'lucide-react';

interface HomeViewProps {
  activeSource: VocabSourceId;
  onSelectSource: (sourceId: VocabSourceId) => void;
  onSelectSet: (sourceId: VocabSourceId, setNumber: number) => void;
  progress: ReturnType<typeof useStudyProgress>;
  isDrawerOpen: boolean;
  onCloseDrawer: () => void;
}

export const HomeView: React.FC<HomeViewProps> = ({
  activeSource,
  onSelectSource,
  onSelectSet,
  progress,
  isDrawerOpen,
  onCloseDrawer
}) => {
  const sources: VocabSourceId[] = ['gre333', 'wordsmart1', 'wordsmart2'];
  const sidebarRef = useRef<HTMLElement | null>(null);
  const touchStartX = useRef<number | null>(null);

  // Lock page scroll & handle Escape key while mobile drawer is open
  useEffect(() => {
    if (isDrawerOpen) {
      document.body.classList.add('drawer-open');
    } else {
      document.body.classList.remove('drawer-open');
    }

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isDrawerOpen) {
        onCloseDrawer();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      document.body.classList.remove('drawer-open');
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isDrawerOpen, onCloseDrawer]);

  const handleTouchStart = (e: React.TouchEvent) => {
    if (!isDrawerOpen) return;
    touchStartX.current = e.touches[0].clientX;
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    if (touchStartX.current === null || !sidebarRef.current) return;
    const dx = Math.min(0, e.touches[0].clientX - touchStartX.current);
    sidebarRef.current.style.transition = 'none';
    sidebarRef.current.style.transform = `translateX(${dx}px)`;
  };

  const handleTouchEnd = (e: React.TouchEvent) => {
    if (touchStartX.current === null || !sidebarRef.current) return;
    const dx = e.changedTouches[0].clientX - touchStartX.current;
    touchStartX.current = null;
    sidebarRef.current.style.transition = '';
    sidebarRef.current.style.transform = '';
    if (dx < -60) {
      onCloseDrawer();
    }
  };

  const handleReset = (sourceId: VocabSourceId, title: string) => {
    if (window.confirm(`Are you sure you want to reset all Study progress for ${title}? This cannot be undone.`)) {
      progress.resetSourceProgress(sourceId);
      try {
        const prefix = `vocab_builder_study_idx_${sourceId}_`;
        for (let i = localStorage.length - 1; i >= 0; i--) {
          const key = localStorage.key(i);
          if (key && key.startsWith(prefix)) {
            localStorage.removeItem(key);
          }
        }
      } catch {
        // ignore
      }
    }
  };

  const info = SOURCES_INFO[activeSource];
  const sets = getSourceSetsMeta(activeSource);
  const sourceProg = progress.getSourceProgress(activeSource);

  const warmSource = () => {
    import('../data/index').then(m => m.prefetchSourceWords(activeSource)).catch(() => {});
  };

  return (
    <div className="home-layout">
      {/* Left Sidebar slot (fixed on desktop, slide-in drawer on mobile <= 860px) */}
      <div className="home-sidebar-slot">
        <aside
          id="home-sidebar"
          ref={sidebarRef}
          className={`home-sidebar ${isDrawerOpen ? 'open' : ''}`}
          aria-label="Word libraries"
          onTouchStart={handleTouchStart}
          onTouchMove={handleTouchMove}
          onTouchEnd={handleTouchEnd}
        >
        {/* Mobile Drawer Header */}
        <div className="drawer-head">
          <div style={{
            backgroundColor: '#2563eb',
            color: '#ffffff',
            borderRadius: '8px',
            padding: '6px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexShrink: 0
          }}>
            <BookOpen size={18} />
          </div>
          <div className="drawer-head-title">
            Vocabulary <span className="brand-gradient-text">Pro</span>
          </div>
          <button
            type="button"
            className="mobile-icon-btn drawer-close-btn"
            onClick={onCloseDrawer}
            aria-label="Close menu"
          >
            <X size={20} />
          </button>
        </div>

        <div className="sidebar-section-label">Word Libraries</div>

        <nav className="sidebar-source-list" aria-label="Select vocabulary library">
          {sources.map(src => {
            const srcInfo = SOURCES_INFO[src];
            const isSelected = activeSource === src;
            const srcProg = progress.getSourceProgress(src);

            return (
              <button
                key={src}
                type="button"
                className={`sidebar-source-btn ${isSelected ? 'active' : ''}`}
                aria-current={isSelected ? 'page' : undefined}
                onClick={() => {
                  onSelectSource(src);
                  onCloseDrawer();
                }}
              >
                <span className="sidebar-source-name">{srcInfo.shortTitle}</span>
                <span className="sidebar-source-count">
                  {srcProg.studiedCount}/{srcInfo.totalWords}
                </span>
              </button>
            );
          })}
        </nav>

        {/* Local Storage Info Card */}
        <div className="storage-info-card">
          <div className="storage-info-title">
            <Lock size={14} />
            <span>Saved on this device</span>
          </div>
          <p className="storage-info-text">
            Your progress is stored privately in this browser. No account or sign-in needed.
          </p>
          <p className="storage-info-text">
            It won&apos;t sync to your other devices, and clearing your browser data will reset it.
          </p>
        </div>
        </aside>
      </div>

      {/* Mobile Drawer Dimmed Backdrop */}
      <div
        className={`drawer-backdrop ${isDrawerOpen ? 'open' : ''}`}
        onClick={onCloseDrawer}
        aria-hidden="true"
      />

      {/* Active Source Section */}
      <section style={{ display: 'flex', flexDirection: 'column', gap: '18px', minWidth: 0 }}>
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
                {info.description}
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
        <div className="home-set-grid">
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
                  warmSource();
                  e.currentTarget.style.borderColor = 'var(--accent-primary)';
                  e.currentTarget.style.transform = 'translateY(-1px)';
                }}
                onTouchStart={warmSource}
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
    </div>
  );
};
