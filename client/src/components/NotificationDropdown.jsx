import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useNotifications } from '../hooks/useNotifications'
import '../styles/notifications.css'

export function NotificationDropdown({ show, onClose }) {
  const navigate = useNavigate()
  const { 
    notifications, 
    loading, 
    fetchNotifications, 
    markAsRead, 
    markAllAsRead, 
    deleteNotification 
  } = useNotifications()

  React.useEffect(() => {
    if (show) {
      console.log('Dropdown opened, fetching notifications...')
      fetchNotifications().then(data => {
        console.log('Fetched notifications:', data)
      })
    }
  }, [show])

  const handleNotificationClick = (notification) => {
    markAsRead(notification.id)
    
    // Navigate based on notification type
    if (notification.type === 'message' && notification.reference_id) {
      navigate('/chat')
    } else if (notification.type === 'follow') {
      navigate(`/profile/${notification.sender_id}`)
    } else if (notification.type === 'like' || notification.type === 'comment') {
      // Navigate to home page where the post is visible
      navigate('/home')
      // Optionally scroll to the specific post if reference_id is available
      if (notification.reference_id) {
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
    
    onClose()
  }

  const handleDelete = (e, notificationId) => {
    e.stopPropagation()
    deleteNotification(notificationId)
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

  if (!show) return null

  return (
    <>
      <div className="notification-overlay" onClick={onClose} />
      <div className="notification-dropdown">
        <div className="notification-header">
          <h3>Notifications</h3>
          {notifications.length > 0 && (
            <button 
              className="mark-all-read-btn"
              onClick={markAllAsRead}
            >
              Mark all as read
            </button>
          )}
        </div>

        <div className="notification-list">
          {loading ? (
            <div className="notification-loading">Loading...</div>
          ) : notifications.length === 0 ? (
            <div className="notification-empty">
              <p>🔔 No notifications yet</p>
              <small style={{color: 'var(--text-secondary)', fontSize: '0.85rem'}}>
                {loading ? 'Loading...' : 'Notifications array is empty'}
              </small>
            </div>
          ) : (
            notifications.map(notification => {
              console.log('Rendering notification:', notification)
              return (
                <div
                  key={notification.id}
                  className={`notification-item ${notification.is_read ? 'read' : 'unread'}`}
                  onClick={() => handleNotificationClick(notification)}
                >
                  <div className="notification-icon">
                    {getNotificationIcon(notification.type)}
                  </div>
                  <div className="notification-content">
                    <div className="notification-text">
                      <strong>{notification.sender_username}</strong>
                      <span className="notification-message">
                        {notification.type === 'message' && ' sent you a message'}
                        {notification.type === 'follow' && ' started following you'}
                        {notification.type === 'like' && ' liked your post'}
                        {notification.type === 'comment' && ' commented on your post'}
                      </span>
                    </div>
                    {notification.content && notification.type === 'comment' && (
                      <div className="notification-preview" style={{
                        fontSize: '0.85rem',
                        color: 'var(--text-secondary)',
                        marginTop: '0.25rem',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap'
                      }}>
                        {notification.content}
                      </div>
                    )}
                    <div className="notification-time">
                      {formatTime(notification.created_at)}
                    </div>
                  </div>
                  <button
                    className="notification-delete"
                    onClick={(e) => handleDelete(e, notification.id)}
                    aria-label="Delete notification"
                  >
                    ✕
                  </button>
                </div>
              )
            })
          )}
        </div>
      </div>
    </>
  )
}
