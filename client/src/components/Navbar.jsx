import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useTheme } from '../context/ThemeContext'
import '../styles/navbar.css'

function Navbar() {
  const { user, logout } = useAuth()
  const { theme, toggleTheme } = useTheme()
  const navigate = useNavigate()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

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
            Social Connect
          </Link>

          <div className="navbar-actions">
            <button onClick={toggleTheme} className="theme-toggle btn">
              {theme === 'light' ? '🌙' : '☀️'}
            </button>

            {user ? (
              <>
                <Link to="/home" className="btn">Home</Link>
                <Link to="/chat" className="btn">Messages</Link>
                <Link to="/profile" className="btn">Profile</Link>
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

          {user ? (
            <>
              <Link to="/home" className="btn">🏠 Home</Link>
              <Link to="/search" className="btn">🔍 Search</Link>
              <Link to="/chat" className="btn">💬 Messages</Link>
              <Link to="/profile" className="btn">👤 Profile</Link>
              <button onClick={handleLogout} className="btn">Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn">Login</Link>
              <Link to="/signup" className="btn btn-primary">Sign Up</Link>
            </>
          )}
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
    </>
  )
}

export default Navbar
