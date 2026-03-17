import { defineStore } from 'pinia'
import axios from 'axios'

export const useCheckinStore = defineStore('checkin', {
  state: () => ({
    hasCheckedInToday: false,
    consecutiveDays: 0,
    totalDays: 0,
    longestStreak: 0,
    lastCheckinDate: null,
    lastCheckinQuote: null,
    newBadges: []
  }),

  getters: {
    weekCalendar: (state) => {
      // 生成最近 7 天的签到日历
      const today = new Date()
      const days = []
      for (let i = 6; i >= 0; i--) {
        const date = new Date(today)
        date.setDate(date.getDate() - i)
        days.push({
          date: date.toISOString().split('T')[0],
          dayOfWeek: ['日', '一', '二', '三', '四', '五', '六'][date.getDay()],
          checkedIn: false // 需要从服务器获取
        })
      }
      return days
    }
  },

  actions: {
    async doCheckin() {
      try {
        const response = await axios.post('/api/checkin', {}, { withCredentials: true })

        if (response.data.success) {
          const result = response.data
          this.hasCheckedInToday = true
          this.consecutiveDays = result.stats?.current_streak || 0
          this.totalDays = result.stats?.total_days || 0
          this.lastCheckinDate = result.checkin_date
          this.lastCheckinQuote = result.quote
          this.newBadges = result.new_badges || []

          return { success: true, data: result }
        }
        return { success: false, error: response.data.message }
      } catch (error) {
        console.error('Checkin error:', error)
        return { success: false, error: error.response?.data?.message || '签到失败' }
      }
    },

    async fetchCheckinStatus() {
      try {
        const response = await axios.get('/api/checkin/status', { withCredentials: true })
        const data = response.data
        this.hasCheckedInToday = data.has_checked_in_today
        this.consecutiveDays = data.stats?.current_streak || 0
        this.totalDays = data.stats?.total_days || 0
        this.longestStreak = data.stats?.longest_streak || 0
        this.lastCheckinDate = data.last_checkin?.checkin_date
      } catch (error) {
        console.error('Fetch status error:', error)
      }
    },

    clearNewBadges() {
      this.newBadges = []
    }
  }
})
