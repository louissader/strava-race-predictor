import { useState, useEffect } from 'react'

function SimpleApp() {
  const [stats, setStats] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('http://localhost:5001/api/stats')
      .then(res => res.json())
      .then(data => {
        console.log('Data loaded:', data)
        setStats(data)
      })
      .catch(err => {
        console.error('Error:', err)
        setError(err.message)
      })
  }, [])

  return (
    <div style={{ padding: '2rem', background: '#0a0e27', color: 'white', minHeight: '100vh' }}>
      <h1 style={{ color: '#00f5d4' }}>🏃 Strava Race Predictor</h1>

      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      {stats ? (
        <div style={{ marginTop: '2rem' }}>
          <h2>Your Stats</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginTop: '1rem' }}>
            <div style={{ background: '#1a1f3a', padding: '1.5rem', borderRadius: '12px', border: '1px solid #00f5d4' }}>
              <div style={{ fontSize: '0.875rem', color: '#a0acd8' }}>TOTAL RUNS</div>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#00f5d4' }}>{stats.total_runs}</div>
            </div>
            <div style={{ background: '#1a1f3a', padding: '1.5rem', borderRadius: '12px', border: '1px solid #ff6b9d' }}>
              <div style={{ fontSize: '0.875rem', color: '#a0acd8' }}>DISTANCE (KM)</div>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#ff6b9d' }}>{stats.total_distance_km}</div>
            </div>
            <div style={{ background: '#1a1f3a', padding: '1.5rem', borderRadius: '12px', border: '1px solid #ffd23f' }}>
              <div style={{ fontSize: '0.875rem', color: '#a0acd8' }}>BEST PACE</div>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#ffd23f' }}>{stats.best_pace}</div>
            </div>
            <div style={{ background: '#1a1f3a', padding: '1.5rem', borderRadius: '12px', border: '1px solid #4ade80' }}>
              <div style={{ fontSize: '0.875rem', color: '#a0acd8' }}>TOTAL HOURS</div>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#4ade80' }}>{stats.total_time_hours}</div>
            </div>
          </div>

          <div style={{ marginTop: '2rem', padding: '1rem', background: 'rgba(0, 245, 212, 0.1)', borderRadius: '12px' }}>
            <p>✅ API is working! Full app loading...</p>
          </div>
        </div>
      ) : (
        <div style={{ marginTop: '2rem' }}>
          <p>Loading your data...</p>
        </div>
      )}
    </div>
  )
}

export default SimpleApp
