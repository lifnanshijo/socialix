import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import axios from 'axios'
import '../styles/search.css'

const API_BASE = 'http://localhost:5000/api'

function Search() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [followStatus, setFollowStatus] = useState({})
  const [followLoading, setFollowLoading] = useState({})
  const [userStats, setUserStats] = useState({})
  const [showMessageModal, setShowMessageModal] = useState(null)
  const [messageText, setMessageText] = useState('')
  const [sendingMessage, setSendingMessage] = useState(false)

  useEffect(() => {
    if (searchQuery.trim()) {
      const delayDebounce = setTimeout(() => {
        searchUsers()
      }, 500)

      return () => clearTimeout(delayDebounce)
    } else {
      setSearchResults([])
    }
  }, [searchQuery])

  useEffect(() => {
    // Fetch follow status and stats for all search results
    searchResults.forEach(searchUser => {
      if (searchUser.id !== user?.id) {
        checkFollowStatus(searchUser.id)
        fetchUserStats(searchUser.id)
      }
    })
  }, [searchResults])

  const searchUsers = async () => {
    if (!searchQuery.trim()) {
      setSearchResults([])
      return
    }

    setLoading(true)
    setError('')

    try {
      const token = localStorage.getItem('token')
      console.log('Searching for:', searchQuery)
      console.log('Token exists:', !!token)
      
      const response = await axios.get(`${API_BASE}/users/search?q=${searchQuery}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      
      console.log('Search response:', response.data)
      
      // Filter out current user from results
      const filteredResults = response.data.filter(u => u.id !== user?.id)
      setSearchResults(filteredResults)
    } catch (err) {
      console.error('Search failed:', err)
      console.error('Error response:', err.response?.data)
      console.error('Error status:', err.response?.status)
      setError(err.response?.data?.message || 'Failed to search users')
    } finally {
      setLoading(false)
    }
  }

  const fetchUserStats = async (userId) => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${API_BASE}/users/${userId}/stats`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      
      setUserStats(prev => ({
        ...prev,
        [userId]: {
          followers: response.data.followers_count || 0,
          following: response.data.following_count || 0
        }
      }))
    } catch (err) {
      console.error('Failed to fetch user stats:', err)
    }
  }

  const checkFollowStatus = async (userId) => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${API_BASE}/users/${userId}/stats`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      
      setFollowStatus(prev => ({
        ...prev,
        [userId]: response.data.is_following || false
      }))
    } catch (err) {
      console.error('Failed to check follow status:', err)
    }
  }

  const handleFollow = async (userId) => {
    setFollowLoading(prev => ({ ...prev, [userId]: true }))

    try {
      const token = localStorage.getItem('token')
      const isFollowing = followStatus[userId]

      if (isFollowing) {
        await axios.post(`${API_BASE}/users/${userId}/unfollow`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        })
      } else {
        await axios.post(`${API_BASE}/users/${userId}/follow`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        })
      }

      setFollowStatus(prev => ({
        ...prev,
        [userId]: !isFollowing
      }))
      
      // Update stats after follow/unfollow
      fetchUserStats(userId)
    } catch (err) {
      console.error('Follow action failed:', err)
      setError('Failed to update follow status')
    } finally {
      setFollowLoading(prev => ({ ...prev, [userId]: false }))
    }
  }

  const handleMessage = async (userId) => {
    setShowMessageModal(userId)
    setMessageText('')
  }

  const handleSendMessage = async () => {
    if (!messageText.trim() || !showMessageModal) return

    setSendingMessage(true)
    try {
      const token = localStorage.getItem('token')
      
      // Create or get conversation
      const convResponse = await axios.post(`${API_BASE}/chat/conversations/${showMessageModal}`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      })
      
      const conversationId = convResponse.data.conversation_id
      
      // Send the message
      await axios.post(`${API_BASE}/chat/conversations/${conversationId}/messages`, 
        { content: messageText },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      
      setShowMessageModal(null)
      setMessageText('')
      
      // Show success message
      alert('Message sent successfully!')
      
      // Navigate to chat page
      navigate('/chat')
    } catch (err) {
      console.error('Failed to send message:', err)
      setError('Failed to send message')
    } finally {
      setSendingMessage(false)
    }
  }

  const handleQuickChat = (userId) => {
    // Quick navigate to chat
    handleMessage(userId)
  }

  const goToProfile = (userId) => {
    navigate(`/profile/${userId}`)
  }

  return (
    <div className="search-container">
      <div className="search-header">
        <h1>Find People</h1>
        <p>Search for users to follow and connect with</p>
      </div>

      <div className="search-box card">
        <div className="search-input-wrapper">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            placeholder="Search by username..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
          {searchQuery && (
            <button 
              className="clear-btn"
              onClick={() => setSearchQuery('')}
            >
              ✕
            </button>
          )}
        </div>
      </div>

      {error && (
        <div className="error-message card">
          {error}
        </div>
      )}

      {loading && (
        <div className="loading-section">
          <div className="spinner"></div>
          <p>Searching...</p>
        </div>
      )}

      {!loading && searchQuery && searchResults.length === 0 && (
        <div className="no-results card">
          <p>No users found matching "{searchQuery}"</p>
        </div>
      )}

      {searchResults.length > 0 && (
        <div className="search-results">
          <h2>Search Results ({searchResults.length})</h2>
          <div className="users-grid">
            {searchResults.map((searchUser) => (
              <div key={searchUser.id} className="user-card card">
                <div 
                  className="user-card-header"
                  onClick={() => goToProfile(searchUser.id)}
                  style={{ cursor: 'pointer' }}
                >
                  <div className="user-avatar-large">
                    {searchUser.username?.charAt(0).toUpperCase()}
                  </div>
                  <div className="user-info">
                    <h3 className="username">{searchUser.username}</h3>
                    <p className="email">{searchUser.email}</p>
                    {searchUser.bio && (
                      <p className="bio">{searchUser.bio}</p>
                    )}
                    
                    {/* User Stats */}
                    <div className="user-stats">
                      <span className="stat-item">
                        <strong>{userStats[searchUser.id]?.followers || 0}</strong> followers
                      </span>
                      <span className="stat-separator">•</span>
                      <span className="stat-item">
                        <strong>{userStats[searchUser.id]?.following || 0}</strong> following
                      </span>
                    </div>
                  </div>
                </div>

                <div className="user-card-actions">
                  <button
                    className={`btn ${followStatus[searchUser.id] ? 'btn-secondary' : 'btn-primary'}`}
                    onClick={() => handleFollow(searchUser.id)}
                    disabled={followLoading[searchUser.id]}
                  >
                    {followLoading[searchUser.id] ? (
                      'Loading...'
                    ) : followStatus[searchUser.id] ? (
                      <>
                        <span>✓</span> Following
                      </>
                    ) : (
                      <>
                        <span>+</span> Follow
                      </>
                    )}
                  </button>
                  <button
                    className="btn btn-outline"
                    onClick={() => handleMessage(searchUser.id)}
                  >
                    <span>💬</span> Message
                  </button>
                  <button
                    className="btn btn-outline"
                    onClick={() => goToProfile(searchUser.id)}
                  >
                    <span>👤</span> View Profile
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Message Modal */}
      {showMessageModal && (
        <div className="modal-overlay" onClick={() => setShowMessageModal(null)}>
          <div className="message-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Send Message</h3>
              <button className="modal-close" onClick={() => setShowMessageModal(null)}>✕</button>
            </div>
            <div className="modal-body">
              <div className="message-recipient">
                <div className="recipient-avatar">
                  {searchResults.find(u => u.id === showMessageModal)?.username?.charAt(0).toUpperCase()}
                </div>
                <div className="recipient-info">
                  <strong>{searchResults.find(u => u.id === showMessageModal)?.username}</strong>
                  <p>Start a conversation</p>
                </div>
              </div>
              <textarea
                className="message-textarea"
                placeholder="Type your message here..."
                value={messageText}
                onChange={(e) => setMessageText(e.target.value)}
                rows="4"
                autoFocus
              />
            </div>
            <div className="modal-footer">
              <button 
                className="btn btn-outline" 
                onClick={() => setShowMessageModal(null)}
                disabled={sendingMessage}
              >
                Cancel
              </button>
              <button 
                className="btn btn-primary" 
                onClick={handleSendMessage}
                disabled={!messageText.trim() || sendingMessage}
              >
                {sendingMessage ? 'Sending...' : 'Send Message'}
              </button>
            </div>
          </div>
        </div>
      )}

      {!searchQuery && !loading && (
        <div className="search-suggestions card">
          <h3>Tips for finding people:</h3>
          <ul>
            <li>Search by username to find specific users</li>
            <li>Use the search bar above to start discovering people</li>
            <li>Follow users to see their posts in your feed</li>
            <li>Send messages to connect with people</li>
          </ul>
        </div>
      )}
    </div>
  )
}

export default Search
