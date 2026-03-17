import axios from 'axios'

// 从环境变量读取 API 基础 URL（生产环境使用）
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

// 创建 axios 实例
const api = axios.create({
  baseURL: API_BASE_URL + '/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 响应拦截器
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // 未授权，跳转到登录页
      localStorage.removeItem('user_id')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api

// API 方法
export const authAPI = {
  login: (username, password) => api.post('/login', { username, password }),
  register: (data) => api.post('/register', data),
  logout: () => api.get('/logout'),
  getProfile: () => api.get('/profile')
}

export const checkinAPI = {
  doCheckin: () => api.post('/checkin'),
  getStatus: () => api.get('/checkin/status'),
  getHistory: () => api.get('/checkin/history')
}

export const badgesAPI = {
  getList: () => api.get('/badges'),
  getDefinitions: () => api.get('/badges/definitions')
}

export const profileAPI = {
  get: () => api.get('/profile'),
  update: (data) => api.put('/profile', data)
}
