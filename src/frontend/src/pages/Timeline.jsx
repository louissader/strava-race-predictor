import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import axios from 'axios'
import { formatPace, formatTime } from '../utils/formatters'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001'

function Timeline() {
  const [selectedDistance, setSelectedDistance] = useState('5K')
  const [timelineData, setTimelineData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [rangeStart, setRangeStart] = useState(0)
  const [rangeEnd, setRangeEnd] = useState(100)

  const distances = ['5K', '10K', 'Half Marathon', 'Marathon']

  useEffect(() => {
    fetchTimelineData()
  }, [selectedDistance])

  const fetchTimelineData = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.get(
        `${API_URL}/api/timeline_predictions?distance=${selectedDistance}`,
        { timeout: 30000 } // 30 seconds timeout
      )
      setTimelineData(response.data)
      setLoading(false)
    } catch (err) {
      console.error('Error fetching timeline data:', err)
      setError('Timeline predictions unavailable. The ML models need to be retrained with your current scikit-learn version. Run: python3 src/backend/models/train_model.py')
      setLoading(false)
    }
  }

  // Calculate filtered data based on range slider
  const getFilteredData = () => {
    if (timelineData.length === 0) return []

    const totalPoints = timelineData.length
    const startIdx = Math.floor((rangeStart / 100) * totalPoints)
    const endIdx = Math.ceil((rangeEnd / 100) * totalPoints)

    return timelineData.slice(startIdx, endIdx)
  }

  const filteredData = getFilteredData()

  // Calculate current prediction stats from filtered data
  const getCurrentStats = () => {
    if (filteredData.length === 0) {
      return { predictedTime: 'N/A', avgWeekly: 0, avgMonthly: 0, improvement: 0 }
    }

    const latest = filteredData[filteredData.length - 1]
    const earliest = filteredData[0]

    const avgWeekly = (filteredData.reduce((sum, d) => sum + d.weekly_distance, 0) / filteredData.length).toFixed(1)
    const avgMonthly = (filteredData.reduce((sum, d) => sum + d.monthly_distance, 0) / filteredData.length).toFixed(1)

    // Calculate improvement (negative means faster time)
    const improvement = earliest.predicted_time_min - latest.predicted_time_min

    return {
      predictedTime: latest.predicted_time_min,
      avgWeekly,
      avgMonthly,
      improvement,
      dateRange: `${earliest.date} to ${latest.date}`
    }
  }

  const stats = getCurrentStats()

  const handleRangeChange = (e) => {
    const value = parseInt(e.target.value)
    if (e.target.name === 'start') {
      setRangeStart(Math.min(value, rangeEnd - 1))
    } else {
      setRangeEnd(Math.max(value, rangeStart + 1))
    }
  }

  // Get race distance in readable format
  const getDistanceInfo = (distance) => {
    const info = {
      '5K': { km: 5, mi: 3.1 },
      '10K': { km: 10, mi: 6.2 },
      'Half Marathon': { km: 21.1, mi: 13.1 },
      'Marathon': { km: 42.2, mi: 26.2 }
    }
    return info[distance] || { km: 0, mi: 0 }
  }

  const distanceInfo = getDistanceInfo(selectedDistance)

  if (loading) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        <div className="page-header">
          <h1 className="page-title">Timeline ⏰</h1>
          <p className="page-subtitle">Prediction evolution over time</p>
        </div>
        <div className="card">
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            <p style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>Loading timeline data...</p>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
              Calculating predictions across your training history. This may take 10-20 seconds.
            </p>
          </div>
        </div>
      </motion.div>
    )
  }

  if (error) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        <div className="page-header">
          <h1 className="page-title">Timeline ⏰</h1>
          <p className="page-subtitle">Prediction evolution over time</p>
        </div>
        <div className="card">
          <p style={{ color: 'var(--danger)' }}>{error}</p>
        </div>
      </motion.div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className="page-header">
        <h1 className="page-title">Timeline ⏰</h1>
        <p className="page-subtitle">How your predicted race times evolved over time</p>
      </div>

      {/* Distance selector */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          {distances.map((distance) => (
            <button
              key={distance}
              className={selectedDistance === distance ? 'btn btn-primary' : 'btn btn-secondary'}
              onClick={() => setSelectedDistance(distance)}
              style={{ flex: '1', minWidth: '100px' }}
            >
              {distance}
            </button>
          ))}
        </div>
      </div>

      {/* Current prediction based on selected range */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '1.25rem', marginBottom: '1rem', color: 'var(--text)' }}>
          Current Prediction
        </h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
          <div>
            <div className="stat-label">Predicted Time</div>
            <div className="stat-value" style={{ fontSize: '2rem', color: 'var(--primary)' }}>
              {typeof stats.predictedTime === 'number' ? formatTime(stats.predictedTime) : stats.predictedTime}
            </div>
            <div className="stat-label" style={{ marginTop: '0.25rem' }}>
              {formatPace(stats.predictedTime / distanceInfo.mi)} /mi avg
            </div>
          </div>
          <div>
            <div className="stat-label">Training Volume</div>
            <div className="stat-value">{stats.avgWeekly} km/week</div>
            <div className="stat-label" style={{ marginTop: '0.25rem' }}>
              {stats.avgMonthly} km/month
            </div>
          </div>
          <div>
            <div className="stat-label">Time Improvement</div>
            <div
              className="stat-value"
              style={{
                color: stats.improvement > 0 ? 'var(--success)' : stats.improvement < 0 ? 'var(--danger)' : 'var(--text)'
              }}
            >
              {stats.improvement > 0 ? '-' : '+'}{Math.abs(stats.improvement).toFixed(1)} min
            </div>
            <div className="stat-label" style={{ marginTop: '0.25rem' }}>
              {stats.improvement > 0 ? 'Faster' : stats.improvement < 0 ? 'Slower' : 'No change'}
            </div>
          </div>
        </div>
      </div>

      {/* Timeline range slider */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '1.25rem', marginBottom: '1rem', color: 'var(--text)' }}>
          Time Range
        </h2>
        <div style={{ padding: '0 0.5rem' }}>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            marginBottom: '1rem',
            fontSize: '0.9rem',
            color: 'var(--text-secondary)'
          }}>
            <span>{timelineData[0]?.date || 'Start'}</span>
            <span>{stats.dateRange || 'Select range'}</span>
            <span>{timelineData[timelineData.length - 1]?.date || 'End'}</span>
          </div>

          {/* Dual range slider */}
          <div style={{ position: 'relative', height: '60px' }}>
            {/* Track background */}
            <div style={{
              position: 'absolute',
              top: '50%',
              left: 0,
              right: 0,
              height: '8px',
              background: 'var(--border)',
              borderRadius: '4px',
              transform: 'translateY(-50%)'
            }} />

            {/* Active range track */}
            <div style={{
              position: 'absolute',
              top: '50%',
              left: `${rangeStart}%`,
              width: `${rangeEnd - rangeStart}%`,
              height: '8px',
              background: 'linear-gradient(90deg, var(--primary), var(--success))',
              borderRadius: '4px',
              transform: 'translateY(-50%)'
            }} />

            {/* Start slider */}
            <input
              type="range"
              name="start"
              min="0"
              max="100"
              value={rangeStart}
              onChange={handleRangeChange}
              style={{
                position: 'absolute',
                width: '100%',
                top: '50%',
                transform: 'translateY(-50%)',
                pointerEvents: 'all',
                WebkitAppearance: 'none',
                appearance: 'none',
                background: 'transparent',
                height: '40px',
                outline: 'none'
              }}
            />

            {/* End slider */}
            <input
              type="range"
              name="end"
              min="0"
              max="100"
              value={rangeEnd}
              onChange={handleRangeChange}
              style={{
                position: 'absolute',
                width: '100%',
                top: '50%',
                transform: 'translateY(-50%)',
                pointerEvents: 'all',
                WebkitAppearance: 'none',
                appearance: 'none',
                background: 'transparent',
                height: '40px',
                outline: 'none'
              }}
            />
          </div>

          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            marginTop: '0.5rem',
            fontSize: '0.85rem',
            color: 'var(--text-secondary)'
          }}>
            <span>{filteredData.length} data points</span>
            <span>{Math.round((rangeEnd - rangeStart) / 100 * timelineData.length)} months</span>
          </div>
        </div>
      </div>

      {/* Timeline visualization */}
      <div className="card">
        <h2 style={{ fontSize: '1.25rem', marginBottom: '1rem', color: 'var(--text)' }}>
          Prediction History
        </h2>

        <div style={{
          overflowX: 'auto',
          marginTop: '1rem',
          maxHeight: '400px',
          overflowY: 'auto'
        }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead style={{ position: 'sticky', top: 0, background: 'var(--card)', zIndex: 1 }}>
              <tr style={{ borderBottom: '2px solid var(--border)' }}>
                <th style={{ padding: '0.75rem', textAlign: 'left' }}>Date</th>
                <th style={{ padding: '0.75rem', textAlign: 'right' }}>Predicted Time</th>
                <th style={{ padding: '0.75rem', textAlign: 'right' }}>Pace</th>
                <th style={{ padding: '0.75rem', textAlign: 'right' }}>Weekly km</th>
                <th style={{ padding: '0.75rem', textAlign: 'right' }}>Monthly km</th>
              </tr>
            </thead>
            <tbody>
              {filteredData.map((point, index) => {
                const avgPace = point.predicted_time_min / distanceInfo.mi
                return (
                  <motion.tr
                    key={point.date}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: Math.min(index * 0.02, 0.3) }}
                    style={{
                      borderBottom: '1px solid var(--border)',
                      background: index === filteredData.length - 1 ? 'rgba(var(--primary-rgb), 0.1)' : 'transparent'
                    }}
                  >
                    <td style={{ padding: '0.75rem' }}>
                      {point.date}
                      {index === filteredData.length - 1 && (
                        <span style={{
                          marginLeft: '0.5rem',
                          fontSize: '0.75rem',
                          color: 'var(--primary)',
                          fontWeight: 'bold'
                        }}>
                          LATEST
                        </span>
                      )}
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'right', fontWeight: '500' }}>
                      {formatTime(point.predicted_time_min)}
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'right', color: 'var(--text-secondary)' }}>
                      {formatPace(avgPace)} /mi
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'right' }}>
                      {point.weekly_distance} km
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'right' }}>
                      {point.monthly_distance} km
                    </td>
                  </motion.tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </div>

      <style>{`
        input[type="range"] {
          -webkit-appearance: none;
          appearance: none;
          background: transparent;
          cursor: pointer;
        }

        input[type="range"]::-webkit-slider-thumb {
          -webkit-appearance: none;
          appearance: none;
          width: 20px;
          height: 20px;
          border-radius: 50%;
          background: var(--primary);
          border: 3px solid var(--card);
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
          cursor: pointer;
          position: relative;
          z-index: 3;
        }

        input[type="range"]::-moz-range-thumb {
          width: 20px;
          height: 20px;
          border-radius: 50%;
          background: var(--primary);
          border: 3px solid var(--card);
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
          cursor: pointer;
          position: relative;
          z-index: 3;
        }

        input[type="range"]::-webkit-slider-thumb:hover {
          transform: scale(1.2);
          transition: transform 0.2s;
        }

        input[type="range"]::-moz-range-thumb:hover {
          transform: scale(1.2);
          transition: transform 0.2s;
        }
      `}</style>
    </motion.div>
  )
}

export default Timeline
