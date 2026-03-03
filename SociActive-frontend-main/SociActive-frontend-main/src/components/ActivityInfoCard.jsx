// src/components/ActivityInfoCard.jsx
import React from 'react';
import {
  Calendar,
  Clock,
  MapPin,
  BarChart,
  User,
  Package,
} from 'lucide-react';
import { formatDate, formatTime } from '../utils/formatters';

// Reusable Info Item Component
const InfoItem = ({ icon: Icon, text, fullWidth = false }) => (
  <div style={{ ...itemStyle, ...(fullWidth && { gridColumn: '1 / -1' }) }}>
    <Icon size={16} /> {text}
  </div>
);

const ActivityInfoCard = ({ details }) => {
  if (!details) return null;

  // Normalize data logic moved here
  const displayTime = details.time || formatTime(details.date);
  const location = details.location || 'No location specified';
  const difficulty = details.difficultyLevel || details.difficulty || 'N/A';
  const equipment = details.equipment || [];
  const current = details.currentParticipants || 0;
  const max = details.maxParticipants || '?';

  return (
    <div className="card">
      <h3
        style={{
          borderBottom: '1px solid #eee',
          paddingBottom: '8px',
          margin: '0 0 10px 0',
          fontSize: '16px',
        }}
      >
        Details
      </h3>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '10px',
          fontSize: '13px',
        }}
      >
        <InfoItem icon={Calendar} text={formatDate(details.date)} />
        <InfoItem icon={BarChart} text={difficulty} />
        <InfoItem icon={Clock} text={displayTime} />
        <InfoItem icon={User} text={`${current}/${max}`} />
        <InfoItem icon={MapPin} text={location} fullWidth />
        <InfoItem
          icon={Package}
          text={Array.isArray(equipment) ? equipment.join(', ') : equipment}
          fullWidth
        />
      </div>
    </div>
  );
};

// Helper style to keep code clean
const itemStyle = {
  display: 'flex',
  alignItems: 'center',
  gap: '8px',
  padding: '8px 10px',
  borderRadius: '12px',
  background: '#f7f7f7',
};

export default ActivityInfoCard;