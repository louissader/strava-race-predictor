import React from 'react'
import { motion } from 'framer-motion'

function Analytics() {
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
      <div className="card">
        <p>Analytics page coming soon with interactive Recharts visualizations!</p>
      </div>
    </motion.div>
  )
}

export default Analytics
