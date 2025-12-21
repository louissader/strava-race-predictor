import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { MapContainer, TileLayer, CircleMarker } from 'react-leaflet'
import axios from 'axios'
import 'leaflet/dist/leaflet.css'

const API_URL = 'http://localhost:5001/api'

function Heatmap() {
  const [heatmapData, setHeatmapData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    axios.get(`${API_URL}/heatmap_coordinates`)
      .then(res => {
        setHeatmapData(res.data)
        setLoading(false)
      })
      .catch(err => {
        console.error(err)
        setLoading(false)
      })
  }, [])

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className="page-header">
        <h1 className="page-title">Running Heatmap 🗺️</h1>
        <p className="page-subtitle">Where your feet have taken you</p>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '4rem' }}>
          <div style={{ fontSize: '3rem' }}>🏃‍♂️</div>
          <p style={{ color: 'var(--text-secondary)', marginTop: '1rem' }}>Loading your routes...</p>
        </div>
      ) : (
        <div className="card" style={{ padding: 0, overflow: 'hidden', height: '70vh' }}>
          {heatmapData && (
            <MapContainer
              center={heatmapData.center}
              zoom={13}
              style={{ height: '100%', width: '100%' }}
            >
              <TileLayer
                url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
              />
              {heatmapData.coordinates.map((coord, idx) => (
                <CircleMarker
                  key={idx}
                  center={coord}
                  radius={3}
                  pathOptions={{
                    fillColor: '#00f5d4',
                    fillOpacity: 0.6,
                    color: '#00f5d4',
                    weight: 1
                  }}
                />
              ))}
            </MapContainer>
          )}
        </div>
      )}

      <div style={{ marginTop: '1rem', padding: '1rem', background: 'rgba(0, 245, 212, 0.1)', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
          💡 <strong>Note:</strong> This is simulated data. To show actual GPS routes, integrate with Strava's detailed activity streams API to fetch polyline data for each run.
        </p>
      </div>
    </motion.div>
  )
}

export default Heatmap
