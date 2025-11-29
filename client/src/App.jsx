import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { GoogleOAuthProvider } from '@react-oauth/google'
import { AuthProvider } from './context/AuthContext'
import { ThemeProvider } from './context/ThemeContext'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Profile from './pages/Profile'
import Home from './pages/Home'
import PrivateRoute from './components/PrivateRoute'
import Navbar from './components/Navbar'

function App() {
  const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID || ''

  return (
    <GoogleOAuthProvider clientId={googleClientId}>
      <Router>
        <ThemeProvider>
          <AuthProvider>
            <div className="app">
              <Navbar />
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<Signup />} />
                <Route path="/home" element={
                  <PrivateRoute>
                    <Home />
                  </PrivateRoute>
                } />
                <Route path="/profile" element={
                  <PrivateRoute>
                    <Profile />
                  </PrivateRoute>
                } />
                <Route path="/" element={<Navigate to="/home" replace />} />
              </Routes>
            </div>
          </AuthProvider>
        </ThemeProvider>
      </Router>
    </GoogleOAuthProvider>
  )
}

export default App
