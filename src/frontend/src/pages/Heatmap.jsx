import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { MapContainer, TileLayer, Polyline, useMap } from 'react-leaflet'
import axios from 'axios'
import 'leaflet/dist/leaflet.css'
import { formatPace } from '../utils/formatters'

const API_URL = 'http://localhost:5001/api'

// Helper function to get color based on pace (min/mi)
const getPaceColor = (paceMinPerMile) => {
  if (!paceMinPerMile || paceMinPerMile < 3 || paceMinPerMile > 20) {
    return '#808080' // Gray for missing/invalid data
  }

  // Color scale: 6min/mi = red (fast), 11min/mi = blue (slow)
  if (paceMinPerMile <= 6) return '#ff0000'      // Red - very fast
  if (paceMinPerMile <= 7) return '#ff6600'      // Orange-red
  if (paceMinPerMile <= 8) return '#ffaa00'      // Orange
  if (paceMinPerMile <= 9) return '#ffff00'      // Yellow
  if (paceMinPerMile <= 10) return '#00ff00'     // Green
  if (paceMinPerMile <= 11) return '#0000ff'     // Blue
  return '#000088'                                // Dark blue - very slow
}

// Component to recenter map when data loads
function MapController({ center }) {
  const map = useMap()

  useEffect(() => {
    if (center) {
      map.setView(center, 13)
    }
  }, [center, map])

  return null
}

