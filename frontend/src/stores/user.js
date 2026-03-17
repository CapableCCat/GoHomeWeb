import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user', {
  state: () => ({
    id: null,
    username: '',
    hometown: '',
    current_city: '',
    family_role: '妈妈',
    nickname: '',
    tone_style: '唠叨型',
    isAuthenticated: false
  }),

  getters: {
    isLoggedIn: (state) => state.isAuthenticated
  },

  actions: {
    async login(username, password) {
      try {
        const response = await axios.post('/api/login', { username, password }, {
          withCredentials: true
        })

        if (response.data.success) {
          const user = response.data.user
          this.id = user.id
          this.username = user.username
          this.hometown = user.hometown
          this.current_city = user.current_city
          this.family_role = user.family_role || '妈妈'
          this.nickname = user.nickname || ''
          this.tone_style = user.tone_style || '唠叨型'
          this.isAuthenticated = true

          localStorage.setItem('user_id', user.id)
          localStorage.setItem('username', user.username)

          return { success: true }
        }
        return { success: false, error: response.data.message }
      } catch (error) {
        console.error('Login error:', error)
        return { success: false, error: error.response?.data?.message || '登录失败' }
      }
    },

    async register(userData) {
      try {
        const response = await axios.post('/api/register', userData, {
          withCredentials: true
        })

        if (response.data.success) {
          return { success: true }
        }
        return { success: false, error: response.data.message }
      } catch (error) {
        console.error('Register error:', error)
        return { success: false, error: error.response?.data?.message || '注册失败' }
      }
    },

    async logout() {
      try {
        await axios.get('/api/logout', { withCredentials: true })
      } catch (error) {
        console.error('Logout error:', error)
      }

      this.id = null
      this.username = ''
      this.hometown = ''
      this.current_city = ''
      this.family_role = '妈妈'
      this.nickname = ''
      this.tone_style = '唠叨型'
      this.isAuthenticated = false

      localStorage.removeItem('user_id')
      localStorage.removeItem('username')
    },

    async fetchProfile() {
      try {
        const response = await axios.get('/api/profile', { withCredentials: true })
        const user = response.data.user
        this.id = user.id
        this.username = user.username
        this.hometown = user.hometown
        this.current_city = user.current_city
        this.family_role = user.family_role || '妈妈'
        this.nickname = user.nickname || ''
        this.tone_style = user.tone_style || '唠叨型'
        this.isAuthenticated = true
      } catch (error) {
        console.error('Fetch profile error:', error)
      }
    }
  }
})
