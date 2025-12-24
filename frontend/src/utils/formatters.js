/**
 * Format pace from decimal minutes (e.g., 7.88) to MM:SS format (e.g., 7:53)
 * @param {number} paceDecimal - Pace in decimal minutes per mile
 * @returns {string} Formatted pace as MM:SS
 */
export const formatPace = (paceDecimal) => {
  if (!paceDecimal || isNaN(paceDecimal)) return 'N/A'

  const minutes = Math.floor(paceDecimal)
  const seconds = Math.round((paceDecimal - minutes) * 60)

  // Handle edge case where seconds round to 60
  if (seconds === 60) {
    return `${minutes + 1}:00`
  }

  return `${minutes}:${seconds.toString().padStart(2, '0')}`
}

/**
 * Format time from minutes to HH:MM:SS or MM:SS
 * @param {number} minutes - Time in minutes
 * @returns {string} Formatted time
 */
export const formatTime = (minutes) => {
  if (!minutes || isNaN(minutes)) return 'N/A'

  const hours = Math.floor(minutes / 60)
  const mins = Math.floor(minutes % 60)
  const secs = Math.round((minutes % 1) * 60)

  if (hours > 0) {
    return `${hours}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  return `${mins}:${secs.toString().padStart(2, '0')}`
}
