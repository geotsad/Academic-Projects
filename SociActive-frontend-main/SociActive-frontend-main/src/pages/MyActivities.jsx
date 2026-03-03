// src/pages/MyActivities.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { activityService } from '../api/activityService';
import { useAuth } from '../context/AuthContext';
import useFetch from '../hooks/useFetch';
import ActivityCard from '../components/ActivityCard';
import { ArrowLeft } from 'lucide-react';

// Reusable Activity Section Component
const ActivitySection = ({ title, activities, loading, onAction, type, marginTop = '0' }) => (
  <div className="card" style={{ marginTop }}>
    <h3 style={{ marginTop: 0 }}>{title}</h3>

    {loading && <p>Loading {title.toLowerCase()}...</p>}
    {!loading && (!activities || activities.length === 0) && (
      <p>No {title.toLowerCase()}.</p>
    )}

    {activities?.map((act) => (
      <ActivityCard
        key={act.activityId}
        activity={act}
        type={type}
        onAction={onAction}
      />
    ))}
  </div>
);

const MyActivities = () => {
  const navigate = useNavigate();
  const { userId: authUserId } = useAuth();

  // Αν δεν έχει token user, fallback στο 1 (για mock)
  const userId = authUserId ?? 1;

  // Φέρνουμε upcoming
  const { data: upcoming, loading: loadingUpcoming } = useFetch(
    () => activityService.getMyUpcoming(userId),
    [userId]
  );

  // Φέρνουμε completed
  const { data: completed, loading: loadingCompleted } = useFetch(
    () => activityService.getMyCompleted(userId),
    [userId]
  );

  // Leave action (future - προς το παρόν απλώς alert)
  const handleLeave = async (activityId) => {
    alert(`Leaving activity ${activityId} (mock only).`);
  };

  // Save action (future)
  const handleSave = async (activityId) => {
    alert(`Saving activity ${activityId} (mock only).`);
  };

  return (
    <div className="container">
      {/* ------------------ HEADER ------------------ */}
      <div
        className="my-activities-header"
        style={{
          background: 'var(--primary-green)',
          color: 'white',
          padding: '15px 20px',
          borderRadius: '50px',
          margin: '0 0 20px 0',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          position: 'relative'
        }}
      >
        <ArrowLeft
          style={{
            cursor: 'pointer',
            position: 'absolute',
            left: 20
          }}
          onClick={() => navigate('/')}
        />

        <h2 className="title-text" style={{ margin: 0 }}>
          My Activities
        </h2>
      </div>

      {/* ------------------ UPCOMING ------------------ */}
      <ActivitySection
        title="Upcoming Activities"
        activities={upcoming}
        loading={loadingUpcoming}
        onAction={handleLeave}
        type="my_upcoming"
      />

      {/* ------------------ COMPLETED ------------------ */}
      <ActivitySection
        title="Completed Activities"
        activities={completed}
        loading={loadingCompleted}
        onAction={handleSave}
        type="my_completed"
        marginTop="20px"
      />
    </div>
  );
};

export default MyActivities;
