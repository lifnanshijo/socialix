import { useState } from 'react'

const API_BASE = 'http://localhost:5000/api/clips'

export function useClips() {
  const [clips, setClips] = useState([])
  const [userClips, setUserClips] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const token = localStorage.getItem('token')

  // Fetch clips from followed users
  const fetchFollowedClips = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${API_BASE}/all`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setClips(data.clips || [])
    } catch (err) {
      setError(err.message)
      console.error('Error fetching clips:', err)
    } finally {
      setLoading(false)
    }
  }

  // Fetch user's own clips
  const fetchUserClips = async (userId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${API_BASE}/user/${userId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setUserClips(data.clips || [])
    } catch (err) {
      setError(err.message)
      console.error('Error fetching user clips:', err)
    } finally {
      setLoading(false)
    }
  }

  // Upload new clip
  const uploadClip = async (file, caption) => {
    setLoading(true)
    setError(null)
    try {
      const formData = new FormData()
      formData.append('clip', file)
      if (caption) {
        formData.append('caption', caption)
      }

      const response = await fetch(`${API_BASE}/upload`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.message || 'Upload failed')
      }

      const data = await response.json()
      return data.clip
    } catch (err) {
      setError(err.message)
      console.error('Error uploading clip:', err)
      throw err
    } finally {
      setLoading(false)
    }
  }

  // Delete clip
  const deleteClip = async (clipId) => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${API_BASE}/${clipId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.error || errorData.message || 'Delete failed')
      }

      // Remove from local state
      setClips(clips.filter(c => c.clip_id !== clipId))
      setUserClips(userClips.filter(c => c.clip_id !== clipId))
    } catch (err) {
      setError(err.message)
      console.error('Error deleting clip:', err)
      throw err
    } finally {
      setLoading(false)
    }
  }

  return {
    clips,
    userClips,
    loading,
    error,
    fetchFollowedClips,
    fetchUserClips,
    uploadClip,
    deleteClip
  }
}
