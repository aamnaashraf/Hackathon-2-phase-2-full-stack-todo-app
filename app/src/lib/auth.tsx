'use client'

import { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { useRouter } from 'next/navigation'
import { login as loginAPI, register as registerAPI, logout as logoutAPI } from './api'
import { useToast } from './toast'

interface User {
  id: string
  email: string
}

interface AuthContextType {
  user: User | null
  loading: boolean
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()
  const { showToast } = useToast()

  useEffect(() => {
    // Check if user is logged in on initial load
    const token = localStorage.getItem('access_token')
    if (token) {
      // In a real app, you might want to validate the token with an API call
      // For now, we'll decode the token to get user info, but more safely
      try {
        // Decode JWT token payload safely
        const tokenParts = token.split('.');
        if (tokenParts.length !== 3) {
          throw new Error('Invalid token format');
        }

        // Decode the payload part (second part)
        let payload = tokenParts[1];
        // Add padding if needed
        payload = payload.replace(/-/g, '+').replace(/_/g, '/');
        while (payload.length % 4) {
          payload += '=';
        }

        const tokenPayload = JSON.parse(atob(payload));
        setUser({
          id: tokenPayload.sub,
          email: tokenPayload.sub // In our implementation, sub is the email
        });
      } catch (error) {
        console.error('Error decoding token:', error);
        localStorage.removeItem('access_token');
        showToast('Session expired. Please log in again.', 'error');
      }
    }
    setLoading(false);
  }, [showToast]);

  const login = async (email: string, password: string) => {
    try {
      const response = await loginAPI(email, password)
      const { access_token, user } = response

      // Store the token in localStorage
      localStorage.setItem('access_token', access_token)

      // Set the user
      setUser(user)

      // Show success message
      showToast('Login successful!', 'success')

      // Redirect to dashboard
      router.push('/dashboard')
    } catch (error: any) {
      console.error('Login error:', error)
      showToast(error.message || 'Login failed. Please try again.', 'error')
      throw error
    }
  }

  const register = async (email: string, password: string) => {
    try {
      const response = await registerAPI(email, password)
      const { access_token, user } = response

      // Store the token in localStorage
      localStorage.setItem('access_token', access_token)

      // Set the user
      setUser(user)

      // Show success message
      showToast('Registration successful!', 'success')

      // Redirect to dashboard
      router.push('/dashboard')
    } catch (error: any) {
      console.error('Registration error:', error)
      showToast(error.message || 'Registration failed. Please try again.', 'error')
      throw error
    }
  }

  const logout = async () => {
    try {
      await logoutAPI()
      setUser(null)
      localStorage.removeItem('access_token')
      showToast('You have been logged out.', 'info')
      router.push('/login')
    } catch (error) {
      console.error('Logout error:', error)
      // Even if the API logout fails, clear the local state
      setUser(null)
      localStorage.removeItem('access_token')
      showToast('You have been logged out.', 'info')
      router.push('/login')
    }
  }

  const value = {
    user,
    loading,
    isAuthenticated: !!user,
    login,
    register,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}