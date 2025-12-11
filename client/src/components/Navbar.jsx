import React, { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useTheme } from '../context/ThemeContext'
import { useNotifications } from '../hooks/useNotifications'
import { Home, Search, MessageSquare, Camera, User, Moon, Sun, LogOut, LogIn, Menu, X, Bell } from 'lucide-react'
import '../styles/navbar.css'
import '../styles/sidebar.css'

function Navbar() {
  const { user, logout } = useAuth()
  const { theme, toggleTheme } = useTheme()
  const { unreadCount } = useNotifications()
  const navigate = useNavigate()
  const location = useLocation()
  const [sidebarOpen, setSidebarOpen] = useState(false)

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
          <button 
            className="navbar-menu-toggle"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            aria-label="Toggle menu"
          >
            {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
          </button>

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
                <Link 
                  to="/notifications" 
                  className={`flex items-center justify-center w-11 h-11 rounded-lg transition-all duration-200 relative ${
                    isActive('/notifications') 
                      ? 'text-cyan-400 shadow-lg shadow-cyan-500/50' 
                      : 'text-gray-400 hover:text-cyan-400'
                  }`}
                  title="Notifications"
                >
                  <Bell size={20} strokeWidth={2} />
                  {unreadCount > 0 && (
                    <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
                      {unreadCount > 9 ? '9+' : unreadCount}
                    </span>
                  )}
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

      {sidebarOpen && <div className="sidebar-overlay" onClick={() => setSidebarOpen(false)} />}

      {/* Sidebar Dropdown Menu */}
      <aside className={`sidebar-dropdown ${sidebarOpen ? 'open' : ''}`}>
        {/* Sidebar Header */}
        <div className="sidebar-header">
          <h2>SocialX</h2>
          <button
            className="sidebar-close-btn"
            onClick={() => setSidebarOpen(false)}
            aria-label="Close sidebar"
          >
            <X size={24} />
          </button>
        </div>

        {/* Main Navigation Section */}
        <nav className="sidebar-section">
          <div className="sidebar-section-title">Navigation</div>

          <Link
            to="/home"
            className={`sidebar-item ${isActive('/home') ? 'active' : ''}`}
            onClick={() => setSidebarOpen(false)}
            title="Home"
          >
            <Home size={20} strokeWidth={2} />
            <span>Home</span>
          </Link>

          <Link
            to="/search"
            className={`sidebar-item ${isActive('/search') ? 'active' : ''}`}
            onClick={() => setSidebarOpen(false)}
            title="Search"
          >
            <Search size={20} strokeWidth={2} />
            <span>Search</span>
          </Link>

          <Link
            to="/chat"
            className={`sidebar-item ${isActive('/chat') ? 'active' : ''}`}
            onClick={() => setSidebarOpen(false)}
            title="Messages"
          >
            <MessageSquare size={20} strokeWidth={2} />
            <span>Messages</span>
          </Link>

          <Link
            to="/clips"
            className={`sidebar-item ${isActive('/clips') ? 'active' : ''}`}
            onClick={() => setSidebarOpen(false)}
            title="Stories"
          >
            <Camera size={20} strokeWidth={2} />
            <span>Stories</span>
          </Link>

          <Link
            to="/notifications"
            className={`sidebar-item ${isActive('/notifications') ? 'active' : ''}`}
            onClick={() => setSidebarOpen(false)}
            title="Notifications"
          >
            <div className="relative inline-block">
              <Bell size={20} strokeWidth={2} />
              {unreadCount > 0 && (
                <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full w-4 h-4 flex items-center justify-center" style={{fontSize: '10px'}}>
                  {unreadCount > 9 ? '9+' : unreadCount}
                </span>
              )}
            </div>
            <span>Notifications {unreadCount > 0 && `(${unreadCount})`}</span>
          </Link>

          {user && (
            <Link
              to="/profile"
              className={`sidebar-item ${isActive('/profile') ? 'active' : ''}`}
              onClick={() => setSidebarOpen(false)}
              title="Profile"
            >
              <User size={20} strokeWidth={2} />
              <span>Profile</span>
            </Link>
          )}
        </nav>

        {/* Divider */}
        <div className="sidebar-divider" />

        {/* Settings Section */}
        <div className="sidebar-section">
          <div className="sidebar-section-title">Settings</div>

          <button
            className="sidebar-item theme-item"
            onClick={() => {
              toggleTheme()
              setSidebarOpen(false)
            }}
            title={theme === 'light' ? 'Dark Mode' : 'Light Mode'}
          >
            {theme === 'light' ? (
              <Moon size={20} strokeWidth={2} />
            ) : (
              <Sun size={20} strokeWidth={2} />
            )}
            <span>{theme === 'light' ? 'Dark Mode' : 'Light Mode'}</span>
          </button>

          {user ? (
            <button
              className="sidebar-item logout-item"
              onClick={() => {
                handleLogout()
                setSidebarOpen(false)
              }}
              title="Logout"
            >
              <LogOut size={20} strokeWidth={2} />
              <span>Logout</span>
            </button>
          ) : (
            <Link
              to="/login"
              className="sidebar-item login-item"
              onClick={() => setSidebarOpen(false)}
              title="Login"
            >
              <LogIn size={20} strokeWidth={2} />
              <span>Login</span>
            </Link>
          )}
        </div>
      </aside>
    </>
  )
}

export default Navbar
