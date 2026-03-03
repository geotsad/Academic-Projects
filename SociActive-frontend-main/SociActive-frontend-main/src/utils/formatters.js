/**
 * src/utils/formatters.js
 * Helper functions to format dates and times consistently.
 */

// Helper to pad numbers to 2 digits
const pad2 = (num) => String(num).padStart(2, '0');

/**
 * Formats a date input into "DD/MM/YYYY"
 * Handles:
 * 1. Arrays [2025, 3, 20] (Common Backend format)
 * 2. Arrays [20, 3, 2025] (Mock format)
 * 3. Strings "2025-03-20"
 */
export const formatDate = (date) => {
  if (!date) return 'N/A';

  if (Array.isArray(date)) {
    // If array is empty or too short
    if (date.length < 3) return 'Invalid Date';

    let day, month, year;

    // Check if the first number is a Year (e.g., 2025)
    if (date[0] > 31) {
      // Format: [Year, Month, Day]
      [year, month, day] = date;
    } else {
      // Format: [Day, Month, Year]
      [day, month, year] = date;
    }

    // Pad with zeros (e.g., 3 -> 03)
    const dayStr = pad2(day);
    const monthStr = pad2(month);

    return `${dayStr}/${monthStr}/${year}`;
  }

  // If it's a string, return as is or try to parse standard date
  return String(date);
};

/**
 * Formats time into "HH:MM"
 * Handles:
 * 1. Arrays [..., ..., ..., 8, 30] (Extracts time from LocalDateTime array)
 * 2. Strings "8:30" -> "08:30"
 */
export const formatTime = (time) => {
  if (!time) return '--:--';

  // 1. Handle Array (e.g., [2025, 3, 20, 8, 30])
  if (Array.isArray(time)) {
    if (time.length >= 5) {
      return `${pad2(time[3])}:${pad2(time[4])}`;
    }
    // If array is just [8, 30]
    if (time.length === 2) {
      return `${pad2(time[0])}:${pad2(time[1])}`;
    }
  }

  // 2. Handle String (e.g., "8:30")
  if (typeof time === 'string') {
    // If it already has a colon
    if (time.includes(':')) {
        const [h, m] = time.split(':');
        return `${pad2(h)}:${pad2(m)}`;
    }
  }

  return String(time);
};

export const getInitials = (name) => {
  if (!name) return '?';
  const parts = name.trim().split(' ');
  if (parts.length === 1) return parts[0][0].toUpperCase();
  return (parts[0][0] + parts[1][0]).toUpperCase();
};