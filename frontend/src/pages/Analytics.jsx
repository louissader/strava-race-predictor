import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import axios from 'axios'
import { formatPace } from '../utils/formatters'

const API_URL = 'http://localhost:5001/api'

function Analytics() {
  const [stats, setStats] = useState(null)
  const [weeklyPatterns, setWeeklyPatterns] = useState(null)
  const [trainingTrends, setTrainingTrends] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadAnalytics()
  }, [])

  const loadAnalytics = async () => {
    try {
      setLoading(true)
      const [statsRes, patternsRes, trendsRes] = await Promise.all([
        axios.get(`${API_URL}/stats`),
        axios.get(`${API_URL}/weekly_patterns`),
        axios.get(`${API_URL}/training_trends`)
      ])

      setStats(statsRes.data)
      setWeeklyPatterns(patternsRes.data)
      setTrainingTrends(trendsRes.data)
      setLoading(false)
    } catch (err) {
      console.error('Error loading analytics:', err)
      setError(err.message)
      setLoading(false)
    }
  }

  // Calculate advanced metrics
  const calculateMetrics = () => {
    if (!stats || !weeklyPatterns || !trainingTrends) return null

    const metrics = {
      // Popular metrics based on research
      consistency: calculateConsistency(),
      preferredTime: getMostPopularRunTime(),
      preferredDay: getMostPopularDay(),
      verticalGainTotal: stats.total_elevation_ft,
      avgWeeklyDistance: calculateAvgWeeklyDistance(),
      longestStreak: calculateLongestStreak(),

      // Fun/Quirky metrics
      lifetimeEquivalent: calculateLifetimeEquivalent(),
      mountEverestsClimbed: (stats.total_elevation_ft / 29032).toFixed(2),
      shoeMileage: calculateShoeMileage(),
      totalCaloriesBurned: calculateCalories()
    }

    return metrics
  }

  const calculateConsistency = () => {
    if (!trainingTrends || trainingTrends.length === 0) return 0

    const monthsWithRuns = trainingTrends.filter(m => m.num_runs > 0).length
    const totalMonths = trainingTrends.length
    return ((monthsWithRuns / totalMonths) * 100).toFixed(0)
  }

  const getMostPopularRunTime = () => {
    if (!weeklyPatterns?.by_hour) return 'N/A'

    const hours = weeklyPatterns.by_hour
    const maxHour = Object.keys(hours).reduce((a, b) =>
      hours[a] > hours[b] ? a : b
    )

    const hour = parseInt(maxHour)
    const period = hour >= 12 ? 'PM' : 'AM'
    const displayHour = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour
    return `${displayHour}:00 ${period}`
  }

  const getMostPopularDay = () => {
    if (!weeklyPatterns?.by_day) return 'N/A'

    const days = weeklyPatterns.by_day
    return Object.keys(days).reduce((a, b) => days[a] > days[b] ? a : b)
  }

  const calculateAvgWeeklyDistance = () => {
    if (!trainingTrends || trainingTrends.length === 0) return 0

    const weeksOfData = trainingTrends.length / 4.33 // avg weeks per month
    return (stats.total_distance_mi / weeksOfData).toFixed(1)
  }

  const calculateLongestStreak = () => {
    // This would require day-by-day data, so we'll estimate
    // based on runs per month
    if (!trainingTrends || trainingTrends.length === 0) return 0

    const avgRunsPerMonth = trainingTrends.reduce((sum, m) => sum + m.num_runs, 0) / trainingTrends.length
    return Math.floor(avgRunsPerMonth / 4) // Rough estimate of weekly runs
  }

  const calculateLifetimeEquivalent = () => {
    // Average person runs 26,000 miles in lifetime
    const lifetimeDistance = 26000
    return ((stats.total_distance_mi / lifetimeDistance) * 100).toFixed(1)
  }

  const calculateShoeMileage = () => {
    // Average running shoe lasts 300-500 miles
    const avgShoeLife = 400
    return Math.floor(stats.total_distance_mi / avgShoeLife)
  }

  const calculateCalories = () => {
    // Rough estimate: 100 calories per mile
    return (stats.total_distance_mi * 100).toLocaleString()
  }

  if (loading) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        <div className="page-header">
          <h1 className="page-title">Analytics 📊</h1>
          <p className="page-subtitle">Deep dive into your training data</p>
        </div>
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>⏳</div>
          <p>Loading analytics...</p>
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
          <h1 className="page-title">Analytics 📊</h1>
          <p className="page-subtitle">Deep dive into your training data</p>
        </div>
        <div className="card" style={{ background: 'rgba(255, 107, 157, 0.1)', border: '1px solid var(--accent-secondary)' }}>
          <h3 style={{ color: 'var(--accent-secondary)', marginBottom: '1rem' }}>Error Loading Analytics</h3>
          <p>{error}</p>
        </div>
      </motion.div>
    )
  }

  const metrics = calculateMetrics()

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.4 }}
    >
      <div style={{ marginBottom: '1.5rem' }}>
        <h1 className="page-title">Analytics 📊</h1>
        <p className="page-subtitle">
          Deep dive into your training data • {stats?.total_runs} runs analyzed
        </p>
      </div>

      {/* Popular Training Metrics */}
      <div style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: '700', marginBottom: '1rem', color: 'var(--accent-primary)' }}>
          🎯 Core Training Metrics
        </h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
          {/* Training Consistency */}
          <div className="card" style={{ background: 'rgba(0, 245, 212, 0.05)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
              <h3 style={{ fontSize: '0.875rem', fontWeight: '600', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Training Consistency
              </h3>
              <span style={{ fontSize: '1.5rem' }}>📅</span>
            </div>
            <div style={{ fontSize: '2.5rem', fontWeight: '700', color: 'var(--accent-primary)', marginBottom: '0.5rem' }}>
              {metrics?.consistency}%
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              Months with activity
            </p>
          </div>

          {/* Average Weekly Distance */}
          <div className="card" style={{ background: 'rgba(0, 245, 212, 0.05)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
              <h3 style={{ fontSize: '0.875rem', fontWeight: '600', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Avg Weekly Distance
              </h3>
              <span style={{ fontSize: '1.5rem' }}>📏</span>
            </div>
            <div style={{ fontSize: '2.5rem', fontWeight: '700', color: 'var(--accent-primary)', marginBottom: '0.5rem' }}>
              {metrics?.avgWeeklyDistance}
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              Miles per week
            </p>
          </div>

          {/* Preferred Running Time */}
          <div className="card" style={{ background: 'rgba(0, 245, 212, 0.05)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
              <h3 style={{ fontSize: '0.875rem', fontWeight: '600', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Favorite Run Time
              </h3>
              <span style={{ fontSize: '1.5rem' }}>🕐</span>
            </div>
            <div style={{ fontSize: '2.5rem', fontWeight: '700', color: 'var(--accent-primary)', marginBottom: '0.5rem' }}>
              {metrics?.preferredTime}
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              Most runs at this hour
            </p>
          </div>

          {/* Preferred Running Day */}
          <div className="card" style={{ background: 'rgba(0, 245, 212, 0.05)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
              <h3 style={{ fontSize: '0.875rem', fontWeight: '600', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Favorite Run Day
              </h3>
              <span style={{ fontSize: '1.5rem' }}>📆</span>
            </div>
            <div style={{ fontSize: '2.5rem', fontWeight: '700', color: 'var(--accent-primary)', marginBottom: '0.5rem' }}>
              {metrics?.preferredDay}
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              Most active day
            </p>
          </div>

          {/* Total Vertical Gain */}
          <div className="card" style={{ background: 'rgba(0, 245, 212, 0.05)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
              <h3 style={{ fontSize: '0.875rem', fontWeight: '600', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Total Elevation
              </h3>
              <span style={{ fontSize: '1.5rem' }}>⛰️</span>
            </div>
            <div style={{ fontSize: '2.5rem', fontWeight: '700', color: 'var(--accent-primary)', marginBottom: '0.5rem' }}>
              {(metrics?.verticalGainTotal / 1000).toFixed(1)}k
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              Feet climbed
            </p>
          </div>

          {/* Average Pace */}
          <div className="card" style={{ background: 'rgba(0, 245, 212, 0.05)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
              <h3 style={{ fontSize: '0.875rem', fontWeight: '600', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Average Pace
              </h3>
              <span style={{ fontSize: '1.5rem' }}>⚡</span>
            </div>
            <div style={{ fontSize: '2.5rem', fontWeight: '700', color: 'var(--accent-primary)', marginBottom: '0.5rem' }}>
              {formatPace(stats?.avg_pace)}
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              Per mile
            </p>
          </div>
        </div>
      </div>

      {/* Fun & Quirky Metrics */}
      <div style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: '700', marginBottom: '1rem', color: 'var(--accent-secondary)' }}>
          🎉 Fun Facts & Milestones
        </h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
          {/* Mount Everests Climbed */}
          <div className="card" style={{ background: 'rgba(255, 107, 157, 0.05)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
              <h3 style={{ fontSize: '0.875rem', fontWeight: '600', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Mt. Everests Climbed
              </h3>
              <span style={{ fontSize: '1.5rem' }}>🏔️</span>
            </div>
            <div style={{ fontSize: '2.5rem', fontWeight: '700', color: 'var(--accent-secondary)', marginBottom: '0.5rem' }}>
              {metrics?.mountEverestsClimbed}
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              Elevation equivalent
            </p>
          </div>

          {/* Shoe Graveyard */}
          <div className="card" style={{ background: 'rgba(255, 107, 157, 0.05)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
              <h3 style={{ fontSize: '0.875rem', fontWeight: '600', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Shoe Graveyard
              </h3>
              <span style={{ fontSize: '1.5rem' }}>👟</span>
            </div>
            <div style={{ fontSize: '2.5rem', fontWeight: '700', color: 'var(--accent-secondary)', marginBottom: '0.5rem' }}>
              {metrics?.shoeMileage}
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              Pairs retired (~400mi each)
            </p>
          </div>

          {/* Lifetime Progress */}
          <div className="card" style={{ background: 'rgba(255, 107, 157, 0.05)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
              <h3 style={{ fontSize: '0.875rem', fontWeight: '600', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Lifetime Progress
              </h3>
              <span style={{ fontSize: '1.5rem' }}>🎯</span>
            </div>
            <div style={{ fontSize: '2.5rem', fontWeight: '700', color: 'var(--accent-secondary)', marginBottom: '0.5rem' }}>
              {metrics?.lifetimeEquivalent}%
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              Of avg lifetime distance (26k mi)
            </p>
          </div>

          {/* Calories Burned */}
          <div className="card" style={{ background: 'rgba(255, 107, 157, 0.05)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
              <h3 style={{ fontSize: '0.875rem', fontWeight: '600', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Calories Burned
              </h3>
              <span style={{ fontSize: '1.5rem' }}>🔥</span>
            </div>
            <div style={{ fontSize: '2.5rem', fontWeight: '700', color: 'var(--accent-secondary)', marginBottom: '0.5rem' }}>
              {(metrics?.totalCaloriesBurned / 1000000).toFixed(1)}M
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              Est. total calories (~100/mi)
            </p>
          </div>
        </div>
      </div>

      {/* Weekly Patterns Breakdown */}
      {weeklyPatterns && (
        <div style={{ marginBottom: '2rem' }}>
          <h2 style={{ fontSize: '1.5rem', fontWeight: '700', marginBottom: '1rem', color: 'var(--accent-primary)' }}>
            📅 Weekly Patterns
          </h2>
          <div className="card">
            <h3 style={{ fontSize: '1rem', fontWeight: '600', marginBottom: '1rem' }}>Runs by Day of Week</h3>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              {Object.entries(weeklyPatterns.by_day || {}).map(([day, count]) => (
                <div
                  key={day}
                  style={{
                    flex: '1 1 120px',
                    padding: '1rem',
                    background: 'rgba(0, 245, 212, 0.05)',
                    borderRadius: '8px',
                    border: day === metrics?.preferredDay ? '2px solid var(--accent-primary)' : '1px solid rgba(0, 245, 212, 0.2)',
                    textAlign: 'center'
                  }}
                >
                  <div style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--accent-primary)', marginBottom: '0.25rem' }}>
                    {count}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                    {day}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* All-Time Records */}
      <div>
        <h2 style={{ fontSize: '1.5rem', fontWeight: '700', marginBottom: '1rem', color: 'var(--accent-primary)' }}>
          🏆 Personal Records
        </h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
          <div className="card" style={{ background: 'rgba(0, 245, 212, 0.05)' }}>
            <h3 style={{ fontSize: '0.875rem', fontWeight: '600', color: 'var(--text-secondary)', marginBottom: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Fastest Pace
            </h3>
            <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--accent-primary)' }}>
              {formatPace(stats?.best_pace)} /mi
            </div>
          </div>

          <div className="card" style={{ background: 'rgba(0, 245, 212, 0.05)' }}>
            <h3 style={{ fontSize: '0.875rem', fontWeight: '600', color: 'var(--text-secondary)', marginBottom: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Longest Run
            </h3>
            <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--accent-primary)' }}>
              {stats?.longest_run_mi} miles
            </div>
          </div>

          <div className="card" style={{ background: 'rgba(0, 245, 212, 0.05)' }}>
            <h3 style={{ fontSize: '0.875rem', fontWeight: '600', color: 'var(--text-secondary)', marginBottom: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Total Distance
            </h3>
            <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--accent-primary)' }}>
              {stats?.total_distance_mi.toLocaleString()} miles
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  )
}

export default Analytics