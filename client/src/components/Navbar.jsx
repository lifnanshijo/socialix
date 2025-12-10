import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useTheme } from '../context/ThemeContext'
import { useNotifications } from '../hooks/useNotifications'
import { NotificationDropdown } from './NotificationDropdown'
import SocialixLogo from './SocialixLogo'
import '../styles/navbar.css'

function Navbar() {
  const { user, logout } = useAuth()
  const { theme, toggleTheme } = useTheme()
  const { unreadCount } = useNotifications()
  const navigate = useNavigate()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [showNotifications, setShowNotifications] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/login')
    setMobileMenuOpen(false)
  }

  const handleNavClick = () => {
    setMobileMenuOpen(false)
  }

  const closeMobileMenu = () => {
    setMobileMenuOpen(false)
  }

  return (
    <>
      <nav className="navbar">
        <div className="navbar-container">
          <Link to="/home" className="navbar-brand" onClick={handleNavClick}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <SocialixLogo size={32} variant="icon" />
              <span style={{ 
                fontSize: '20px', 
                fontWeight: '700',
                background: 'linear-gradient(135deg, #00d4ff, #3366ff, #9933ff)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text'
              }}>
                Socialix
              </span>
            </div>
          </Link>

          <div className="navbar-actions">
            <button onClick={toggleTheme} className="theme-toggle btn">
              {theme === 'light' ? '🌙' : '☀️'}
            </button>

            {user ? (
              <>
                <Link to="/home" className="btn">🏠 Home</Link>
                <Link to="/search" className="btn">🔍 Search</Link>
                <Link to="/chat" className="btn">💬 Messages</Link>
                <Link to="/clips" className="btn">📸 Stories</Link>
                <Link to="/profile" className="btn">👤 Profile</Link>
                <button 
                  className="notification-bell btn" 
                  onClick={() => setShowNotifications(!showNotifications)}
                  aria-label="Notifications"
                >
                  🔔
                  {unreadCount > 0 && (
                    <span className="notification-badge">{unreadCount}</span>
                  )}
                </button>
                <button onClick={handleLogout} className="btn">Logout</button>
              </>
            ) : (
              <>
                <Link to="/login" className="btn">Login</Link>
                <Link to="/signup" className="btn btn-primary">Sign Up</Link>
              </>
            )}
          </div>

          {/* Mobile menu toggle */}
          <button
            className="mobile-nav-toggle"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle navigation menu"
          >
            {mobileMenuOpen ? '✕' : '☰'}
          </button>
        </div>
      </nav>

      {/* Mobile Navigation Drawer */}
      {user && (
        <>
          <div
            className={`mobile-nav-overlay ${mobileMenuOpen ? 'open' : ''}`}
            onClick={closeMobileMenu}
          />
          <nav className={`mobile-nav-drawer ${mobileMenuOpen ? 'open' : ''}`}>
            <Link to="/home" className="nav-item" onClick={handleNavClick}>
              🏠 Home
            </Link>
            <Link to="/chat" className="nav-item" onClick={handleNavClick}>
              💬 Messages
            </Link>
            <Link to="/clips" className="nav-item" onClick={handleNavClick}>
              📸 Stories
            </Link>
            <Link to="/profile" className="nav-item" onClick={handleNavClick}>
              👤 Profile
            </Link>
            <button
              className="nav-item"
              onClick={toggleTheme}
              style={{ textAlign: 'left', background: 'none', border: 'none', cursor: 'pointer' }}
            >
              {theme === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode'}
            </button>
            <button
              className="nav-item"
              onClick={handleLogout}
              style={{ textAlign: 'left', background: 'none', border: 'none', cursor: 'pointer', color: '#e41e3f' }}
            >
              🚪 Logout
            </button>
          </nav>
        </>
      )}
      
      <NotificationDropdown 
        show={showNotifications} 
        onClose={() => setShowNotifications(false)} 
      />
    </>
  )
}

export default Navbar
