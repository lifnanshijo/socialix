import { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE = 'http://localhost:5000/api'

export function useNotifications() {
  const [notifications, setNotifications] = useState([])
  const [unreadCount, setUnreadCount] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const token = localStorage.getItem('token')

  const fetchNotifications = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.get(`${API_BASE}/notifications/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      console.log('Notifications response:', response.data)
      setNotifications(response.data.notifications || [])
      return response.data.notifications || []
    } catch (err) {
      setError(err.message)
      console.error('Error fetching notifications:', err)
      console.error('Error response:', err.response?.data)
      return []
    } finally {
      setLoading(false)
    }
  }

  const fetchUnreadCount = async () => {
    try {
      const response = await axios.get(`${API_BASE}/notifications/unread-count`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      console.log('Unread count:', response.data.count)
      setUnreadCount(response.data.count || 0)
    } catch (err) {
      console.error('Error fetching unread count:', err)
      console.error('Error response:', err.response?.data)
    }
  }

  const markAsRead = async (notificationId) => {
    try {
      await axios.put(`${API_BASE}/notifications/${notificationId}/read`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setNotifications(notifications.map(n => 
        n.id === notificationId ? { ...n, is_read: true } : n
      ))
      setUnreadCount(Math.max(0, unreadCount - 1))
    } catch (err) {
      console.error('Error marking notification as read:', err)
    }
  }

  const markAllAsRead = async () => {
    try {
      await axios.put(`${API_BASE}/notifications/mark-all-read`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setNotifications(notifications.map(n => ({ ...n, is_read: true })))
      setUnreadCount(0)
    } catch (err) {
      console.error('Error marking all as read:', err)
    }
  }

  const deleteNotification = async (notificationId) => {
    try {
      await axios.delete(`${API_BASE}/notifications/${notificationId}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      const notification = notifications.find(n => n.id === notificationId)
      setNotifications(notifications.filter(n => n.id !== notificationId))
      if (notification && !notification.is_read) {
        setUnreadCount(Math.max(0, unreadCount - 1))
      }
    } catch (err) {
      console.error('Error deleting notification:', err)
    }
  }

  useEffect(() => {
    if (token) {
      fetchUnreadCount()
      const interval = setInterval(fetchUnreadCount, 30000) // Update every 30 seconds
      return () => clearInterval(interval)
    }
  }, [token])

  return {
    notifications,
    unreadCount,
    loading,
    error,
    fetchNotifications,
    fetchUnreadCount,
    markAsRead,
    markAllAsRead,
    deleteNotification
  }
}
