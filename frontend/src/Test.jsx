import React from 'react'

function Test() {
  return (
    <div style={{ padding: '2rem', background: '#0a0e27', color: 'white', minHeight: '100vh', fontFamily: 'sans-serif' }}>
      <h1 style={{ color: '#00f5d4', fontSize: '3rem' }}>✅ React is Working!</h1>
      <p style={{ fontSize: '1.5rem', marginTop: '2rem' }}>
        If you see this, React is rendering successfully.
      </p>
      <div style={{ marginTop: '2rem', padding: '1.5rem', background: '#1a1f3a', borderRadius: '12px', border: '2px solid #00f5d4' }}>
        <p>✅ Vite dev server: Running</p>
        <p>✅ React: Loaded</p>
        <p>✅ JSX: Compiling</p>
        <p>Now checking API connection...</p>
      </div>
    </div>
  )
}

export default Test
