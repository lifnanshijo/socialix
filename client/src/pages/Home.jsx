import React from 'react'
import { useAuth } from '../context/AuthContext'
import '../styles/home.css'

function Home() {
  const { user } = useAuth()

  return (
    <div className="home-container">
      <div className="welcome-section card">
        <h1>Welcome back, {user?.username}!</h1>
        <p>This is your social media dashboard</p>
      </div>

      <div className="feed-container">
        <div className="create-post card">
          <h3>Create a post</h3>
          <textarea placeholder="What's on your mind?"></textarea>
          <button className="btn btn-primary">Post</button>
        </div>

        <div className="posts-section">
          <div className="post-card card">
            <div className="post-header">
              <img src="https://via.placeholder.com/50" alt="avatar" />
              <div>
                <h4>Sample User</h4>
                <span>2 hours ago</span>
              </div>
            </div>
            <div className="post-content">
              <p>This is a sample post. Start building your social media features here!</p>
            </div>
            <div className="post-actions">
              <button className="btn">Like</button>
              <button className="btn">Comment</button>
              <button className="btn">Share</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
