import React, { useState, useEffect } from 'react'
import { useTheme } from '../context/ThemeContext'
import '../styles/splash.css'

function SplashScreen({ onComplete }) {
  const [isExiting, setIsExiting] = useState(false)
  const { theme } = useTheme()

  useEffect(() => {
    // Auto-exit splash screen after 3 seconds
    const timer = setTimeout(() => {
      setIsExiting(true)
      setTimeout(() => {
        onComplete()
      }, 300)
    }, 3000)

    return () => clearTimeout(timer)
  }, [onComplete])

  return (
    <div className={`splash-screen ${isExiting ? 'splash-exit' : ''} ${theme === 'light' ? 'light-mode' : ''}`}>
      {/* Tech Mesh Background */}
      <div className="splash-background">
        {/* Animated Particles */}
        <div className="particle-container">
          <div className="particle p1"></div>
          <div className="particle p2"></div>
          <div className="particle p3"></div>
          <div className="particle p4"></div>
          <div className="particle p5"></div>
          <div className="particle p6"></div>
          <div className="particle p7"></div>
          <div className="particle p8"></div>
        </div>

        <svg className="mesh-bg" viewBox="0 0 500 500" preserveAspectRatio="xMidYMid slice">
          <defs>
            <linearGradient id="meshGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#23C7FF" stopOpacity="0.08" />
              <stop offset="50%" stopColor="#8A4BFF" stopOpacity="0.06" />
              <stop offset="100%" stopColor="#D24EFF" stopOpacity="0.08" />
            </linearGradient>
            <filter id="meshGlow">
              <feGaussianBlur stdDeviation="1" result="coloredBlur" />
              <feMerge>
                <feMergeNode in="coloredBlur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          {/* Grid lines */}
          <g className="mesh-lines" opacity="0.12">
            {[...Array(10)].map((_, i) => (
              <line key={`v${i}`} x1={i * 50} y1="0" x2={i * 50} y2="500" stroke="url(#meshGradient)" strokeWidth="0.5" />
            ))}
            {[...Array(10)].map((_, i) => (
              <line key={`h${i}`} x1="0" y1={i * 50} x2="500" y2={i * 50} stroke="url(#meshGradient)" strokeWidth="0.5" />
            ))}
          </g>

          {/* Network nodes */}
          <circle cx="100" cy="100" r="2" fill="#23C7FF" opacity="0.5" className="mesh-node" filter="url(#meshGlow)" />
          <circle cx="400" cy="100" r="2" fill="#3BF3F7" opacity="0.5" className="mesh-node" filter="url(#meshGlow)" />
          <circle cx="250" cy="250" r="2" fill="#8A4BFF" opacity="0.5" className="mesh-node" filter="url(#meshGlow)" />
          <circle cx="100" cy="400" r="2" fill="#D24EFF" opacity="0.5" className="mesh-node" filter="url(#meshGlow)" />
          <circle cx="400" cy="400" r="2" fill="#23C7FF" opacity="0.5" className="mesh-node" filter="url(#meshGlow)" />
        </svg>
      </div>

      {/* Main Content */}
      <div className="splash-content">
        {/* X-Symbol Container */}
        <div className="orb-container">

          {/* X-Symbol */}
          <svg
            className="logo-x"
            viewBox="0 0 400 400"
            width="140"
            height="140"
            xmlns="http://www.w3.org/2000/svg"
            style={{ position: 'absolute', zIndex: 2 }}
          >
            <defs>
              <linearGradient id="xGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#23C7FF" />
                <stop offset="25%" stopColor="#3BF3F7" />
                <stop offset="75%" stopColor="#8A4BFF" />
                <stop offset="100%" stopColor="#D24EFF" />
              </linearGradient>
              <filter id="xGlow">
                <feGaussianBlur stdDeviation="2" result="coloredBlur" />
                <feMerge>
                  <feMergeNode in="coloredBlur" />
                  <feMergeNode in="SourceGraphic" />
                </feMerge>
              </filter>
            </defs>

            {/* X symbol - modern bold design */}
            <g filter="url(#xGlow)" className="x-symbol">
              {/* First diagonal - modern bold stroke */}
              <line x1="100" y1="100" x2="300" y2="300" stroke="url(#xGradient)" strokeWidth="36" strokeLinecap="round" strokeLinejoin="round" />
              
              {/* Second diagonal - modern bold stroke */}
              <line x1="300" y1="100" x2="100" y2="300" stroke="url(#xGradient)" strokeWidth="36" strokeLinecap="round" strokeLinejoin="round" />
            </g>
          </svg>
        </div>

        {/* Brand Text */}
        <div className="splash-text">
          <h1 className="splash-title">SocialX</h1>
          <p className="splash-subtitle">Connect. Create. Inspire.</p>
        </div>
      </div>

      {/* Loading Indicator */}
      <div className="splash-loader">
        <div className="loader-dot"></div>
        <div className="loader-dot"></div>
        <div className="loader-dot"></div>
      </div>
    </div>
  )
}

export default SplashScreen
