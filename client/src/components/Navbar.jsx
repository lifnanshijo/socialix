import React, { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useTheme } from '../context/ThemeContext'
import { useNotifications } from '../hooks/useNotifications'
import { NotificationDropdown } from './NotificationDropdown'
import { Home, Search, MessageSquare, Camera, User, Moon, Sun, LogOut, LogIn } from 'lucide-react'
import '../styles/navbar.css'

function Navbar() {
  const { user, logout } = useAuth()
  const { theme, toggleTheme } = useTheme()
  const { unreadCount } = useNotifications()
  const navigate = useNavigate()
  const location = useLocation()
  const [showNotifications, setShowNotifications] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const isActive = (path) => {
    return location.pathname === path || location.pathname.startsWith(path + '/')
  }

  return (
    <>
      <nav className="navbar">
        <div className="navbar-container">
          <Link to="/home" className="navbar-brand">
            {/* Brand Logo with X-Symbol and Text */}
            <div className="brand-logo">
              {/* X-Symbol SVG */}
              <svg
                className="brand-x-icon"
                viewBox="0 0 400 400"
                width="32"
                height="32"
                xmlns="http://www.w3.org/2000/svg"
              >
                <defs>
                  <linearGradient id="navXGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#23C7FF" />
                    <stop offset="25%" stopColor="#3BF3F7" />
                    <stop offset="75%" stopColor="#8A4BFF" />
                    <stop offset="100%" stopColor="#D24EFF" />
                  </linearGradient>
                  <filter id="navXGlow">
                    <feGaussianBlur stdDeviation="1.5" result="coloredBlur" />
                    <feMerge>
                      <feMergeNode in="coloredBlur" />
                      <feMergeNode in="SourceGraphic" />
                    </feMerge>
                  </filter>
                </defs>
                {/* X - modern bold design */}
                <g className="x-symbol" filter="url(#navXGlow)">
                  {/* First diagonal - modern bold stroke */}
                  <line x1="100" y1="100" x2="300" y2="300" stroke="url(#navXGradient)" strokeWidth="36" strokeLinecap="round" strokeLinejoin="round" />
                  
                  {/* Second diagonal - modern bold stroke */}
                  <line x1="300" y1="100" x2="100" y2="300" stroke="url(#navXGradient)" strokeWidth="36" strokeLinecap="round" strokeLinejoin="round" />
                </g>
              </svg>

              {/* Brand Text */}
              <span className="brand-text">SocialX</span>
            </div>
          </Link>

          <div className="navbar-actions">
            {user && (
              <div className="flex items-center gap-6">
                <Link 
                  to="/home" 
                  className={`flex items-center justify-center w-11 h-11 rounded-lg transition-all duration-200 ${
                    isActive('/home') 
                      ? 'text-cyan-400 shadow-lg shadow-cyan-500/50' 
                      : 'text-gray-400 hover:text-cyan-400'
                  }`}
                  title="Home"
                >
                  <Home size={20} strokeWidth={2} />
                </Link>
                <Link 
                  to="/search" 
                  className={`flex items-center justify-center w-11 h-11 rounded-lg transition-all duration-200 ${
                    isActive('/search') 
                      ? 'text-cyan-400 shadow-lg shadow-cyan-500/50' 
                      : 'text-gray-400 hover:text-cyan-400'
                  }`}
                  title="Search"
                >
                  <Search size={20} strokeWidth={2} />
                </Link>
                <Link 
                  to="/chat" 
                  className={`flex items-center justify-center w-11 h-11 rounded-lg transition-all duration-200 ${
                    isActive('/chat') 
                      ? 'text-cyan-400 shadow-lg shadow-cyan-500/50' 
                      : 'text-gray-400 hover:text-cyan-400'
                  }`}
                  title="Messages"
                >
                  <MessageSquare size={20} strokeWidth={2} />
                </Link>
                <Link 
                  to="/clips" 
                  className={`flex items-center justify-center w-11 h-11 rounded-lg transition-all duration-200 ${
                    isActive('/clips') 
                      ? 'text-cyan-400 shadow-lg shadow-cyan-500/50' 
                      : 'text-gray-400 hover:text-cyan-400'
                  }`}
                  title="Stories"
                >
                  <Camera size={20} strokeWidth={2} />
                </Link>
              </div>
            )}
            {!user && (
              <>
                <Link to="/login" className="btn">Login</Link>
                <Link to="/signup" className="btn btn-primary">Sign Up</Link>
              </>
            )}
          </div>
        </div>
      </nav>

      <NotificationDropdown 
        show={showNotifications} 
        onClose={() => setShowNotifications(false)} 
      />
    </>
  )
}

export default Navbar
