import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import '../styles/Splash.css'

function Splash() {
  const navigate = useNavigate()
  const { isAuthenticated, loading } = useAuth()
  const [showSplash, setShowSplash] = useState(true)

  useEffect(() => {
    if (!loading) {
      const timer = setTimeout(() => {
        setShowSplash(false)
        if (isAuthenticated) {
          navigate('/home')
        } else {
          navigate('/login')
        }
      }, 2500)

      return () => clearTimeout(timer)
    }
  }, [loading, isAuthenticated, navigate])

  if (!showSplash) return null

  return (
    <div className="splash-screen">
      <div className="splash-content">
        <div className="splash-logo">Social Connect</div>
        <div className="splash-loader"></div>
      </div>
    </div>
  )
}

export default Splash
