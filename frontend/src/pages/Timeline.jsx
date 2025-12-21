import { motion } from 'framer-motion'

function Timeline() {
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
        <p>Timeline page coming soon!</p>
      </div>
    </motion.div>
  )
}

export default Timeline
