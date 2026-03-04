// src/api/activityService.js
import { client } from './client';

// Έξυπνος extractor που προσπαθεί να βρει όποιο array υπάρχει
const extractData = (payload) => {
  if (!payload) return [];
  if (Array.isArray(payload)) return payload;
  if (payload.data && Array.isArray(payload.data)) return payload.data;
  if (payload.content && Array.isArray(payload.content)) return payload.content;
  
  for (const key of Object.keys(payload)) {
    if (Array.isArray(payload[key])) {
      return payload[key];
    }
  }
  return [];
};

// Helper for API calls with error handling
const apiCall = async (call, errorMsg) => {
  try {
    const res = await call();
    return extractData(res.data);
  } catch (e) {
    console.error(errorMsg, e);
    return [];
  }
};

/**
 * 🎯 ΤΕΛΙΚΗ ΔΙΟΡΘΩΣΗ: Mapping των ονομάτων από το UI στο Backend
 */
const mapAndCleanFilters = (filters) => {
    const cleanedFilters = {};
    
    // 1. Difficulty Mapping (Το UI στέλνει 'difficulty', το Backend θέλει 'difficultyLevel')
    const difficultyVal = filters.difficulty || filters.difficultyLevel;
    if (difficultyVal && difficultyVal !== 'All' && difficultyVal !== '') {
        cleanedFilters.difficultyLevel = difficultyVal;
    }

    // 2. Participants Mapping (Το UI στέλνει 'participants', το Backend θέλει 'maxParticipants')
    const participantsVal = filters.participants || filters.maxParticipants;
    if (participantsVal) {
        cleanedFilters.maxParticipants = participantsVal;
    }

    // 3. Type
    if (filters.type && filters.type !== 'All' && filters.type !== '') {
        cleanedFilters.type = filters.type;
    }

    // 4. Location
    if (filters.location && filters.location !== 'All' && filters.location !== '') {
        cleanedFilters.location = filters.location;
    }

    // 5. Dates
    if (filters.dateFrom) cleanedFilters.dateFrom = filters.dateFrom;
    if (filters.dateTo) cleanedFilters.dateTo = filters.dateTo;

    // 6. Completed
    if (filters.completed !== undefined) cleanedFilters.completed = filters.completed;

    return cleanedFilters;
}


export const activityService = {
  // HOMEPAGE activities
  getUpcomingActivities: async (userId, filters = {}) => {
    try {
        console.log('1. Filters from UI:', filters);

        // 1. Καθαρισμός και χαρτογράφηση των φίλτρων
        const mappedFilters = mapAndCleanFilters(filters);
        
        console.log('2. Mapped Filters for Backend:', mappedFilters);

        // 2. Συνδυασμός με το default φίλτρο completed: false
        const params = { completed: false, ...mappedFilters };
        
        const res = await client.get(`/users/${userId}/activities`, { params });
        // console.log('getUpcomingActivities response:', res.data);
        return extractData(res.data);
    } catch (e) {
      console.error('API Error in getUpcomingActivities:', e);
      return [];
    }
  },

  // PINNED ACTIVITIES
  getPinnedActivities: async (userId) => {
    return apiCall(
      () => client.get(`/users/${userId}/activities/pinned`),
      'API Error in getPinnedActivities:'
    );
  },

  // Λεπτομέρειες Activity (View Details)
  getActivityDetails: async (userId, activityId) => {
    try {
      const res = await client.get(
        `/users/${userId}/activities/${activityId}/details`
      );
      if (res.data && res.data.data) return res.data.data;
      return res.data;
    } catch (e) {
      console.error('API Error in getActivityDetails:', e);
      return null;
    }
  },

  // JOIN activity
  joinActivity: async (userId, activityId) => {
    const res = await client.post(
      `/users/${userId}/activities/${activityId}/joinRequests`
    );
    if (res.data && res.data.success === true) {
      return res.data.data; 
    }
    throw new Error(res.data?.message || 'Join failed');
  },

  // MY UPCOMING
  getMyUpcoming: async (userId) => {
    return apiCall(
      () => client.get(`/users/${userId}/participatingActivities`),
      'API Error in getMyUpcoming:'
    );
  },

  // MY COMPLETED
  getMyCompleted: async (userId) => {
    return apiCall(
      () => client.get(`/users/${userId}/participatedActivities`),
      'API Error in getMyCompleted:'
    );
  },

  // Review
  submitReview: async (userId, activityId, payload) => {
    return client.post(
      `/users/${userId}/activities/${activityId}/reviews`,
      payload
    );
  },

  pinActivity: async (userId, activityId) => {
  return client.post(`/users/${userId}/activities/${activityId}/pins`);
  },

  unpinActivity: async (userId, activityId) => {
  return client.delete(`/users/${userId}/activities/${activityId}/pins`);
  },
};