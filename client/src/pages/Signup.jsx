import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { GoogleLogin } from '@react-oauth/google'
import '../styles/auth.css'

function Signup() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  })
  const [error, setError] = useState('')
  const { signup, loginWithGoogle } = useAuth()
  const navigate = useNavigate()
  const hasGoogleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID && import.meta.env.VITE_GOOGLE_CLIENT_ID !== 'your_google_client_id_here'

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match')
      return
    }

    try {
      await signup(formData.username, formData.email, formData.password)
      navigate('/home')
    } catch (err) {
      setError(err.response?.data?.message || 'Signup failed')
    }
  }

  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      await loginWithGoogle(credentialResponse.credential)
      navigate('/home')
    } catch (err) {
      setError('Google signup failed')
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card card">
        <h1>Create Account</h1>
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="username"
            placeholder="Username"
            value={formData.username}
            onChange={handleChange}
            required
          />
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            required
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            required
          />
          <input
            type="password"
            name="confirmPassword"
            placeholder="Confirm Password"
            value={formData.confirmPassword}
            onChange={handleChange}
            required
          />
          <button type="submit" className="btn btn-primary">Sign Up</button>
        </form>

        {hasGoogleClientId && (
          <>
            <div className="divider">OR</div>
            <div className="oauth-section">
              <GoogleLogin
                onSuccess={handleGoogleSuccess}
                onError={() => {}}
              />
            </div>
          </>
        )}

        <p className="auth-switch">
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  )
}

export default Signup
