import React, { createContext, useContext, useState, useEffect } from 'react'
import axios from 'axios'

const AuthContext = createContext()
const API_URL = 'http://localhost:5000'

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is logged in on mount
    const token = localStorage.getItem('token')
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      fetchUser()
    } else {
      setLoading(false)
    }
  }, [])

  const fetchUser = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/auth/me`)
      setUser(response.data)
    } catch (err) {
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    } finally {
      setLoading(false)
    }
  }

  const login = async (email, password) => {
    const response = await axios.post(`${API_URL}/api/auth/login`, { email, password })
    const { token, user } = response.data
    localStorage.setItem('token', token)
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    setUser(user)
    return response.data
  }

  const signup = async (username, email, password) => {
    const response = await axios.post(`${API_URL}/api/auth/signup`, { username, email, password })
    const { token, user } = response.data
    localStorage.setItem('token', token)
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    setUser(user)
    return response.data
  }

  const loginWithGoogle = async (credential) => {
    const response = await axios.post(`${API_URL}/api/auth/google`, { credential })
    const { token, user } = response.data
    localStorage.setItem('token', token)
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    setUser(user)
    return response.data
  }

  const logout = () => {
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
    setUser(null)
  }

  const updateProfile = async (profileData, files = {}) => {
    try {
      // If files exist, use FormData with fetch API
      if (Object.keys(files).length > 0) {
        const formData = new FormData()
        
        // Add profile data
        if (profileData.username) formData.append('username', profileData.username)
        if (profileData.bio) formData.append('bio', profileData.bio)
        
        // Add files
        if (files.avatarFile) formData.append('avatar', files.avatarFile)
        if (files.coverFile) formData.append('cover_image', files.coverFile)
        
        const token = localStorage.getItem('token')
        const response = await fetch(`${API_URL}/api/users/profile`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`
          },
          body: formData
        })
        
        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.message || 'Profile update failed')
        }
        
        const updatedUser = await response.json()
        setUser(updatedUser)
        return updatedUser
      } else {
        // For text-only updates, use axios
        const response = await axios.put(`${API_URL}/api/users/profile`, profileData)
        setUser(response.data)
        return response.data
      }
    } catch (err) {
      console.error('Profile update error:', err)
      throw err
    }
  }

  const value = {
    user,
    login,
    signup,
    loginWithGoogle,
    logout,
    updateProfile,
    loading
  }

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  )
}
