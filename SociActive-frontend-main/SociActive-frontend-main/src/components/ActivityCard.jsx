// src/components/ActivityCard.jsx
import React from 'react';
import { Pin } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { formatDate } from '../utils/formatters';

const ActivityCard = ({
  activity,
  type = 'feed',
  onAction,
  onTogglePin,
}) => {
  const navigate = useNavigate();
  const { activityId, details } = activity;

  const isPinned = activity.isPinned ?? activity.pinned ?? false;

  // 🔹 ΛΥΣΗ DUPLICATION: Υπολογισμός ρυθμίσεων αντί για 3 if statements
  const getButtonConfig = () => {
    if (type === 'feed' || type === 'pinned') {
      return { text: 'Join', className: 'btn-primary' };
    }
    if (type === 'my_upcoming') {
      return { text: 'Leave', className: 'btn-leave' };
    }
    if (type === 'my_completed') {
      return { text: 'Save', className: 'btn-save' };
    }
    return null;
  };

  const buttonConfig = getButtonConfig();

  return (
    <div className="card" style={{ position: 'relative' }}>
      {/* ---------- PIN BUTTON ---------- */}
      {onTogglePin && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            onTogglePin(activityId, isPinned);
          }}
          style={{
            position: 'absolute',
            top: 10,
            left: 10,
            border: 'none',
            background: 'transparent',
            cursor: 'pointer',
            padding: 4,
          }}
        >
          <Pin
            size={20}
            strokeWidth={2.2}
            style={{
              transform: 'rotate(45deg)',
              color: isPinned ? 'black' : 'gray',
              fill: isPinned ? 'black' : 'transparent',
              transition: '0.2s ease',
            }}
          />
        </button>
      )}

      {/* ---------- CONTENT ---------- */}
      <div style={{ paddingLeft: onTogglePin ? '35px' : '0px' }}>
        <h3 style={{ marginBottom: '5px' }}>{details.activityType}</h3>

        <div className="text-muted" style={{ fontSize: '0.875rem', lineHeight: '1.6' }}>
          <div>Date: {formatDate(details.date)}</div>
          <div>Time: {details.time}</div>
          <div>Location: {details.location}</div>
        </div>

        <div
          style={{
            marginTop: '15px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}
        >
          <span
            style={{
              textDecoration: 'underline',
              fontSize: '14px',
              cursor: 'pointer'
            }}
            onClick={() => navigate(`/activity/${activityId}`)}
          >
            View details
          </span>

          {/* 🔹 ΛΥΣΗ DUPLICATION: Render ΜΟΝΟ μια φορά */}
          {onAction && buttonConfig && (
            <button
              className={`${buttonConfig.className} action-btn`}
              onClick={(e) => {
                e.stopPropagation();
                onAction(activityId);
              }}
            >
              {buttonConfig.text}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default ActivityCard;