import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import VoiceRecorder from '../components/VoiceRecorder';
import '../styles/chat.css';

const Chat = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [showSearch, setShowSearch] = useState(false);
  const [showVoiceRecorder, setShowVoiceRecorder] = useState(false);
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const API_BASE = 'http://localhost:5000/api';

  useEffect(() => {
    fetchConversations();
  }, []);

  useEffect(() => {
    if (selectedConversation) {
      fetchMessages(selectedConversation.id);
      const interval = setInterval(() => {
        fetchMessages(selectedConversation.id);
      }, 3000); // Poll for new messages every 3 seconds
      return () => clearInterval(interval);
    }
  }, [selectedConversation]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (searchTerm) {
      searchUsers();
    } else {
      setSearchResults([]);
    }
  }, [searchTerm]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchConversations = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_BASE}/chat/conversations`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setConversations(response.data.conversations || []);
    } catch (error) {
      console.error('Error fetching conversations:', error);
    }
  };

  const fetchMessages = async (conversationId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(
        `${API_BASE}/chat/conversations/${conversationId}/messages`,
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      setMessages(response.data.messages || []);
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if ((!newMessage.trim() && !selectedImage) || !selectedConversation) return;

    try {
      const token = localStorage.getItem('token');
      
      // Send image message
      if (selectedImage) {
        const reader = new FileReader();
        reader.onloadend = async () => {
          const base64Data = reader.result;
          await axios.post(
            `${API_BASE}/chat/conversations/${selectedConversation.id}/messages`,
            { 
              content: newMessage.trim() || null,
              message_type: 'image',
              media_data: base64Data,
              file_type: selectedImage.type
            },
            {
              headers: { Authorization: `Bearer ${token}` }
            }
          );
          setNewMessage('');
          setSelectedImage(null);
          setImagePreview(null);
          fetchMessages(selectedConversation.id);
          fetchConversations();
        };
        reader.readAsDataURL(selectedImage);
      } else {
        // Send text message
        await axios.post(
          `${API_BASE}/chat/conversations/${selectedConversation.id}/messages`,
          { content: newMessage, message_type: 'text' },
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        );
        setNewMessage('');
        fetchMessages(selectedConversation.id);
        fetchConversations();
      }
    } catch (error) {
      console.error('Error sending message:', error);
      alert('Failed to send message. Please try again.');
    }
  };

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) { // 5MB limit
        alert('Image size should be less than 5MB');
        return;
      }
      setSelectedImage(file);
      setImagePreview(URL.createObjectURL(file));
    }
  };

  const removeImage = () => {
    setSelectedImage(null);
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleVoiceRecordingComplete = async (audioBlob) => {
    if (!selectedConversation) return;

    try {
      const token = localStorage.getItem('token');
      const reader = new FileReader();
      
      reader.onloadend = async () => {
        const base64Data = reader.result;
        await axios.post(
          `${API_BASE}/chat/conversations/${selectedConversation.id}/messages`,
          { 
            message_type: 'voice',
            media_data: base64Data,
            file_type: 'audio/webm'
          },
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        );
        setShowVoiceRecorder(false);
        fetchMessages(selectedConversation.id);
        fetchConversations();
      };
      
      reader.readAsDataURL(audioBlob);
    } catch (error) {
      console.error('Error sending voice message:', error);
      alert('Failed to send voice message. Please try again.');
    }
  };

  const searchUsers = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(
        `${API_BASE}/chat/users/search?q=${searchTerm}`,
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      setSearchResults(response.data.users || []);
    } catch (error) {
      console.error('Error searching users:', error);
    }
  };

  const startConversation = async (userId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${API_BASE}/chat/conversations/${userId}`,
        {},
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      
      const conversationId = response.data.conversation_id;
      
      // Refresh conversations to get the full conversation object
      await fetchConversations();
      
      // Find and select the conversation from the list
      const conversations = await axios.get(`${API_BASE}/chat/conversations`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      const newConv = conversations.data.conversations?.find(c => c.id === conversationId);
      if (newConv) {
        setSelectedConversation(newConv);
      }
      
      fetchMessages(conversationId);
      setShowSearch(false);
      setSearchTerm('');
    } catch (error) {
      console.error('Error starting conversation:', error);
      console.error('Error response:', error.response?.data);
    }
  };

  const selectConversation = (conv) => {
    setSelectedConversation(conv);
    setShowSearch(false);
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (days > 7) {
      return date.toLocaleDateString();
    } else if (days > 0) {
      return `${days}d ago`;
    } else if (hours > 0) {
      return `${hours}h ago`;
    } else {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
  };

  return (
    <div className="chat-container">
      {/* Conversations Sidebar */}
      <div className="conversations-sidebar">
        <div className="sidebar-header">
          <h2>Messages</h2>
          <button 
            className="new-chat-btn"
            onClick={() => setShowSearch(!showSearch)}
          >
            +
          </button>
        </div>

        {showSearch && (
          <div className="search-section">
            <input
              type="text"
              placeholder="Search users..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="user-search-input"
            />
            {searchResults.length > 0 && (
              <div className="search-results">
                {searchResults.map((searchUser) => (
                  <div
                    key={searchUser.id}
                    className="search-result-item"
                    onClick={() => startConversation(searchUser.id)}
                  >
                    <div className="user-avatar">
                      {searchUser.username.charAt(0).toUpperCase()}
                    </div>
                    <div className="user-info">
                      <div className="username">{searchUser.username}</div>
                      <div className="user-email">{searchUser.email}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        <div className="conversations-list">
          {conversations.length === 0 ? (
            <div className="no-conversations">
              <p>No conversations yet</p>
              <p>Click + to start chatting</p>
            </div>
          ) : (
            conversations.map((conv) => (
              <div
                key={conv.id}
                className={`conversation-item ${
                  selectedConversation?.id === conv.id ? 'active' : ''
                }`}
              >
                <div 
                  className="user-avatar"
                  onClick={() => navigate(`/profile/${conv.other_user_id}`)}
                  style={{ cursor: 'pointer' }}
                >
                  {conv.other_username?.charAt(0).toUpperCase() || '?'}
                </div>
                <div className="conversation-info" onClick={() => selectConversation(conv)}>
                  <div className="conversation-header">
                    <span 
                      className="username"
                      onClick={(e) => {
                        e.stopPropagation();
                        navigate(`/profile/${conv.other_user_id}`);
                      }}
                      style={{ cursor: 'pointer' }}
                    >
                      {conv.other_username || 'Unknown'}
                    </span>
                    <span className="time">
                      {conv.last_message_time && formatTime(conv.last_message_time)}
                    </span>
                  </div>
                  <div className="last-message">
                    {conv.last_message || 'Start a conversation'}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Messages Area */}
      <div className="messages-area">
        {selectedConversation ? (
          <>
            <div className="messages-header">
              <div 
                className="user-avatar"
                onClick={() => navigate(`/profile/${selectedConversation.other_user_id}`)}
                style={{ cursor: 'pointer' }}
              >
                {selectedConversation.other_username?.charAt(0).toUpperCase() || '?'}
              </div>
              <span 
                className="username"
                onClick={() => navigate(`/profile/${selectedConversation.other_user_id}`)}
                style={{ cursor: 'pointer' }}
              >
                {selectedConversation.other_username || 'Chat'}
              </span>
            </div>

            <div className="messages-list">
              {messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`message ${
                    msg.sender_id === user.id ? 'sent' : 'received'
                  }`}
                >
                  <div className="message-content">
                    {msg.sender_id !== user.id && (
                      <div className="message-sender">{msg.sender_username}</div>
                    )}
                    
                    {/* Render based on message type */}
                    {msg.message_type === 'image' && msg.media_url && (
                      <div className="message-image">
                        <img src={msg.media_url} alt="Shared image" />
                      </div>
                    )}
                    
                    {msg.message_type === 'voice' && msg.media_url && (
                      <div className="message-voice">
                        <audio controls src={msg.media_url}>
                          Your browser does not support the audio element.
                        </audio>
                      </div>
                    )}
                    
                    {msg.content && (
                      <div className="message-text">{msg.content}</div>
                    )}
                    
                    <div className="message-time">
                      {formatTime(msg.created_at)}
                    </div>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            {/* Voice Recorder */}
            {showVoiceRecorder && (
              <VoiceRecorder
                onRecordingComplete={handleVoiceRecordingComplete}
                onCancel={() => setShowVoiceRecorder(false)}
              />
            )}

            {/* Image Preview */}
            {imagePreview && (
              <div className="image-preview-container">
                <div className="image-preview">
                  <img src={imagePreview} alt="Preview" />
                  <button className="remove-image-btn" onClick={removeImage}>
                    ✕
                  </button>
                </div>
              </div>
            )}

            <form className="message-input-form" onSubmit={sendMessage}>
              <input
                type="file"
                ref={fileInputRef}
                accept="image/*"
                style={{ display: 'none' }}
                onChange={handleImageSelect}
              />
              
              <button
                type="button"
                className="attach-btn"
                onClick={() => fileInputRef.current?.click()}
                title="Send image"
              >
                📷
              </button>
              
              <button
                type="button"
                className="voice-btn"
                onClick={() => setShowVoiceRecorder(!showVoiceRecorder)}
                title="Record voice message"
              >
                🎤
              </button>
              
              <input
                type="text"
                placeholder="Type a message..."
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                className="message-input"
              />
              
              <button type="submit" className="send-btn" disabled={!newMessage.trim() && !selectedImage}>
                Send
              </button>
            </form>
          </>
        ) : (
          <div className="no-conversation-selected">
            <h3>Select a conversation</h3>
            <p>Choose from your existing conversations or start a new one</p>
            <button 
              className="start-chat-btn"
              onClick={() => setShowSearch(true)}
            >
              + Start New Conversation
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Chat;
