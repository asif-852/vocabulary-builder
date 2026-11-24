import React, { useEffect } from 'react';
import { BookOpen, Menu } from 'lucide-react';

interface HeaderProps {
  onGoHome?: () => void;
  showMenuButton?: boolean;
  isDrawerOpen?: boolean;
  onOpenDrawer?: () => void;
}

const STUDY_BOOK_FAVICON =
  "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='8' fill='%232563eb'/><g transform='translate(4 4)' fill='none' stroke='%23ffffff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M12 7v14'/><path d='M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z'/></g></svg>";

export const Header: React.FC<HeaderProps> = ({
  onGoHome,
  showMenuButton = false,
  isDrawerOpen = false,
  onOpenDrawer
}) => {
  useEffect(() => {
    const link = document.querySelector<HTMLLinkElement>("link[rel*='icon']");
    if (link && link.href !== STUDY_BOOK_FAVICON) {
      link.href = STUDY_BOOK_FAVICON;
    }
  }, []);

  return (
    <>
      {/* Mobile Sticky App Bar (shown on <= 860px) */}
      <header className="mobile-appbar">
        {showMenuButton && onOpenDrawer && (
          <button
            type="button"
            className="mobile-icon-btn mobile-menu-trigger"
            onClick={onOpenDrawer}
            aria-label="Open word libraries menu"
            aria-controls="home-sidebar"
            aria-expanded={isDrawerOpen}
          >
            <Menu size={22} />
          </button>
        )}

        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            minWidth: 0,
            cursor: onGoHome ? 'pointer' : 'default'
          }}
          onClick={onGoHome}
        >
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
          <div style={{ minWidth: 0 }}>
            <div className="mobile-appbar-title">
              Vocabulary <span className="brand-gradient-text">Pro</span>
            </div>
            <div className="mobile-appbar-subtitle">
              Master high-quality vocabulary
            </div>
          </div>
        </div>
      </header>

      {/* Desktop Fixed Header (shown on > 860px) */}
      <header className="site-header">
        <div className="site-header-inner">
          <div
            style={{ display: 'inline-flex', alignItems: 'center', gap: '10px', cursor: onGoHome ? 'pointer' : 'default' }}
            onClick={onGoHome}
          >
            <div style={{
              backgroundColor: '#2563eb',
              color: '#ffffff',
              borderRadius: '8px',
              padding: '6px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <BookOpen size={20} />
            </div>
            <div>
              <h1 className="site-title">
                Vocabulary <span className="brand-gradient-text">Pro</span>
              </h1>
              <p className="site-subtitle">
                Master high-quality vocabulary
              </p>
            </div>
          </div>
        </div>
      </header>
    </>
  );
};
