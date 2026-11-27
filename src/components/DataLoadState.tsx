import React from 'react';
import { ArrowLeft, RotateCcw } from 'lucide-react';

interface DataLoadStateProps {
  loading: boolean;
  error: string | null;
  onRetry: () => void;
  onBack: () => void;
  backLabel: string;
}

export const DataLoadState: React.FC<DataLoadStateProps> = ({
  loading,
  error,
  onRetry,
  onBack,
  backLabel
}) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', maxWidth: '720px', margin: '0 auto', width: '100%' }}>
      <div>
        <button
          type="button"
          onClick={onBack}
          className="pill-button"
          style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}
        >
          <ArrowLeft size={16} />
          <span>{backLabel}</span>
        </button>
      </div>

      <div
        style={{
          backgroundColor: '#ffffff',
          border: '1px solid var(--border-color)',
          borderRadius: 'var(--radius-lg)',
          padding: '32px 24px',
          textAlign: 'center',
          boxShadow: 'var(--shadow-sm)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '12px'
        }}
      >
        {loading ? (
          <p style={{ fontSize: '0.95rem', color: 'var(--text-secondary)', fontWeight: 500 }}>
            Loading vocabulary set...
          </p>
        ) : (
          <>
            <p style={{ fontSize: '0.95rem', color: '#b91c1c', fontWeight: 500 }}>
              {error || 'Unable to load vocabulary data.'}
            </p>
            <button
              type="button"
              onClick={onRetry}
              className="pill-button"
              style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}
            >
              <RotateCcw size={15} />
              <span>Try again</span>
            </button>
          </>
        )}
      </div>
    </div>
  );
};
