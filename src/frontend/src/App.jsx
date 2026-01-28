import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Home, TrendingUp, Map, BarChart3, Trophy, Bot } from 'lucide-react'
import Dashboard from './pages/Dashboard'
import Analytics from './pages/Analytics'
import Heatmap from './pages/Heatmap'
import Timeline from './pages/Timeline'
import Coach from './pages/Coach'
import './App.css'

function NavBar() {
  const location = useLocation()

  const navItems = [
    { path: '/', icon: Home, label: 'Home' },
    { path: '/analytics', icon: BarChart3, label: 'Analytics' },
    { path: '/heatmap', icon: Map, label: 'Heatmap' },
    { path: '/timeline', icon: TrendingUp, label: 'Timeline' },
    { path: '/coach', icon: Bot, label: 'Coach' },
  ]

  return (
    <nav className="nav-bar">
      <div className="nav-container">
        <div className="nav-brand">
          <Trophy className="brand-icon" />
          <span className="brand-text">Louis Sader RunMetrics</span>
        </div>

        <div className="nav-links">
          {navItems.map(({ path, icon: Icon, label }) => (
            <Link
              key={path}
              to={path}
              className={`nav-link ${location.pathname === path ? 'active' : ''}`}
            >
              <Icon size={20} />
              <span>{label}</span>
            </Link>
          ))}
        </div>
      </div>
    </nav>
  )
}

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '50px', background: 'white', color: 'black' }}>
          <h1>Something went wrong!</h1>
          <pre>{this.state.error?.toString()}</pre>
        </div>
      )
    }
    return this.props.children
  }
}

function App() {
  const [stats, setStats] = useState(null)

  useEffect(() => {
    fetch('http://localhost:5001/api/stats')
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(err => console.error('Error loading stats:', err))
  }, [])

  return (
    <ErrorBoundary>
      <Router>
        <div className="app">
          <NavBar />

          <main className="main-content">
            <AnimatePresence mode="wait">
              <Routes>
                <Route path="/" element={<Dashboard stats={stats} />} />
                <Route path="/analytics" element={<Analytics />} />
                <Route path="/heatmap" element={<Heatmap />} />
                <Route path="/timeline" element={<Timeline />} />
                <Route path="/coach" element={<Coach />} />
              </Routes>
            </AnimatePresence>
          </main>

          <footer className="app-footer">
            <p>Made with ❤️ for runners | Data from Strava</p>
          </footer>
        </div>
      </Router>
    </ErrorBoundary>
  )
}

export default App
