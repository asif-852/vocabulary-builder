import React from 'react';
import { BookOpen } from 'lucide-react';

interface HeaderProps {
  onGoHome?: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onGoHome }) => {
  return (
    <header className="site-header">
      <div 
        style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: onGoHome ? 'pointer' : 'default' }}
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
          <h1 className="site-title">Vocabulary Builder</h1>
          <p className="site-subtitle">
            GRE 333 · Word Smart 1 · Word Smart 2 · Progress saved in this browser
          </p>
        </div>
      </div>
    </header>
  );
};
