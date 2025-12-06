import React, { useState } from 'react'
import { ClipUpload } from '../components/ClipUpload'
import { ClipsView } from '../components/ClipsView'
import { useAuth } from '../context/AuthContext'
import '../styles/clips.css'

export function ClipsPage() {
  const { user } = useAuth()
  const [activeTab, setActiveTab] = useState('feed')
  const [refreshKey, setRefreshKey] = useState(0)

  const handleUploadSuccess = () => {
    // Force refresh of clips
    setRefreshKey(prev => prev + 1)
    setActiveTab('feed')
  }

  return (
    <div className="clips-page">
      <div className="clips-header">
        <h1>📸 Stories</h1>
      </div>

      <div className="clips-tabs">
        <button
          className={`tab ${activeTab === 'feed' ? 'active' : ''}`}
          onClick={() => setActiveTab('feed')}
        >
          📺 Feed
        </button>
        <button
          className={`tab ${activeTab === 'my-clips' ? 'active' : ''}`}
          onClick={() => setActiveTab('my-clips')}
        >
          ✏️ My Stories
        </button>
        <button
          className={`tab ${activeTab === 'upload' ? 'active' : ''}`}
          onClick={() => setActiveTab('upload')}
        >
          📤 Upload
        </button>
      </div>

      <div className="clips-content">
        {activeTab === 'feed' && (
          <ClipsView key={refreshKey} showUserClips={false} />
        )}

        {activeTab === 'my-clips' && (
          <ClipsView key={refreshKey} showUserClips={true} userId={user?.id} />
        )}

        {activeTab === 'upload' && (
          <ClipUpload onUploadSuccess={handleUploadSuccess} />
        )}
      </div>
    </div>
  )
}

export default ClipsPage
