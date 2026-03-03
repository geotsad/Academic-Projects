// src/pages/ActivityDetails.jsx
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { activityService } from '../api/activityService';
import { useAuth } from '../context/AuthContext';
import { Send } from 'lucide-react';
import ActivityInfoCard from '../components/ActivityInfoCard';
import { getInitials } from '../utils/formatters';
import HeaderPill from '../components/HeaderPill';

// Reusable Card Header Component
const CardHeader = ({ title }) => (
  <h3
    style={{
      borderBottom: '1px solid #eee',
      paddingBottom: '8px',
      margin: '0 0 10px 0',
      fontSize: '16px',
    }}
  >
    {title}
  </h3>
);

const ActivityDetails = () => {
  const { id } = useParams();
  const { userId } = useAuth();
  const navigate = useNavigate();

  const [details, setDetails] = useState(null);
  const [showAllParticipants, setShowAllParticipants] = useState(false);
  const [messageInput, setMessageInput] = useState('');

  useEffect(() => {
    activityService.getActivityDetails(userId, id).then((data) => {
      console.log('Backend Data Received:', data);
      setDetails(data);
    });
  }, [id, userId]);

  if (!details) return <div className="container">Loading...</div>;

  const isCompleted = details.completed === true;

  const participants = Array.isArray(details.participants)
    ? details.participants
    : [];

  const MAX_VISIBLE = 2;
  const visibleParticipants = showAllParticipants
    ? participants
    : participants.slice(0, MAX_VISIBLE);

  // 🔹 ΛΥΣΗ DUPLICATION: Φτιάχνουμε τα δεδομένα σε πίνακα
  const chatMessages = [
    {
      id: 1,
      user: participants[0]?.username || 'Aimilia',
      text: 'Hey everyone! Are we doing a warm-up together?',
    },
    {
      id: 2,
      user: participants[1]?.username || 'Giorgos C.',
      text: "Yes, let's meet 15 min earlier for stretching.",
    },
  ];

  return (
    <div className="container">
      <HeaderPill title={details.activityType || 'Activity'} action="back" />

      <ActivityInfoCard details={details} />

      {/* ===== USERS CARD ===== */}
      <div className="card">
        <CardHeader title="Users" />

        {participants.length > 0 ? (
          <>
            {visibleParticipants.map((u, index) => (
              <div
                key={u.userId || index}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '8px 0',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <div
                    style={{
                      width: 36,
                      height: 36,
                      borderRadius: '50%',
                      background: 'var(--primary-green)',
                      color: 'white',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontWeight: 600,
                    }}
                  >
                    {getInitials(u.username)}
                  </div>

                  <div>
                    <div style={{ fontWeight: 600, fontSize: '14px' }}>
                      {u.username || 'User'}
                    </div>
                    <div style={{ fontSize: '12px', color: '#666' }}>
                      Participant
                    </div>
                  </div>
                </div>

                <button
                  className="btn-secondary"
                  style={{
                    borderRadius: '20px',
                    padding: '4px 14px',
                    fontSize: '12px',
                    color: 'var(--primary-green)',
                    border: '2px solid var(--primary-green)',
                    background: 'white',
                  }}
                >
                  View
                </button>
              </div>
            ))}

            {participants.length > MAX_VISIBLE && (
              <button
                className="pinned-toggle-btn"
                onClick={() => setShowAllParticipants((prev) => !prev)}
                style={{ marginTop: '4px', fontSize: '22px' }}
              >
                {showAllParticipants ? '▲' : '▼'}
              </button>
            )}
          </>
        ) : (
          <p style={{ color: '#999', fontSize: '14px' }}>
            No participant info available.
          </p>
        )}
      </div>

      {/* ===== CHAT CARD ===== */}
      <div className="card" style={{ marginTop: '12px' }}>
        <CardHeader title="Chat" />

        <div style={{ background: '#e5f8d9', borderRadius: '12px', padding: '10px' }}>
          {/* 🔹 ΛΥΣΗ DUPLICATION: Map αντί για copy-paste */}
          {chatMessages.map((msg) => (
            <div key={msg.id} style={{ marginBottom: '10px' }}>
              <div
                style={{ fontSize: '12px', fontWeight: 600, marginBottom: '4px' }}
              >
                {msg.user}
              </div>
              <div
                style={{
                  background: '#5cb85c',
                  color: 'white',
                  padding: '8px 10px',
                  borderRadius: '12px',
                  display: 'inline-block',
                  fontSize: '13px',
                }}
              >
                {msg.text}
              </div>
            </div>
          ))}

          {isCompleted ? (
            <div
              style={{
                marginTop: '12px',
                background: '#ffffff',
                borderRadius: '12px',
                padding: '8px 10px',
                textAlign: 'center',
                fontSize: '12px',
                color: '#777',
              }}
            >
              The activity has been completed!
            </div>
          ) : (
            <div
              style={{
                marginTop: '12px',
                display: 'flex',
                gap: '8px',
                alignItems: 'center',
                background: '#fff',
                padding: '8px',
                borderRadius: '12px',
              }}
            >
              <input
                type="text"
                value={messageInput}
                onChange={(e) => setMessageInput(e.target.value)}
                placeholder="Type a message..."
                style={{ flex: 1, border: 'none', outline: 'none', fontSize: '13px' }}
              />
              <button
                style={{
                  background: 'var(--primary-green)',
                  color: 'white',
                  border: 'none',
                  borderRadius: '50%',
                  width: '32px',
                  height: '32px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  cursor: 'pointer',
                }}
                onClick={() => setMessageInput('')}
              >
                <Send size={16} />
              </button>
            </div>
          )}
        </div>
      </div>

      <button
        className="btn"
        style={{
          width: '100%',
          marginTop: '20px',
          background: 'var(--warning-yellow)',
          color: '#000',
          borderRadius: '999px',
          fontWeight: 600,
          boxShadow: '0 3px 6px rgba(0,0,0,0.15)',
        }}
        onClick={() =>
          navigate(`/review/${id}`, {
            state: { participants: details.participants || [] },
          })
        }
      >
        Review Activity
      </button>
    </div>
  );
};

export default ActivityDetails;