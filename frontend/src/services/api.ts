import axios from 'axios';
import type { AnalysisResult, AnalysisHistoryItem, UserProfile } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach Authorization Token interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('git_intel_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Capture token expiry (401 Unauthorized) interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('git_intel_token');
      localStorage.removeItem('git_intel_auth');
      localStorage.removeItem('git_intel_user');
      // Dispatch a global event to notify the App shell to redirect to login
      window.dispatchEvent(new Event('auth-expired'));
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: async (email: string, usernamePassword?: string) => {
    // Standard OAuth2 Form Body payload or simple JSON payload
    // We send JSON format matching FastAPI expectations
    const response = await api.post('/api/auth/login', {
      email,
      password: usernamePassword || '',
    });
    return response.data; // Expected format: { access_token: string, user: UserProfile }
  },
  register: async (name: string, email: string, usernamePassword?: string) => {
    const response = await api.post('/api/auth/register', {
      name,
      email,
      password: usernamePassword || '',
    });
    return response.data; // Expected format: { access_token: string, user: UserProfile }
  },
};

export const repositoriesAPI = {
  analyze: async (repoUrl: string, saveTrainingRecord: boolean = false): Promise<AnalysisResult> => {
    // Map parameter repo_url according to our backend specification
    const response = await api.post('/api/repositories/analyze', {
      repo_url: repoUrl,
      save_training_record: saveTrainingRecord,
    });
    return response.data;
  },
  getHistory: async (): Promise<AnalysisHistoryItem[]> => {
    const response = await api.get('/api/repositories/history');
    return response.data;
  },
  deleteHistory: async (id: string): Promise<void> => {
    await api.delete(`/api/repositories/history/${id}`);
  },
};

export const usersAPI = {
  getProfile: async (): Promise<UserProfile> => {
    const response = await api.get('/api/users/profile');
    return response.data;
  },
};
