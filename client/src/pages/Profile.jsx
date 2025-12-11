import React, { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import ProfileCustomization from '../components/ProfileCustomization'
import axios from 'axios'
import '../styles/profile.css'

function Profile() {
  const { user } = useAuth()
  const [isEditing, setIsEditing] = useState(false)
  const [posts, setPosts] = useState([])
  const [postLikes, setPostLikes] = useState({})
  const [postComments, setPostComments] = useState({})
  const [expandedComments, setExpandedComments] = useState({})
  const [commentText, setCommentText] = useState({})
  const [profileData, setProfileData] = useState({
    username: '',
    bio: '',
    avatar: '',
    cover_image: ''
  })

  const API_BASE = 'http://localhost:5000/api'

  useEffect(() => {
    if (user) {
      setProfileData({
        username: user.username || '',
        bio: user.bio || '',
        avatar: user.avatar || '',
        cover_image: user.cover_image || ''
      })
      fetchUserPosts()
    }
  }, [user])

  const fetchUserPosts = async () => {
    if (!user?.id) return
    
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${API_BASE}/posts/user/${user.id}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setPosts(response.data.posts || [])
    } catch (error) {
      console.error('Error fetching posts:', error)
    }
  }

  const fetchPostLikes = async (postId) => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${API_BASE}/posts/${postId}/likes`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setPostLikes(prev => ({
        ...prev,
        [postId]: {
          count: response.data.likes?.length || 0,
          userLiked: response.data.user_liked || false
        }
      }))
    } catch (error) {
      console.error('Error fetching likes:', error)
    }
  }

  const fetchPostComments = async (postId) => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${API_BASE}/posts/${postId}/comments`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setPostComments(prev => ({
        ...prev,
        [postId]: response.data.comments || []
      }))
    } catch (error) {
      console.error('Error fetching comments:', error)
    }
  }

  const handleLike = async (postId) => {
    try {
      const token = localStorage.getItem('token')
      const userLiked = postLikes[postId]?.userLiked
      
      if (userLiked) {
        await axios.delete(`${API_BASE}/posts/${postId}/like`, {
          headers: { Authorization: `Bearer ${token}` }
        })
      } else {
        await axios.post(`${API_BASE}/posts/${postId}/like`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        })
      }
      
      await fetchPostLikes(postId)
    } catch (error) {
      console.error('Error toggling like:', error)
    }
  }

  const handleComment = async (postId) => {
    if (!commentText[postId]?.trim()) return
    
    try {
      const token = localStorage.getItem('token')
      await axios.post(`${API_BASE}/posts/${postId}/comments`, 
        { content: commentText[postId] },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      
      setCommentText(prev => ({ ...prev, [postId]: '' }))
      await fetchPostComments(postId)
    } catch (error) {
      console.error('Error adding comment:', error)
    }
  }

  const toggleComments = (postId) => {
    setExpandedComments(prev => ({
      ...prev,
      [postId]: !prev[postId]
    }))
    
    if (!expandedComments[postId] && !postComments[postId]) {
      fetchPostComments(postId)
    }
  }

  const handleChange = (e) => {
    setProfileData({
      ...profileData,
      [e.target.name]: e.target.value
    })
  }

  const handleImageUpload = (updatedUser) => {
    // Update local state with new image URLs from the updated user
    setProfileData({
      username: updatedUser.username || profileData.username,
      bio: updatedUser.bio || profileData.bio,
      avatar: updatedUser.avatar || profileData.avatar,
      cover_image: updatedUser.cover_image || profileData.cover_image
    })
    setIsEditing(false)
  }

  return (
    <div className="profile-container">
      <div className="profile-header">
        <div className="cover-image" style={{ 
          backgroundImage: `url(${profileData.cover_image || 'https://via.placeholder.com/1200x300'})` 
        }}>
        </div>
        <div className="profile-info">
          <div className="avatar" style={{ 
            backgroundImage: `url(${profileData.avatar || 'https://via.placeholder.com/150'})` 
          }}>
          </div>
          <div className="user-details">
            <h1>{profileData.username}</h1>
            <p className="bio">{profileData.bio || 'No bio yet'}</p>
          </div>
          <button 
            className="btn btn-primary edit-btn"
            onClick={() => setIsEditing(!isEditing)}
          >
            {isEditing ? 'Cancel' : 'Edit Profile'}
          </button>
        </div>
      </div>

      {isEditing && (
        <ProfileCustomization
          profileData={profileData}
          handleChange={handleChange}
          onImageUpload={handleImageUpload}
        />
      )}

      <div className="profile-content card">
        <h2>About</h2>
        <div className="about-section">
          <p><strong>Username:</strong> {profileData.username}</p>
          <p><strong>Email:</strong> {user?.email}</p>
          <p><strong>Member since:</strong> {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}</p>
        </div>
      </div>

      <div className="profile-content card" style={{ marginTop: '20px' }}>
        <h2>My Posts</h2>
        <div className="posts-grid">
          {posts.length === 0 ? (
            <p className="no-posts">No posts yet</p>
          ) : (
            posts.map((post) => {
              const likes = postLikes[post.id] || { count: 0, userLiked: false }
              const comments = postComments[post.id] || []
              const isExpanded = expandedComments[post.id] || false
              
              if (!postLikes[post.id]) {
                fetchPostLikes(post.id)
              }
              
              return (
                <div key={post.id} className="post-card">
                  {post.imageUrl && (
                    <img 
                      src={post.imageUrl} 
                      alt="Post" 
                      className="post-image"
                    />
                  )}
                  {post.videoUrl && (
                    <video 
                      src={post.videoUrl} 
                      controls 
                      className="post-image"
                    />
                  )}
                  {post.content && (
                    <p className="post-content">{post.content}</p>
                  )}
                  <div className="post-meta">
                    <span>{new Date(post.createdAt).toLocaleDateString()}</span>
                    <div className="post-actions">
                      <button 
                        className={`action-btn ${likes.userLiked ? 'liked' : ''}`}
                        onClick={() => handleLike(post.id)}
                      >
                        <span className="icon">❤️</span>
                        <span>{likes.count}</span>
                      </button>
                      <button 
                        className="action-btn"
                        onClick={() => toggleComments(post.id)}
                      >
                        <span className="icon">💬</span>
                        <span>{comments.length}</span>
                      </button>
                      <button 
                        className="action-btn"
                        onClick={() => {
                          navigator.clipboard.writeText(`${window.location.origin}/post/${post.id}`)
                          alert('Link copied to clipboard!')
                        }}
                      >
                        <span className="icon">🔗</span>
                      </button>
                    </div>
                  </div>
                  
                  {isExpanded && (
                    <div className="comments-section">
                      <div className="comments-list">
                        {comments.map((comment) => (
                          <div key={comment.id} className="comment">
                            <div className="comment-header">
                              <span className="comment-author">{comment.username}</span>
                              <span className="comment-date">
                                {new Date(comment.createdAt).toLocaleDateString()}
                              </span>
                            </div>
                            <p className="comment-content">{comment.content}</p>
                          </div>
                        ))}
                      </div>
                      <div className="comment-input">
                        <input
                          type="text"
                          placeholder="Add a comment..."
                          value={commentText[post.id] || ''}
                          onChange={(e) => setCommentText(prev => ({
                            ...prev,
                            [post.id]: e.target.value
                          }))}
                          onKeyDown={(e) => {
                            if (e.key === 'Enter') {
                              handleComment(post.id)
                            }
                          }}
                        />
                        <button 
                          className="btn btn-primary btn-sm"
                          onClick={() => handleComment(post.id)}
                        >
                          Post
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              )
            })
          )}
        </div>
      </div>
    </div>
  )
}

export default Profile
