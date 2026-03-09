import axios from 'axios';

// updated base URL for production deployment
const API_BASE_URL = 'https://smart-file-organizer-orhn.onrender.com';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const authAPI = {
  sendOTP: (email) => api.post('/auth/send-otp', { email }),
  verifyOTP: (email, otp) => api.post('/auth/verify-otp', { email, otp }),
};

export const fileAPI = {
  scanFiles: (folderPath) => api.post('/scan', { folder_path: folderPath }),
  organizeFiles: (folderPath) => api.post('/organize', { folder_path: folderPath }),
};

export default api;
