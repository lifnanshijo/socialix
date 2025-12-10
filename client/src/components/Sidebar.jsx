import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useTheme } from '../context/ThemeContext'
import { useNotifications } from '../hooks/useNotifications'
import {
  Home,
  Search,
  MessageSquare,
  Camera,
  User,
  Bell,
  Moon,
  Sun,
  LogOut,
  LogIn,
  Menu,
  X,
} from 'lucide-react'
import '../styles/sidebar.css'

function Sidebar() {
  const { user, logout } = useAuth()
  const { theme, toggleTheme } = useTheme()
  const { unreadCount } = useNotifications()
  const location = useLocation()
  const [isOpen, setIsOpen] = useState(false)

  const isActive = (path) => {
    return location.pathname === path || location.pathname.startsWith(path + '/')
  }

  const handleNavClick = () => {
    setIsOpen(false)
  }

  const handleLogout = () => {
    logout()
    setIsOpen(false)
  }

  return (
    <>
      {/* Sidebar Toggle Button (Icon-based) */}
      <button
        className="sidebar-toggle-icon"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle sidebar menu"
        title="Menu"
      >
        {isOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Sidebar Overlay */}
      {isOpen && <div className="sidebar-overlay" onClick={() => setIsOpen(false)} />}

      {/* Sidebar Dropdown Menu */}
      <aside className={`sidebar-dropdown ${isOpen ? 'open' : ''}`}>
        {/* Sidebar Header */}
        <div className="sidebar-header">
          <h2>SocialX</h2>
          <button
            className="sidebar-close-btn"
            onClick={() => setIsOpen(false)}
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
            onClick={handleNavClick}
            title="Home"
          >
            <Home size={20} strokeWidth={2} />
            <span>Home</span>
          </Link>

          <Link
            to="/search"
            className={`sidebar-item ${isActive('/search') ? 'active' : ''}`}
            onClick={handleNavClick}
            title="Search"
          >
            <Search size={20} strokeWidth={2} />
            <span>Search</span>
          </Link>

          <Link
            to="/chat"
            className={`sidebar-item ${isActive('/chat') ? 'active' : ''}`}
            onClick={handleNavClick}
            title="Messages"
          >
            <MessageSquare size={20} strokeWidth={2} />
            <span>Messages</span>
          </Link>

          <Link
            to="/clips"
            className={`sidebar-item ${isActive('/clips') ? 'active' : ''}`}
            onClick={handleNavClick}
            title="Stories"
          >
            <Camera size={20} strokeWidth={2} />
            <span>Stories</span>
          </Link>

          {user && (
            <Link
              to="/profile"
              className={`sidebar-item ${isActive('/profile') ? 'active' : ''}`}
              onClick={handleNavClick}
              title="Profile"
            >
              <User size={20} strokeWidth={2} />
              <span>Profile</span>
            </Link>
          )}

          {user && (
            <Link
              to="/notifications"
              className={`sidebar-item ${isActive('/notifications') ? 'active' : ''}`}
              onClick={handleNavClick}
              title="Notifications"
            >
              <div className="notification-icon-wrapper">
                <Bell size={20} strokeWidth={2} />
                {unreadCount > 0 && (
                  <span className="notification-badge">{unreadCount}</span>
                )}
              </div>
              <span>Notifications</span>
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
              handleNavClick()
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
              onClick={handleLogout}
              title="Logout"
            >
              <LogOut size={20} strokeWidth={2} />
              <span>Logout</span>
            </button>
          ) : (
            <Link
              to="/login"
              className="sidebar-item login-item"
              onClick={handleNavClick}
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

export default Sidebar
