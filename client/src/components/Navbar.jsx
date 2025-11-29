import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useTheme } from '../context/ThemeContext'
import '../styles/navbar.css'

function Navbar() {
  const { user, logout } = useAuth()
  const { theme, toggleTheme } = useTheme()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/home" className="navbar-brand">
          Social Connect
        </Link>

        <div className="navbar-actions">
          <button onClick={toggleTheme} className="theme-toggle btn">
            {theme === 'light' ? '🌙' : '☀️'}
          </button>

          {user ? (
            <>
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
      </div>
    </nav>
  )
}

export default Navbar
