import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Trophy, Zap, Mountain, Target, TrendingUp, Award } from 'lucide-react'
import axios from 'axios'

const API_URL = 'http://localhost:5001/api'

function Dashboard({ stats }) {
  const [impressiveActivities, setImpressiveActivities] = useState(null)
  const [predictions, setPredictions] = useState(null)

  useEffect(() => {
    // Fetch impressive activities
    axios.get(`${API_URL}/impressive-activities`)
      .then(res => setImpressiveActivities(res.data))
      .catch(err => console.error(err))

    // Fetch predictions
    axios.get(`${API_URL}/predictions`)
      .then(res => setPredictions(res.data))
      .catch(err => console.error(err))
  }, [])

  const formatTime = (minutes) => {
    const hrs = Math.floor(minutes / 60)
    const mins = Math.floor(minutes % 60)
    const secs = Math.floor((minutes % 1) * 60)
    return hrs > 0 ? `${hrs}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}` : `${mins}:${String(secs).padStart(2, '0')}`
  }

  const formatDate = (dateStr) => {
    return new Date(dateStr).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.4 }}
    >
      {/* Hero Section */}
      <div className="hero-section" style={{
        background: 'linear-gradient(135deg, rgba(0, 245, 212, 0.1) 0%, rgba(255, 107, 157, 0.1) 100%)',
        borderRadius: '24px',
        padding: '3rem 2rem',
        marginBottom: '2rem',
        border: '1px solid var(--border-color)'
      }}>
        <h1 className="page-title" style={{ marginBottom: '1rem' }}>
          Your Running Journey 🏃‍♂️
        </h1>
        <p className="page-subtitle">
          {stats ? `${stats.total_runs} runs • ${stats.total_distance_mi} mi • ${stats.total_time_hours} hours of pure determination` : 'Loading your stats...'}
        </p>
      </div>

      {/* Quick Stats */}
      {stats && (
        <div className="grid-4" style={{ marginBottom: '2rem' }}>
          <motion.div
            className="stat-card"
            whileHover={{ scale: 1.05 }}
            style={{ background: 'linear-gradient(135deg, var(--bg-card), rgba(0, 245, 212, 0.1))' }}
          >
            <Trophy size={32} color="var(--accent-primary)" style={{ marginBottom: '1rem' }} />
            <div className="stat-value">{stats.total_runs}</div>
            <div className="stat-label">Total Runs</div>
          </motion.div>

          <motion.div
            className="stat-card"
            whileHover={{ scale: 1.05 }}
            style={{ background: 'linear-gradient(135deg, var(--bg-card), rgba(255, 107, 157, 0.1))' }}
          >
            <Target size={32} color="var(--accent-secondary)" style={{ marginBottom: '1rem' }} />
            <div className="stat-value">{stats.total_distance_mi}</div>
            <div className="stat-label">Miles</div>
          </motion.div>

          <motion.div
            className="stat-card"
            whileHover={{ scale: 1.05 }}
            style={{ background: 'linear-gradient(135deg, var(--bg-card), rgba(255, 210, 63, 0.1))' }}
          >
            <Zap size={32} color="var(--accent-tertiary)" style={{ marginBottom: '1rem' }} />
            <div className="stat-value">{stats.avg_pace}</div>
            <div className="stat-label">Average Pace (min/mi)</div>
          </motion.div>

          <motion.div
            className="stat-card"
            whileHover={{ scale: 1.05 }}
            style={{ background: 'linear-gradient(135deg, var(--bg-card), rgba(74, 222, 128, 0.1))' }}
          >
            <Mountain size={32} color="var(--success)" style={{ marginBottom: '1rem' }} />
            <div className="stat-value">{Math.round(stats.total_elevation_ft)}</div>
            <div className="stat-label">Elevation Gain (ft)</div>
          </motion.div>
        </div>
      )}

      {/* Race Predictions */}
      {predictions && (
        <div style={{ marginBottom: '2rem' }}>
          <h2 style={{ fontSize: '1.75rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <TrendingUp color="var(--accent-primary)" />
            Race Time Predictions
          </h2>
          <div className="grid-4">
            {['5K', '10K', 'Half Marathon', 'Marathon'].map((distance, idx) => {
              const pred = predictions[distance]
              const colors = ['var(--accent-primary)', 'var(--accent-secondary)', 'var(--accent-tertiary)', 'var(--success)']
              return (
                <motion.div
                  key={distance}
                  className="card"
                  whileHover={{ scale: 1.03 }}
                  style={{
                    borderLeft: `4px solid ${colors[idx]}`,
                    background: `linear-gradient(135deg, var(--bg-card), ${colors[idx]}15)`
                  }}
                >
                  <h3 style={{ color: colors[idx], marginBottom: '1rem', fontSize: '1.25rem' }}>{distance}</h3>
                  {pred.has_model ? (
                    <>
                      <div style={{ fontSize: '1.75rem', fontWeight: '700', color: 'var(--text-primary)', marginBottom: '0.5rem', fontFamily: 'JetBrains Mono' }}>
                        {formatTime(pred.best_time_min)}
                      </div>
                      <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                        Best Time ({pred.num_races} races)
                      </div>
                      <div style={{ marginTop: '0.75rem', padding: '0.5rem', background: 'rgba(0,0,0,0.2)', borderRadius: '8px', fontSize: '0.75rem' }}>
                        ±{pred.model_accuracy_mae.toFixed(1)} min accuracy
                      </div>
                    </>
                  ) : (
                    <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                      Need {5 - pred.num_races} more races
                    </div>
                  )}
                </motion.div>
              )
            })}
          </div>
        </div>
      )}

      {/* Impressive Activities */}
      {impressiveActivities && (
        <div>
          <h2 style={{ fontSize: '1.75rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Award color="var(--accent-tertiary)" />
            Hall of Fame
          </h2>

          <div className="grid-2" style={{ gap: '1.5rem' }}>
            {/* Longest Runs */}
            <motion.div
              className="card card-glow"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 }}
            >
              <h3 style={{ color: 'var(--accent-primary)', marginBottom: '1rem', fontSize: '1.25rem' }}>
                🏅 Longest Runs
              </h3>
              {impressiveActivities.longest_runs.map((run, idx) => (
                <div key={idx} style={{
                  padding: '0.75rem',
                  background: 'rgba(0, 245, 212, 0.05)',
                  borderRadius: '8px',
                  marginBottom: '0.5rem',
                  borderLeft: `3px solid var(--accent-primary)`
                }}>
                  <div style={{ fontWeight: '600', marginBottom: '0.25rem' }}>{run.name}</div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                    <span>{run.distance_mi.toFixed(2)} mi</span>
                    <span>{formatDate(run.start_date)}</span>
                  </div>
                </div>
              ))}
            </motion.div>

            {/* Fastest Paces */}
            <motion.div
              className="card card-glow"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
            >
              <h3 style={{ color: 'var(--accent-secondary)', marginBottom: '1rem', fontSize: '1.25rem' }}>
                ⚡ Fastest Paces
              </h3>
              {impressiveActivities.fastest_paces.map((run, idx) => (
                <div key={idx} style={{
                  padding: '0.75rem',
                  background: 'rgba(255, 107, 157, 0.05)',
                  borderRadius: '8px',
                  marginBottom: '0.5rem',
                  borderLeft: `3px solid var(--accent-secondary)`
                }}>
                  <div style={{ fontWeight: '600', marginBottom: '0.25rem' }}>{run.name}</div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                    <span>{run.pace_min_per_mi.toFixed(2)} min/mi</span>
                    <span>{run.distance_mi.toFixed(2)} mi</span>
                  </div>
                </div>
              ))}
            </motion.div>

            {/* Highest Elevation */}
            <motion.div
              className="card card-glow"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              <h3 style={{ color: 'var(--accent-tertiary)', marginBottom: '1rem', fontSize: '1.25rem' }}>
                🏔️ Biggest Climbs
              </h3>
              {impressiveActivities.highest_elevation.map((run, idx) => (
                <div key={idx} style={{
                  padding: '0.75rem',
                  background: 'rgba(255, 210, 63, 0.05)',
                  borderRadius: '8px',
                  marginBottom: '0.5rem',
                  borderLeft: `3px solid var(--accent-tertiary)`
                }}>
                  <div style={{ fontWeight: '600', marginBottom: '0.25rem' }}>{run.name}</div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                    <span>{run.elevation_ft.toFixed(0)} ft gain</span>
                    <span>{run.distance_mi.toFixed(2)} mi</span>
                  </div>
                </div>
              ))}
            </motion.div>

            {/* Most Consistent */}
            <motion.div
              className="card card-glow"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
            >
              <h3 style={{ color: 'var(--success)', marginBottom: '1rem', fontSize: '1.25rem' }}>
                🎯 Most Consistent
              </h3>
              {impressiveActivities.most_consistent.slice(0, 5).map((run, idx) => (
                <div key={idx} style={{
                  padding: '0.75rem',
                  background: 'rgba(74, 222, 128, 0.05)',
                  borderRadius: '8px',
                  marginBottom: '0.5rem',
                  borderLeft: `3px solid var(--success)`
                }}>
                  <div style={{ fontWeight: '600', marginBottom: '0.25rem' }}>{run.name}</div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                    <span>{run.pace_min_per_mi.toFixed(2)} min/mi</span>
                    <span>{run.distance_mi.toFixed(2)} mi</span>
                  </div>
                </div>
              ))}
            </motion.div>
          </div>
        </div>
      )}
    </motion.div>
  )
}

export default Dashboard
