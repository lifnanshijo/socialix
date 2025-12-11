import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useNotifications } from '../hooks/useNotifications'
import '../styles/notifications-page.css'

function Notifications() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [filter, setFilter] = useState('all') // all, unread, message, follow, like, comment
  const {
    notifications,
    loading,
    error,
    fetchNotifications,
    markAsRead,
    markAllAsRead,
    deleteNotification
  } = useNotifications()

  useEffect(() => {
    fetchNotifications()
  }, [])

  const handleNotificationClick = (notification) => {
    markAsRead(notification.id)
    
    // Navigate based on notification type
    if (notification.type === 'message' && notification.reference_id) {
      navigate('/chat')
    } else if (notification.type === 'follow') {
      navigate(`/profile/${notification.sender_id}`)
    } else if (notification.type === 'like' || notification.type === 'comment') {
      navigate('/home')
      setTimeout(() => {
        const postElement = document.getElementById(`post-${notification.reference_id}`)
        if (postElement) {
          postElement.scrollIntoView({ behavior: 'smooth', block: 'center' })
          postElement.classList.add('highlight-post')
          setTimeout(() => postElement.classList.remove('highlight-post'), 2000)
        }
      }, 500)
    }
  }

  const handleDelete = (notificationId) => {
    if (window.confirm('Delete this notification?')) {
      deleteNotification(notificationId)
    }
  }

  const formatTime = (timestamp) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diffInSeconds = Math.floor((now - date) / 1000)
    
    if (diffInSeconds < 60) return 'Just now'
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`
    if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)}d ago`
    return date.toLocaleDateString()
  }

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'message': return '💬'
      case 'follow': return '👤'
      case 'like': return '❤️'
      case 'comment': return '💭'
      default: return '🔔'
    }
  }

  const getNotificationColor = (type) => {
    switch (type) {
      case 'message': return '#3b82f6'
      case 'follow': return '#8b5cf6'
      case 'like': return '#ef4444'
      case 'comment': return '#10b981'
      default: return '#6b7280'
    }
  }

  const filteredNotifications = notifications.filter(n => {
    if (filter === 'all') return true
    if (filter === 'unread') return !n.is_read
    return n.type === filter
  })

  const unreadCount = notifications.filter(n => !n.is_read).length

  return (
    <div className="notifications-page">
      <div className="notifications-header">
        <h1>🔔 Notifications</h1>
        {unreadCount > 0 && (
          <span className="unread-badge">{unreadCount} unread</span>
        )}
      </div>

      <div className="notifications-actions">
        <div className="notification-filters">
          <button 
            className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
            onClick={() => setFilter('all')}
          >
            All
          </button>
          <button 
            className={`filter-btn ${filter === 'unread' ? 'active' : ''}`}
            onClick={() => setFilter('unread')}
          >
            Unread
          </button>
          <button 
            className={`filter-btn ${filter === 'message' ? 'active' : ''}`}
            onClick={() => setFilter('message')}
          >
            💬 Messages
          </button>
          <button 
            className={`filter-btn ${filter === 'follow' ? 'active' : ''}`}
            onClick={() => setFilter('follow')}
          >
            👤 Follows
          </button>
          <button 
            className={`filter-btn ${filter === 'like' ? 'active' : ''}`}
            onClick={() => setFilter('like')}
          >
            ❤️ Likes
          </button>
          <button 
            className={`filter-btn ${filter === 'comment' ? 'active' : ''}`}
            onClick={() => setFilter('comment')}
          >
            💭 Comments
          </button>
        </div>

        {unreadCount > 0 && (
          <button className="mark-all-btn" onClick={markAllAsRead}>
            Mark all as read
          </button>
        )}
      </div>

      <div className="notifications-content">
        {loading ? (
          <div className="notifications-loading">
            <div className="spinner"></div>
            <p>Loading notifications...</p>
          </div>
        ) : error ? (
          <div className="notifications-error">
            <p>❌ {error}</p>
            <button onClick={fetchNotifications}>Retry</button>
          </div>
        ) : filteredNotifications.length === 0 ? (
          <div className="notifications-empty">
            <div className="empty-icon">🔔</div>
            <h3>No notifications</h3>
            <p>
              {filter === 'unread' 
                ? "You're all caught up!" 
                : filter === 'all'
                ? "You don't have any notifications yet"
                : `No ${filter} notifications`}
            </p>
          </div>
        ) : (
          <div className="notifications-list">
            {filteredNotifications.map(notification => (
              <div
                key={notification.id}
                className={`notification-card ${notification.is_read ? 'read' : 'unread'}`}
                onClick={() => handleNotificationClick(notification)}
              >
                <div 
                  className="notification-icon-circle"
                  style={{ backgroundColor: getNotificationColor(notification.type) }}
                >
                  {getNotificationIcon(notification.type)}
                </div>

                <div className="notification-body">
                  <div className="notification-header-text">
                    <strong>{notification.sender_username}</strong>
                    <span className="notification-action">
                      {notification.type === 'message' && ' sent you a message'}
                      {notification.type === 'follow' && ' started following you'}
                      {notification.type === 'like' && ' liked your post'}
                      {notification.type === 'comment' && ' commented on your post'}
                    </span>
                  </div>

                  {notification.content && (
                    <div className="notification-content-text">
                      {notification.content}
                    </div>
                  )}

                  <div className="notification-footer">
                    <span className="notification-time">
                      {formatTime(notification.created_at)}
                    </span>
                    {!notification.is_read && (
                      <span className="unread-dot">●</span>
                    )}
                  </div>
                </div>

                <button
                  className="notification-delete-btn"
                  onClick={(e) => {
                    e.stopPropagation()
                    handleDelete(notification.id)
                  }}
                  aria-label="Delete notification"
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default Notifications
