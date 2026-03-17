<template>
  <div class="dashboard-container">
    <div class="welcome-card">
      <h2>欢迎回来，{{ userStore.username }}</h2>
      <p class="hometown-info">
        <span v-if="userStore.hometown">家乡：{{ userStore.hometown }}</span>
        <span v-if="userStore.current_city" class="separator">|</span>
        <span v-if="userStore.current_city">当前：{{ userStore.current_city }}</span>
      </p>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">📅</div>
        <div class="stat-value">{{ checkinStore.consecutiveDays }}</div>
        <div class="stat-label">连续签到</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">✅</div>
        <div class="stat-value">{{ checkinStore.totalDays }}</div>
        <div class="stat-label">总签到天数</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🔥</div>
        <div class="stat-value">{{ checkinStore.longestStreak }}</div>
        <div class="stat-label">最长连续</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🏆</div>
        <div class="stat-value">{{ badgesStore.earnedCount }}</div>
        <div class="stat-label">获得勋章</div>
      </div>
    </div>

    <div class="action-card">
      <h3>今日签到</h3>
      <p v-if="checkinStore.hasCheckedInToday" class="checked-in-hint">
        已完成今日签到
      </p>
      <button
        v-else
        @click="handleCheckin"
        class="btn btn-primary btn-large"
        :disabled="checkingIn"
      >
        {{ checkingIn ? '签到中...' : '立即签到' }}
      </button>
    </div>

    <div v-if="checkinStore.newBadges.length > 0" class="new-badges-section">
      <h3>🎉 新解锁勋章</h3>
      <div class="badges-row">
        <div v-for="badge in checkinStore.newBadges" :key="badge.id" class="badge-item">
          <div class="badge-icon">{{ badge.name.split(' ')[0] }}</div>
          <div class="badge-name">{{ badge.name }}</div>
        </div>
      </div>
    </div>

    <div class="family-greeting-card" v-if="lastQuote">
      <div class="greeting-header">
        <span class="family-role">{{ userStore.family_role }}</span>
        <span v-if="lastQuote.dialect" class="dialect-tag">{{ lastQuote.dialect }}</span>
      </div>
      <p class="greeting-content">{{ lastQuote.content }}</p>
    </div>

    <p v-if="error" class="error-message">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import { useCheckinStore } from '../stores/checkin'
import { useBadgesStore } from '../stores/badges'
import { checkinAPI } from '../api'

const userStore = useUserStore()
const checkinStore = useCheckinStore()
const badgesStore = useBadgesStore()

const checkingIn = ref(false)
const error = ref('')
const lastQuote = ref(null)

const handleCheckin = async () => {
  checkingIn.value = true
  error.value = ''

  try {
    const response = await checkinAPI.doCheckin()
    if (response.data.success) {
      await checkinStore.doCheckin()
      await badgesStore.fetchBadges()
      lastQuote.value = response.data.quote
    }
  } catch (err) {
    error.value = err.response?.data?.message || '签到失败，请稍后重试'
  } finally {
    checkingIn.value = false
  }
}

onMounted(async () => {
  await checkinStore.fetchCheckinStatus()
  await badgesStore.fetchBadges()
})
</script>

<style scoped>
.dashboard-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px;
}

.welcome-card {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.welcome-card h2 {
  color: #F5A623;
  margin-bottom: 8px;
}

.hometown-info {
  color: #666;
  font-size: 14px;
}

.separator {
  margin: 0 8px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.stat-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #F5A623;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 13px;
  color: #666;
}

.action-card {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.action-card h3 {
  color: #333;
  margin-bottom: 16px;
}

.btn-large {
  padding: 16px 48px;
  font-size: 18px;
}

.checked-in-hint {
  color: #4CAF50;
  font-size: 16px;
}

.new-badges-section {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.new-badges-section h3 {
  color: #F5A623;
  margin-bottom: 16px;
}

.badges-row {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.badge-item {
  background: #FFF5E6;
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  min-width: 100px;
}

.badge-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.badge-name {
  font-size: 13px;
  color: #666;
}

.family-greeting-card {
  background: linear-gradient(135deg, #FFF9F0 0%, #FFF5E6 100%);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.greeting-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.family-role {
  font-size: 18px;
  font-weight: bold;
  color: #F5A623;
}

.dialect-tag {
  background: #F5A623;
  color: #fff;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
}

.greeting-content {
  color: #333;
  line-height: 1.8;
  font-size: 16px;
}

.error-message {
  color: #FF6B6B;
  text-align: center;
  margin-top: 16px;
}
</style>
