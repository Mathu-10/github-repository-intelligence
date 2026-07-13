import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI, usersAPI } from '../services/api';
import type { UserProfile } from '../types';

interface AuthContextType {
  user: UserProfile | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (email: string, password?: string) => Promise<void>;
  register: (name: string, email: string, password?: string) => Promise<void>;
  logout: () => void;
  updateProfileState: (name: string, email: string) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  // Check if token exists in localStorage on startup
  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('git_intel_token');
      const isAuthSaved = localStorage.getItem('git_intel_auth') === 'true';

      if (token && isAuthSaved) {
        try {
          setIsAuthenticated(true);
          // Attempt to retrieve profile from backend
          const profile = await usersAPI.getProfile();
          setUser(profile);
        } catch (err) {
          console.warn("Failed to retrieve profile, using stored session metadata:", err);
          const savedUser = localStorage.getItem('git_intel_user');
          if (savedUser) {
            setUser(JSON.parse(savedUser));
          }
        }
      }
      setLoading(false);
    };

    initAuth();

    // Event listener to catch token expiry events from Axios response interceptor
    const handleAuthExpired = () => {
      setIsAuthenticated(false);
      setUser(null);
      alert("Your authentication token has expired. Redirecting to login page.");
    };

    window.addEventListener('auth-expired', handleAuthExpired);
    return () => {
      window.removeEventListener('auth-expired', handleAuthExpired);
    };
  }, []);

  const login = async (email: string, password?: string) => {
    setLoading(true);
    try {
      const data = await authAPI.login(email, password);
      // Expected payload format: { access_token: string, user: UserProfile }
      localStorage.setItem('git_intel_token', data.access_token);
      localStorage.setItem('git_intel_auth', 'true');
      localStorage.setItem('git_intel_user', JSON.stringify(data.user));
      setUser(data.user);
      setIsAuthenticated(true);
    } finally {
      setLoading(false);
    }
  };

  const register = async (name: string, email: string, password?: string) => {
    setLoading(true);
    try {
      const data = await authAPI.register(name, email, password);
      localStorage.setItem('git_intel_token', data.access_token);
      localStorage.setItem('git_intel_auth', 'true');
      localStorage.setItem('git_intel_user', JSON.stringify(data.user));
      setUser(data.user);
      setIsAuthenticated(true);
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('git_intel_token');
    localStorage.removeItem('git_intel_auth');
    localStorage.removeItem('git_intel_user');
    setUser(null);
    setIsAuthenticated(false);
  };

  const updateProfileState = (name: string, email: string) => {
    setUser(prev => {
      if (!prev) return null;
      const updated = { ...prev, name, email };
      localStorage.setItem('git_intel_user', JSON.stringify(updated));
      return updated;
    });
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated,
        loading,
        login,
        register,
        logout,
        updateProfileState,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
