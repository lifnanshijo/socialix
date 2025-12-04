import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import '../styles/userProfile.css';

const UserProfile = () => {
  const { userId } = useParams();
  const { user: currentUser } = useAuth();
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [posts, setPosts] = useState([]);
  const [stats, setStats] = useState({
    followers_count: 0,
    following_count: 0,
    is_following: false
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('posts');
  const [showFollowersModal, setShowFollowersModal] = useState(false);
  const [showFollowingModal, setShowFollowingModal] = useState(false);
  const [followers, setFollowers] = useState([]);
  const [following, setFollowing] = useState([]);
  const [loadingFollowers, setLoadingFollowers] = useState(false);

  const API_BASE = 'http://localhost:5000/api';

  useEffect(() => {
    if (userId) {
      console.log('Loading user profile for userId:', userId);
      fetchUserProfile();
      fetchUserPosts();
      fetchFollowStats();
    }
  }, [userId]);

  const fetchUserProfile = async () => {
    try {
      const token = localStorage.getItem('token');
      console.log('Fetching user profile for ID:', userId);
      const response = await axios.get(`${API_BASE}/users/${userId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      console.log('User profile data:', response.data);
      setUser(response.data);
      setError(null);
    } catch (error) {
      console.error('Error fetching user profile:', error);
      console.error('Error response:', error.response?.data);
      setError(error.response?.data?.message || 'Failed to load user profile');
      setLoading(false);
    }
  };

  const fetchUserPosts = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_BASE}/posts/feed?user_id=${userId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setPosts(response.data.posts || []);
    } catch (error) {
      console.error('Error fetching user posts:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchFollowStats = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_BASE}/users/${userId}/stats`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      console.log('Follow stats received:', response.data);
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching follow stats:', error);
      console.error('Error response:', error.response?.data);
    }
  };

  const handleFollow = async () => {
    try {
      const token = localStorage.getItem('token');
      const endpoint = stats.is_following ? 'unfollow' : 'follow';
      console.log(`Attempting to ${endpoint} user ${userId}`);
      
      const response = await axios.post(
        `${API_BASE}/users/${userId}/${endpoint}`, 
        {}, 
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      
      console.log(`${endpoint} response:`, response.data);
      
      // Refresh stats after follow/unfollow
      await fetchFollowStats();
    } catch (error) {
      console.error('Error toggling follow:', error);
      console.error('Error response:', error.response?.data);
      alert(error.response?.data?.error || `Failed to ${stats.is_following ? 'unfollow' : 'follow'} user`);
    }
  };

  const handleMessage = () => {
    navigate('/chat');
  };

  const fetchFollowers = async () => {
    setLoadingFollowers(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_BASE}/users/${userId}/followers`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setFollowers(response.data.followers || []);
    } catch (error) {
      console.error('Error fetching followers:', error);
    } finally {
      setLoadingFollowers(false);
    }
  };

  const fetchFollowing = async () => {
    setLoadingFollowers(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_BASE}/users/${userId}/following`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setFollowing(response.data.following || []);
    } catch (error) {
      console.error('Error fetching following:', error);
    } finally {
      setLoadingFollowers(false);
    }
  };

  const handleShowFollowers = () => {
    fetchFollowers();
    setShowFollowersModal(true);
  };

  const handleShowFollowing = () => {
    fetchFollowing();
    setShowFollowingModal(true);
  };

  const startConversationWith = async (targetUserId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(
        `${API_BASE}/chat/conversations/${targetUserId}`,
        {},
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      navigate('/chat');
    } catch (error) {
      console.error('Error starting conversation:', error);
    }
  };

  const isOwnProfile = currentUser && user && currentUser.id === user.id;

  if (loading) {
    return <div className="loading">Loading profile...</div>;
  }

  if (error || !user) {
    return (
      <div className="error-container">
        <div className="error">
          {error || 'User not found'}
        </div>
        <button className="btn btn-primary" onClick={() => navigate('/home')}>
          Back to Home
        </button>
      </div>
    );
  }

  return (
    <div className="user-profile-container">
      <div className="profile-header">
        {user.coverImage && (
          <div 
            className="cover-image" 
            style={{ backgroundImage: `url(${user.coverImage})` }}
          />
        )}
        <div className="profile-info">
          <div className="avatar-section">
            {user.avatar ? (
              <img src={user.avatar} alt={user.username} className="profile-avatar" />
            ) : (
              <div className="profile-avatar-placeholder">
                {user.username?.charAt(0).toUpperCase()}
              </div>
            )}
          </div>
          <div className="user-details">
            <h1>{user.username}</h1>
            <p className="email">{user.email}</p>
            {user.bio && <p className="bio">{user.bio}</p>}
            
            <div className="stats">
              <div className="stat-item" onClick={() => setActiveTab('posts')} style={{ cursor: 'pointer' }}>
                <span className="stat-number">{posts.length}</span>
                <span className="stat-label">Posts</span>
              </div>
              <div className="stat-item" onClick={handleShowFollowers} style={{ cursor: 'pointer' }}>
                <span className="stat-number">{stats.followers_count}</span>
                <span className="stat-label">Followers</span>
              </div>
              <div className="stat-item" onClick={handleShowFollowing} style={{ cursor: 'pointer' }}>
                <span className="stat-number">{stats.following_count}</span>
                <span className="stat-label">Following</span>
              </div>
            </div>

            <div className="profile-actions">
              {isOwnProfile ? (
                <button 
                  className="btn btn-primary"
                  onClick={() => navigate('/profile')}
                >
                  Edit Profile
                </button>
              ) : (
                <>
                  <button 
                    className={`btn ${stats.is_following ? 'btn-secondary' : 'btn-primary'}`}
                    onClick={handleFollow}
                  >
                    {stats.is_following ? 'Unfollow' : 'Follow'}
                  </button>
                  <button 
                    className="btn btn-secondary"
                    onClick={handleMessage}
                  >
                    Message
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="profile-content">
        <div className="tabs">
          <button 
            className={`tab ${activeTab === 'posts' ? 'active' : ''}`}
            onClick={() => setActiveTab('posts')}
          >
            Posts
          </button>
        </div>

        <div className="tab-content">
          {activeTab === 'posts' && (
            <div className="posts-grid">
              {posts.length === 0 ? (
                <p className="no-posts">No posts yet</p>
              ) : (
                posts.map((post) => (
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
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
      </div>

      {/* Followers Modal */}
      {showFollowersModal && (
        <div className="modal-overlay" onClick={() => setShowFollowersModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Followers</h2>
              <button className="modal-close" onClick={() => setShowFollowersModal(false)}>×</button>
            </div>
            <div className="modal-body">
              {loadingFollowers ? (
                <p className="loading-text">Loading...</p>
              ) : followers.length === 0 ? (
                <p className="no-results">No followers yet</p>
              ) : (
                <div className="users-list">
                  {followers.map((follower) => (
                    <div key={follower.id} className="user-item">
                      <div 
                        className="user-info-section"
                        onClick={() => {
                          setShowFollowersModal(false);
                          navigate(`/profile/${follower.id}`);
                        }}
                      >
                        <div className="user-avatar-small">
                          {follower.username?.charAt(0).toUpperCase()}
                        </div>
                        <div className="user-details-small">
                          <div className="username-small">{follower.username}</div>
                          {follower.bio && <div className="bio-small">{follower.bio}</div>}
                        </div>
                      </div>
                      <button 
                        className="btn btn-primary btn-small"
                        onClick={() => {
                          setShowFollowersModal(false);
                          startConversationWith(follower.id);
                        }}
                      >
                        Message
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Following Modal */}
      {showFollowingModal && (
        <div className="modal-overlay" onClick={() => setShowFollowingModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Following</h2>
              <button className="modal-close" onClick={() => setShowFollowingModal(false)}>×</button>
            </div>
            <div className="modal-body">
              {loadingFollowers ? (
                <p className="loading-text">Loading...</p>
              ) : following.length === 0 ? (
                <p className="no-results">Not following anyone yet</p>
              ) : (
                <div className="users-list">
                  {following.map((followedUser) => (
                    <div key={followedUser.id} className="user-item">
                      <div 
                        className="user-info-section"
                        onClick={() => {
                          setShowFollowingModal(false);
                          navigate(`/profile/${followedUser.id}`);
                        }}
                      >
                        <div className="user-avatar-small">
                          {followedUser.username?.charAt(0).toUpperCase()}
                        </div>
                        <div className="user-details-small">
                          <div className="username-small">{followedUser.username}</div>
                          {followedUser.bio && <div className="bio-small">{followedUser.bio}</div>}
                        </div>
                      </div>
                      <button 
                        className="btn btn-primary btn-small"
                        onClick={() => {
                          setShowFollowingModal(false);
                          startConversationWith(followedUser.id);
                        }}
                      >
                        Message
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserProfile;
