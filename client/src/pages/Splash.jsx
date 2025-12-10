import React, { useEffect, useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import '../styles/Splash.css'

function Splash() {
  const navigate = useNavigate()
  const location = useLocation()
  const { isAuthenticated, loading } = useAuth()
  const [showSplash, setShowSplash] = useState(true)
  const [hasShownOnce, setHasShownOnce] = useState(false)

  useEffect(() => {
    // Only show splash screen on the very first load (at root path)
    if (location.pathname !== '/' || hasShownOnce) {
      setShowSplash(false)
      return
    }

    if (!loading) {
      const timer = setTimeout(() => {
        setShowSplash(false)
        setHasShownOnce(true)
        if (isAuthenticated) {
          navigate('/home')
        } else {
          navigate('/login')
        }
      }, 2500)

      return () => clearTimeout(timer)
    }
  }, [loading, isAuthenticated, navigate, location.pathname, hasShownOnce])

  if (!showSplash) return null

  return (
    <div className="splash-screen">
      <div className="splash-content">
        <div className="splash-logo-container">
          <div className="logo-sx">
            <span className="logo-s">S</span>
            <span className="logo-x">X</span>
          </div>
        </div>
        <h1 className="splash-text">Socialix</h1>
        <p className="splash-subtitle">Social Connect Platform</p>
        <div className="splash-loader"></div>
      </div>
    </div>
  )
}

export default Splash
