import React, { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import axios from 'axios'
import '../styles/home.css'

function Home() {
  const { user } = useAuth()
  const [posts, setPosts] = useState([])
  const [content, setContent] = useState('')
  const [imageFile, setImageFile] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [expandedComments, setExpandedComments] = useState({})
  const [commentText, setCommentText] = useState({})
  const [postLikes, setPostLikes] = useState({})
  const [postComments, setPostComments] = useState({})

  useEffect(() => {
    fetchPosts()
  }, [])

  const fetchPosts = async () => {
    try {
      const response = await axios.get('/api/posts/feed')
      setPosts(response.data)
      
      // Fetch likes and comments for each post
      response.data.forEach(post => {
        fetchPostLikes(post.id)
        fetchPostComments(post.id)
      })
    } catch (err) {
      console.error('Failed to fetch posts:', err)
    }
  }

  const fetchPostLikes = async (postId) => {
    try {
      const response = await axios.get(`/api/posts/${postId}/likes`)
      setPostLikes(prev => ({
        ...prev,
        [postId]: {
          count: response.data.count,
          isLiked: response.data.likes?.some(like => like.user_id === user?.id) || false
        }
      }))
    } catch (err) {
      console.error('Failed to fetch likes:', err)
    }
  }

  const fetchPostComments = async (postId) => {
    try {
      const response = await axios.get(`/api/posts/${postId}/comments`)
      setPostComments(prev => ({
        ...prev,
        [postId]: response.data
      }))
    } catch (err) {
      console.error('Failed to fetch comments:', err)
    }
  }

  const handleLike = async (postId) => {
    try {
      const isLiked = postLikes[postId]?.isLiked
      
      if (isLiked) {
        await axios.post(`/api/posts/${postId}/unlike`)
      } else {
        await axios.post(`/api/posts/${postId}/like`)
      }
      
      fetchPostLikes(postId)
    } catch (err) {
      console.error('Failed to toggle like:', err)
    }
  }

  const handleAddComment = async (postId) => {
    const comment = commentText[postId]?.trim()
    if (!comment) return

    try {
      await axios.post(`/api/posts/${postId}/comments`, { content: comment })
      setCommentText(prev => ({ ...prev, [postId]: '' }))
      fetchPostComments(postId)
    } catch (err) {
      console.error('Failed to add comment:', err)
    }
  }

  const handleDeleteComment = async (commentId, postId) => {
    if (!window.confirm('Delete this comment?')) return

    try {
      await axios.delete(`/api/posts/comments/${commentId}`)
      fetchPostComments(postId)
    } catch (err) {
      console.error('Failed to delete comment:', err)
    }
  }

  const toggleComments = (postId) => {
    setExpandedComments(prev => ({
      ...prev,
      [postId]: !prev[postId]
    }))
  }

  const handleShare = async (postId) => {
    const shareUrl = `${window.location.origin}/post/${postId}`
    
    try {
      if (navigator.share) {
        await navigator.share({
          title: 'Check out this post!',
          url: shareUrl
        })
      } else {
        // Fallback: copy to clipboard
        await navigator.clipboard.writeText(shareUrl)
        alert('Link copied to clipboard!')
      }
    } catch (err) {
      console.error('Failed to share:', err)
    }
  }

  const handleImageSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        setError('Image size must be less than 5MB')
        return
      }
      setImageFile(file)
      setImagePreview(URL.createObjectURL(file))
      setError('')
    }
  }

  const removeImage = () => {
    setImageFile(null)
    setImagePreview(null)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!content.trim() && !imageFile) {
      setError('Please add some content or an image')
      return
    }

    setLoading(true)
    setError('')

    try {
      const formData = new FormData()
      formData.append('content', content)
      if (imageFile) {
        formData.append('image', imageFile)
      }

      await axios.post('/api/posts/create', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      // Clear form
      setContent('')
      setImageFile(null)
      setImagePreview(null)
      
      // Refresh posts
      fetchPosts()
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to create post')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (postId) => {
    if (!window.confirm('Are you sure you want to delete this post?')) {
      return
    }

    try {
      await axios.delete(`/api/posts/${postId}`)
      setPosts(posts.filter(post => post.id !== postId))
    } catch (err) {
      console.error('Failed to delete post:', err)
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const seconds = Math.floor((now - date) / 1000)
    
    if (seconds < 60) return 'just now'
    if (seconds < 3600) return `${Math.floor(seconds / 60)} minutes ago`
    if (seconds < 86400) return `${Math.floor(seconds / 3600)} hours ago`
    if (seconds < 604800) return `${Math.floor(seconds / 86400)} days ago`
    
    return date.toLocaleDateString()
  }

  return (
    <div className="home-container">
      <div className="welcome-section card">
        <h1>Welcome back, {user?.username}!</h1>
        <p>Share your moments with the world</p>
      </div>

      <div className="feed-container">
        <div className="create-post card">
          <h3>Create a post</h3>
          {error && <div className="error-message">{error}</div>}
          
          <form onSubmit={handleSubmit}>
            <textarea 
              placeholder="What's on your mind?"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows="3"
            />
            
            {imagePreview && (
              <div className="image-preview">
                <img src={imagePreview} alt="Preview" />
                <button 
                  type="button" 
                  className="remove-image"
                  onClick={removeImage}
                >
                  ✕
                </button>
              </div>
            )}
            
            <div className="post-actions-bar">
              <label className="image-upload-btn">
                📷 Add Photo
                <input 
                  type="file" 
                  accept="image/*"
                  onChange={handleImageSelect}
                  style={{ display: 'none' }}
                />
              </label>
              
              <button 
                type="submit" 
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? 'Posting...' : 'Post'}
              </button>
            </div>
          </form>
        </div>

        <div className="posts-section">
          {posts.length === 0 ? (
            <div className="no-posts card">
              <p>No posts yet. Be the first to post!</p>
            </div>
          ) : (
            posts.map(post => (
              <div key={post.id} className="post-card card">
                <div className="post-header">
                  <img 
                    src={post.user?.avatar || 'https://via.placeholder.com/50'} 
                    alt="avatar" 
                  />
                  <div className="post-user-info">
                    <h4>{post.user?.username || 'Unknown User'}</h4>
                    <span>{formatDate(post.createdAt)}</span>
                  </div>
                  {post.userId === user?.id && (
                    <button 
                      className="delete-btn"
                      onClick={() => handleDelete(post.id)}
                    >
                      🗑️
                    </button>
                  )}
                </div>
                
                <div className="post-content">
                  {post.content && <p>{post.content}</p>}
                  {post.imageUrl && (
                    <div className="post-image">
                      <img src={post.imageUrl} alt="Post" />
                    </div>
                  )}
                </div>
                
                <div className="post-actions">
                  <button 
                    className={`btn like-btn ${postLikes[post.id]?.isLiked ? 'liked' : ''}`}
                    onClick={() => handleLike(post.id)}
                  >
                    {postLikes[post.id]?.isLiked ? '❤️' : '🤍'} Like
                    {postLikes[post.id]?.count > 0 && (
                      <span className="count"> ({postLikes[post.id].count})</span>
                    )}
                  </button>
                  <button 
                    className="btn"
                    onClick={() => toggleComments(post.id)}
                  >
                    💬 Comment
                    {postComments[post.id]?.count > 0 && (
                      <span className="count"> ({postComments[post.id].count})</span>
                    )}
                  </button>
                  <button 
                    className="btn"
                    onClick={() => handleShare(post.id)}
                  >
                    🔗 Share
                  </button>
                </div>

                {expandedComments[post.id] && (
                  <div className="comments-section">
                    <div className="add-comment">
                      <input
                        type="text"
                        placeholder="Write a comment..."
                        value={commentText[post.id] || ''}
                        onChange={(e) => setCommentText(prev => ({
                          ...prev,
                          [post.id]: e.target.value
                        }))}
                        onKeyPress={(e) => {
                          if (e.key === 'Enter') {
                            handleAddComment(post.id)
                          }
                        }}
                      />
                      <button 
                        className="btn btn-primary"
                        onClick={() => handleAddComment(post.id)}
                      >
                        Post
                      </button>
                    </div>

                    <div className="comments-list">
                      {postComments[post.id]?.comments?.map(comment => (
                        <div key={comment.id} className="comment-item">
                          <img 
                            src={comment.avatar || 'https://via.placeholder.com/40'} 
                            alt="avatar" 
                          />
                          <div className="comment-content">
                            <div className="comment-header">
                              <strong>{comment.username}</strong>
                              <span>{formatDate(comment.createdAt)}</span>
                            </div>
                            <p>{comment.content}</p>
                          </div>
                          {comment.userId === user?.id && (
                            <button 
                              className="delete-comment-btn"
                              onClick={() => handleDeleteComment(comment.id, post.id)}
                            >
                              ✕
                            </button>
                          )}
                        </div>
                      ))}
                      {(!postComments[post.id]?.comments || postComments[post.id].comments.length === 0) && (
                        <p className="no-comments">No comments yet. Be the first to comment!</p>
                      )}
                    </div>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

export default Home
