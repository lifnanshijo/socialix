import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { GoogleLogin } from '@react-oauth/google'
import '../styles/auth.css'

function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { login, loginWithGoogle } = useAuth()
  const navigate = useNavigate()
  const hasGoogleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID && import.meta.env.VITE_GOOGLE_CLIENT_ID !== 'your_google_client_id_here'

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    
    try {
      await login(email, password)
      navigate('/home')
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed')
    }
  }

  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      await loginWithGoogle(credentialResponse.credential)
      navigate('/home')
    } catch (err) {
      setError('Google login failed')
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card card">
        <h1>Login to Social Connect</h1>
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit" className="btn btn-primary">Login</button>
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
          Don't have an account? <Link to="/signup">Sign up</Link>
        </p>
      </div>
    </div>
  )
}

export default Login
