<template>
  <div class="checkin-container">
    <div class="checkin-card">
      <h2>今日签到</h2>

      <div v-if="!hasCheckedIn" class="checkin-action">
        <p class="checkin-hint">点击按钮完成今日签到</p>
        <button
          @click="handleCheckin"
          class="btn btn-primary btn-checkin"
          :disabled="checkingIn"
        >
          {{ checkingIn ? '签到中...' : '签到' }}
        </button>
      </div>

      <div v-else class="checkin-result">
        <div class="success-icon">✅</div>
        <h3>签到成功！</h3>
        <p class="checkin-date">{{ today }}</p>

        <div class="stats-row">
          <div class="stat-item">
            <div class="stat-label">连续签到</div>
            <div class="stat-value">{{ checkinStore.consecutiveDays }} 天</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">总签到</div>
            <div class="stat-value">{{ checkinStore.totalDays }} 天</div>
          </div>
        </div>

        <div v-if="quote" class="quote-card">
          <p class="quote-content">{{ quote.content }}</p>
          <p class="quote-source">—— {{ quote.family_role }}{{ quote.dialect ? ` (${quote.dialect})` : '' }}</p>
        </div>

        <div v-if="newBadges.length > 0" class="badges-section">
          <h4>🎉 解锁新勋章</h4>
          <div class="badges-row">
            <div v-for="badge in newBadges" :key="badge.id" class="badge-card">
              <div class="badge-icon">{{ badge.name.split(' ')[0] }}</div>
              <div class="badge-name">{{ badge.name }}</div>
              <div class="badge-desc">{{ badge.description }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="calendar-section">
        <h3>最近签到</h3>
        <div class="calendar-grid">
          <div
            v-for="day in checkinStore.weekCalendar"
            :key="day.date"
            class="calendar-day"
          >
            <div class="day-date">{{ day.date.slice(8) }}</div>
            <div class="day-week">{{ day.dayOfWeek }}</div>
          </div>
        </div>
      </div>
    </div>

    <p v-if="error" class="error-message">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCheckinStore } from '../stores/checkin'
import { useBadgesStore } from '../stores/badges'
import { checkinAPI } from '../api'

const checkinStore = useCheckinStore()
const badgesStore = useBadgesStore()

const checkingIn = ref(false)
const hasCheckedIn = ref(false)
const error = ref('')
const quote = ref(null)
const newBadges = ref([])

const today = computed(() => {
  const date = new Date()
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
})

const handleCheckin = async () => {
  checkingIn.value = true
  error.value = ''

  try {
    const response = await checkinAPI.doCheckin()
    if (response.data.success) {
      hasCheckedIn.value = true
      quote.value = response.data.quote
      newBadges.value = response.data.new_badges || []
      await checkinStore.doCheckin()
    }
  } catch (err) {
    error.value = err.response?.data?.message || '签到失败'
  } finally {
    checkingIn.value = false
  }
}

onMounted(async () => {
  await checkinStore.fetchCheckinStatus()
  hasCheckedIn.value = checkinStore.hasCheckedInToday
})
</script>

<style scoped>
.checkin-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 24px;
}

.checkin-card {
  background: #fff;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.checkin-card h2 {
  text-align: center;
  color: #F5A623;
  margin-bottom: 24px;
}

.checkin-action {
  text-align: center;
}

.checkin-hint {
  color: #666;
  margin-bottom: 24px;
}

.btn-checkin {
  padding: 16px 64px;
  font-size: 20px;
  font-weight: bold;
}

.checkin-result {
  text-align: center;
}

.success-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.checkin-result h3 {
  color: #F5A623;
  margin-bottom: 8px;
}

.checkin-date {
  color: #999;
  margin-bottom: 24px;
}

.stats-row {
  display: flex;
  justify-content: center;
  gap: 48px;
  margin-bottom: 24px;
}

.stat-item {
  text-align: center;
}

.stat-label {
  color: #666;
  font-size: 14px;
  margin-bottom: 4px;
}

.stat-value {
  color: #F5A623;
  font-size: 24px;
  font-weight: bold;
}

.quote-card {
  background: linear-gradient(135deg, #FFF9F0 0%, #FFF5E6 100%);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
}

.quote-content {
  color: #333;
  line-height: 1.8;
  font-size: 16px;
  margin-bottom: 12px;
}

.quote-source {
  color: #999;
  font-size: 14px;
  text-align: right;
}

.badges-section {
  margin-top: 24px;
}

.badges-section h4 {
  color: #F5A623;
  margin-bottom: 16px;
}

.badges-row {
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

.badge-card {
  background: #FFF5E6;
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  min-width: 120px;
}

.badge-icon {
  font-size: 36px;
  margin-bottom: 8px;
}

.badge-name {
  font-weight: bold;
  color: #333;
  margin-bottom: 4px;
}

.badge-desc {
  font-size: 12px;
  color: #666;
}

.calendar-section {
  margin-top: 32px;
}

.calendar-section h3 {
  text-align: center;
  color: #333;
  margin-bottom: 16px;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}

.calendar-day {
  background: #f5f5f5;
  border-radius: 8px;
  padding: 12px 8px;
  text-align: center;
}

.day-date {
  font-weight: bold;
  color: #333;
  margin-bottom: 4px;
}

.day-week {
  color: #999;
  font-size: 12px;
}

.error-message {
  color: #FF6B6B;
  text-align: center;
  margin-top: 16px;
}
</style>
