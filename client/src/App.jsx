import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { GoogleOAuthProvider } from '@react-oauth/google'
import { AuthProvider } from './context/AuthContext'
import { ThemeProvider } from './context/ThemeContext'
import SplashScreen from './components/SplashScreen'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Profile from './pages/Profile'
import Home from './pages/Home'
import Chat from './pages/Chat'
import Search from './pages/Search'
import Clips from './pages/Clips'
import Notifications from './pages/Notifications'
import UserProfile from './pages/UserProfile'
import ColorPalette from './components/ColorPalette'
import ColorSystemPalette from './components/ColorSystemPalette'
import PrivateRoute from './components/PrivateRoute'
import Navbar from './components/Navbar'
import Sidebar from './components/Sidebar'
import MobileBottomNav from './components/MobileBottomNav'
import './styles/theme.css'
import './styles/index.css'
import './styles/sidebar.css'

function App() {
  const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID || ''
  const [showSplash, setShowSplash] = useState(true)

  return (
    <GoogleOAuthProvider clientId={googleClientId}>
      <Router>
        <ThemeProvider>
          <AuthProvider>
            {showSplash && <SplashScreen onComplete={() => setShowSplash(false)} />}
            <div className="app">
              <Sidebar />
              <Navbar />
              <div style={{ flex: 1, overflow: 'auto' }}>
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
                  <Route path="/profile/:userId" element={
                    <PrivateRoute>
                      <UserProfile />
                    </PrivateRoute>
                  } />
                  <Route path="/chat" element={
                    <PrivateRoute>
                      <Chat />
                    </PrivateRoute>
                  } />
                  <Route path="/search" element={
                    <PrivateRoute>
                      <Search />
                    </PrivateRoute>
                  } />
                  <Route path="/clips" element={
                    <PrivateRoute>
                      <Clips />
                    </PrivateRoute>
                  } />
                  <Route path="/notifications" element={
                    <PrivateRoute>
                      <Notifications />
                    </PrivateRoute>
                  } />
                  <Route path="/colors" element={<ColorPalette />} />
                  <Route path="/color-system" element={<ColorSystemPalette />} />
                  <Route path="/" element={<Navigate to="/home" replace />} />
                </Routes>
              </div>
              <MobileBottomNav />
            </div>
          </AuthProvider>
        </ThemeProvider>
      </Router>
    </GoogleOAuthProvider>
  )
}

export default App
