import React from 'react';
import { ArrowLeft, X } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const HeaderPill = ({ title, action = 'back' }) => {
  const navigate = useNavigate();

  return (
    <div
      style={{
        margin: '0 0 20px 0',
        marginTop: '4px',
        background: 'var(--primary-green)',
        color: 'white',
        borderRadius: '999px',
        padding: '10px 16px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
      }}
    >
      {/* Αν το action είναι 'back', δείξε βελάκι αριστερά */}
      {action === 'back' && (
        <ArrowLeft
          style={{ cursor: 'pointer', position: 'absolute', left: 18 }}
          onClick={() => navigate(-1)}
        />
      )}

      <h2 style={{ margin: 0, fontSize: '18px', fontWeight: 600 }}>
        {title}
      </h2>

      {/* Αν το action είναι 'close', δείξε X δεξιά (για το Review) */}
      {action === 'close' && (
        <button
          onClick={() => navigate(-1)}
          style={{
            position: 'absolute',
            right: 12,
            width: 26,
            height: 26,
            borderRadius: '50%',
            border: '2px solid white',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: 'transparent',
            color: 'white',
            cursor: 'pointer',
          }}
        >
          <X size={16} />
        </button>
      )}
    </div>
  );
};

export default HeaderPill;