function Heatmap() {
  const [routes, setRoutes] = useState([])
  const [center, setCenter] = useState([41.8781, -71.4774]) // Default center
  const [loading, setLoading] = useState(true)
  const [loadingMore, setLoadingMore] = useState(false)
  const [loadingProgress, setLoadingProgress] = useState(0)
  const [error, setError] = useState(null)
  const [displayLimit, setDisplayLimit] = useState(100) // Limit routes displayed on map
  const [totalAvailable, setTotalAvailable] = useState(0) // Total routes available on server
  const [hasMore, setHasMore] = useState(false) // Whether more routes are available on server

  // Initial load
  useEffect(() => {
    loadInitialRoutes()
  }, [])

  const loadInitialRoutes = () => {
    setLoading(true)
    setLoadingProgress(0)

    // Simulate progress for better UX
    const progressInterval = setInterval(() => {
      setLoadingProgress(prev => {
        if (prev >= 90) return prev
        return prev + Math.random() * 10
      })
    }, 500)

    axios.get(`${API_URL}/routes?limit=100&offset=0`, {
      timeout: 120000,
      responseType: 'json',
      headers: { 'Accept': 'application/json' }
    })
      .then(res => {
        const routesData = res.data.routes || []

        if (routesData.length === 0) {
          setError('No routes found in API response')
          clearInterval(progressInterval)
          setLoading(false)
          return
        }

        console.log('Loaded initial', routesData.length, 'routes')
        setRoutes(routesData)
        setTotalAvailable(res.data.total_routes || routesData.length)
        setHasMore(res.data.has_more || false)
        if (res.data.center) {
          setCenter(res.data.center)
        }
        setLoadingProgress(100)
        clearInterval(progressInterval)
        setTimeout(() => setLoading(false), 300)
      })
      .catch(err => {
        console.error('Error loading routes:', err)
        setError(err.response?.data?.error || err.message || 'Failed to load routes')
        clearInterval(progressInterval)
        setLoading(false)
      })

    return () => clearInterval(progressInterval)
  }

  const loadMoreFromServer = () => {
    if (loadingMore || !hasMore) return

    setLoadingMore(true)
    const offset = routes.length

    axios.get(`${API_URL}/routes?limit=100&offset=${offset}`, {
      timeout: 120000,
      responseType: 'json',
      headers: { 'Accept': 'application/json' }
    })
      .then(res => {
        const newRoutes = res.data.routes || []
        console.log('Loaded', newRoutes.length, 'more routes (total:', routes.length + newRoutes.length, ')')

        setRoutes(prev => [...prev, ...newRoutes])
        setHasMore(res.data.has_more || false)
        setLoadingMore(false)

        // Auto-expand display limit to show new routes
        setDisplayLimit(prev => prev + newRoutes.length)
      })
      .catch(err => {
        console.error('Error loading more routes:', err)
        setError(err.response?.data?.error || err.message || 'Failed to load more routes')
        setLoadingMore(false)
      })
  }

  const loadAllRoutes = async () => {
    if (loadingMore || !hasMore) return

    setLoadingMore(true)
    let currentOffset = routes.length
    let allNewRoutes = []
    let stillHasMore = true

    try {
      while (stillHasMore) {
        const res = await axios.get(`${API_URL}/routes?limit=100&offset=${currentOffset}`, {
          timeout: 120000,
          responseType: 'json',
          headers: { 'Accept': 'application/json' }
        })

        const newRoutes = res.data.routes || []
        allNewRoutes = [...allNewRoutes, ...newRoutes]
        stillHasMore = res.data.has_more || false
        currentOffset += newRoutes.length

        console.log(`Loaded ${allNewRoutes.length} routes so far (total will be: ${routes.length + allNewRoutes.length})`)
      }

      console.log('Finished loading all routes:', routes.length + allNewRoutes.length, 'total')
      setRoutes(prev => [...prev, ...allNewRoutes])
      setHasMore(false)
      setDisplayLimit(prev => prev + allNewRoutes.length)
      setLoadingMore(false)
    } catch (err) {
      console.error('Error loading all routes:', err)
      setError(err.response?.data?.error || err.message || 'Failed to load all routes')
      setLoadingMore(false)
    }
  }

  // Group coordinates by pace to create colored segments
  const getRouteSegments = (route) => {
    const segments = []
    let currentSegment = []
    let currentPace = null

    route.coordinates.forEach((coord, i) => {
      const pace = route.paces[i]

      if (i === 0 || pace === currentPace || (!pace && !currentPace)) {
        currentSegment.push(coord)
      } else {
        if (currentSegment.length > 1) {
          segments.push({
            coords: currentSegment,
            pace: currentPace
          })
        }
        currentSegment = [route.coordinates[i-1], coord] // Overlap to connect segments
        currentPace = pace
      }
    })

    // Add final segment
    if (currentSegment.length > 1) {
      segments.push({
        coords: currentSegment,
        pace: currentPace
      })
    }

    return segments
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.4 }}
    >
      <div style={{ marginBottom: '1.5rem' }}>
        <h1 className="page-title">Route Heatmap 🗺️</h1>
        <p className="page-subtitle">
          GPS routes colored by pace • {routes ? `${routes.length} runs loaded` : 'Loading...'}
        </p>
      </div>

      {loading && (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          {/* Running person animation */}
          <div style={{
            fontSize: '3rem',
            marginBottom: '1.5rem',
            animation: 'run 1.5s infinite',
            display: 'inline-block'
          }}>
            🏃‍♂️
          </div>

          <p style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '1rem' }}>
            Loading GPS routes from Strava...
          </p>

          {/* Progress bar */}
          <div style={{
            width: '100%',
            maxWidth: '400px',
            height: '8px',
            background: 'rgba(255, 255, 255, 0.1)',
            borderRadius: '4px',
            overflow: 'hidden',
            margin: '1.5rem auto',
            position: 'relative'
          }}>
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${loadingProgress}%` }}
              transition={{ duration: 0.3 }}
              style={{
                height: '100%',
                background: 'linear-gradient(90deg, var(--accent-primary), var(--accent-secondary))',
                borderRadius: '4px',
                boxShadow: '0 0 10px rgba(0, 245, 212, 0.5)'
              }}
            />
          </div>

          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            {Math.round(loadingProgress)}% • Fetching detailed route data...
          </p>

          <p style={{ color: 'var(--text-secondary)', fontSize: '0.75rem', marginTop: '0.5rem' }}>
            This may take 20-30 seconds for recent runs
          </p>

          <style>{`
            @keyframes run {
              0%, 100% { transform: translateX(-10px) scale(1); }
              50% { transform: translateX(10px) scale(1.1); }
            }
          `}</style>
        </div>
      )}

      {error && (
        <div className="card" style={{ background: 'rgba(255, 107, 157, 0.1)', border: '1px solid var(--accent-secondary)' }}>
          <h3 style={{ color: 'var(--accent-secondary)', marginBottom: '1rem' }}>Error Loading Routes</h3>
          <p>{error}</p>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginTop: '1rem' }}>
            Make sure your Strava credentials are configured correctly in the .env file
          </p>
        </div>
      )}

      {!loading && !error && routes && routes.length === 0 && (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>📍</div>
          <p>No GPS data found for recent runs</p>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginTop: '0.5rem' }}>
            Routes must have GPS tracking enabled on Strava
          </p>
        </div>
      )}

      {!loading && !error && routes && routes.length > 0 && (
        <>
          {/* Display info and controls */}
          <div className="card" style={{ marginBottom: '1rem', padding: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
              <div>
                <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                  Showing <span style={{ color: 'var(--accent-primary)', fontWeight: '600' }}>{Math.min(displayLimit, routes.length)}</span> of <span style={{ color: 'var(--accent-primary)', fontWeight: '600' }}>{routes.length}</span> routes on map
                  {totalAvailable > routes.length && (
                    <span> • <span style={{ color: 'var(--accent-primary)', fontWeight: '600' }}>{totalAvailable}</span> total available</span>
                  )}
                </p>
              </div>
              <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                {routes.length > displayLimit && (
                  <>
                    <button
                      onClick={() => setDisplayLimit(prev => Math.min(prev + 100, routes.length))}
                      style={{
                        padding: '0.5rem 1rem',
                        background: 'var(--accent-primary)',
                        color: '#000',
                        border: 'none',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        fontWeight: '600',
                        fontSize: '0.875rem'
                      }}
                    >
                      Show 100 More
                    </button>
                    <button
                      onClick={() => setDisplayLimit(routes.length)}
                      style={{
                        padding: '0.5rem 1rem',
                        background: 'rgba(0, 245, 212, 0.1)',
                        color: 'var(--accent-primary)',
                        border: '1px solid var(--accent-primary)',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        fontWeight: '600',
                        fontSize: '0.875rem'
                      }}
                    >
                      Show All Loaded ({routes.length})
                    </button>
                  </>
                )}
                {hasMore && (
                  <>
                    <button
                      onClick={loadMoreFromServer}
                      disabled={loadingMore}
                      style={{
                        padding: '0.5rem 1rem',
                        background: loadingMore ? 'rgba(255, 107, 157, 0.3)' : 'var(--accent-secondary)',
                        color: '#000',
                        border: 'none',
                        borderRadius: '6px',
                        cursor: loadingMore ? 'not-allowed' : 'pointer',
                        fontWeight: '600',
                        fontSize: '0.875rem',
                        opacity: loadingMore ? 0.6 : 1
                      }}
                    >
                      {loadingMore ? 'Loading...' : 'Load 100 More'}
                    </button>
                    <button
                      onClick={loadAllRoutes}
                      disabled={loadingMore}
                      style={{
                        padding: '0.5rem 1rem',
                        background: loadingMore ? 'rgba(0, 245, 212, 0.2)' : 'rgba(0, 245, 212, 0.1)',
                        color: 'var(--accent-primary)',
                        border: '1px solid var(--accent-primary)',
                        borderRadius: '6px',
                        cursor: loadingMore ? 'not-allowed' : 'pointer',
                        fontWeight: '600',
                        fontSize: '0.875rem',
                        opacity: loadingMore ? 0.6 : 1
                      }}
                    >
                      {loadingMore ? 'Loading All...' : `Load All (${totalAvailable - routes.length} remaining)`}
                    </button>
                  </>
                )}
                {!hasMore && routes.length > 0 && routes.length === totalAvailable && (
                  <span style={{ padding: '0.5rem 1rem', color: 'var(--accent-primary)', fontSize: '0.875rem', fontWeight: '600' }}>
                    ✓ All {routes.length} routes loaded!
                  </span>
                )}
              </div>
            </div>
          </div>

          <div style={{
            height: '600px',
            borderRadius: '12px',
            overflow: 'hidden',
            border: '2px solid var(--border-color)',
            marginBottom: '1.5rem',
            position: 'relative'
          }}>
            {/* Pace Legend */}
            <div style={{
              position: 'absolute',
              top: '10px',
              right: '10px',
              background: 'rgba(10, 14, 39, 0.95)',
              padding: '1rem',
              borderRadius: '8px',
              zIndex: 1000,
              border: '1px solid var(--border-color)',
              minWidth: '180px'
            }}>
              <h4 style={{ color: '#fff', marginBottom: '0.75rem', fontSize: '0.875rem', fontWeight: '600' }}>
                Pace (min/mi)
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.35rem', fontSize: '0.75rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <div style={{ width: '20px', height: '3px', background: '#ff0000', borderRadius: '2px' }}></div>
                  <span>≤6:00 (Fast)</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <div style={{ width: '20px', height: '3px', background: '#ff6600', borderRadius: '2px' }}></div>
                  <span>6-7</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <div style={{ width: '20px', height: '3px', background: '#ffaa00', borderRadius: '2px' }}></div>
                  <span>7-8</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <div style={{ width: '20px', height: '3px', background: '#ffff00', borderRadius: '2px' }}></div>
                  <span>8-9</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <div style={{ width: '20px', height: '3px', background: '#00ff00', borderRadius: '2px' }}></div>
                  <span>9-10</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <div style={{ width: '20px', height: '3px', background: '#0000ff', borderRadius: '2px' }}></div>
                  <span>10-11</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <div style={{ width: '20px', height: '3px', background: '#000088', borderRadius: '2px' }}></div>
                  <span>≥11 (Recovery)</span>
                </div>
              </div>
            </div>

            <MapContainer
              center={center}
              zoom={13}
              style={{ height: '100%', width: '100%' }}
              zoomControl={true}
            >
              <MapController center={center} />

              {/* Dark theme map tiles */}
              <TileLayer
                url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
              />

              {/* Draw polylines for each route with pace-based coloring */}
              {routes.slice(0, displayLimit).map((route, idx) => {
                const segments = getRouteSegments(route)

                return segments.map((segment, segIdx) => (
                  <Polyline
                    key={`${idx}-${segIdx}`}
                    positions={segment.coords}
                    pathOptions={{
                      color: getPaceColor(segment.pace),
                      weight: 3,
                      opacity: 0.7
                    }}
                  >
                  </Polyline>
                ))
              })}
            </MapContainer>
          </div>

          {/* Route list */}
          <div className="card">
            <h3 style={{ marginBottom: '1rem', color: 'var(--accent-primary)' }}>
              Recent Routes ({routes.length})
            </h3>
            <div style={{ display: 'grid', gap: '0.75rem' }}>
              {routes.slice(0, 10).map((route, idx) => (
                <div
                  key={idx}
                  style={{
                    padding: '0.75rem',
                    background: 'rgba(0, 245, 212, 0.05)',
                    borderRadius: '8px',
                    border: '1px solid rgba(0, 245, 212, 0.2)',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                  }}
                >
                  <div>
                    <div style={{ fontWeight: '600', marginBottom: '0.25rem' }}>{route.name}</div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                      {route.date} • Avg pace: {formatPace(route.avg_pace)} /mi
                    </div>
                  </div>
                  <div style={{
                    padding: '0.5rem 1rem',
                    background: getPaceColor(route.avg_pace),
                    borderRadius: '6px',
                    fontSize: '0.875rem',
                    fontWeight: '600',
                    color: '#000'
                  }}>
                    {formatPace(route.avg_pace)}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </motion.div>
  )
}

export default Heatmap