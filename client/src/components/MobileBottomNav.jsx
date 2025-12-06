import React from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import '../styles/mobile-bottom-nav.css'

function MobileBottomNav() {
  const location = useLocation()
  const navigate = useNavigate()
  const { user } = useAuth()

  // Only show on mobile
  if (!user) return null

  const isActive = (path) => location.pathname === path

  const navItems = [
    { path: '/home', label: 'Home', icon: '🏠' },
    { path: '/chat', label: 'Messages', icon: '💬' },
    { path: '/clips', label: 'Stories', icon: '📸' },
    { path: '/profile', label: 'Profile', icon: '👤' },
  ]

  return (
    <nav className="mobile-bottom-nav">
      <div className="bottom-nav-container">
        {navItems.map((item) => (
          <button
            key={item.path}
            className={`bottom-nav-item ${isActive(item.path) ? 'active' : ''}`}
            onClick={() => navigate(item.path)}
            aria-label={item.label}
          >
            <span className="icon">{item.icon}</span>
            <span className="label">{item.label}</span>
          </button>
        ))}
      </div>
    </nav>
  )
}

export default MobileBottomNav
