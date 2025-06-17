import axios from 'axios';
import config from './config';

const axiosClient = axios.create({
  baseURL:  config.BASE_URL,
  timeout: 20000, // 20 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the token in headers
axiosClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    // Handle request error
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle token refresh
axiosClient.interceptors.response.use(
  res => res,
  async error => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const res = await axios.post('/refresh', {}, { withCredentials: true });

      const newToken = res.data.access_token;
      localStorage.setItem('access_token', newToken);
      originalRequest.headers.Authorization = `Bearer ${newToken}`;

      return axiosClient(originalRequest);
    }
    return Promise.reject(error);
  }
);

export default axiosClient;