<template>
  <div class="badges-container">
    <div class="badges-header">
      <h2>勋章墙</h2>
      <div class="badges-stats">
        <span>已解锁：{{ badgesStore.earnedCount }} / {{ badgesStore.totalCount }}</span>
      </div>
    </div>

    <div v-for="(category, catId) in badgesStore.allDefinitions" :key="catId" class="badge-section">
      <h3>{{ category.name }}</h3>
      <div class="badge-grid">
        <div
          v-for="badgeDef in category.badges"
          :key="badgeDef.id"
          class="badge-card-wrapper"
        >
          <div
            class="badge-card"
            :class="{ 'locked': !isBadgeEarned(badgeDef.id) }"
          >
            <div class="badge-icon">
              {{ getBadgeIcon(badgeDef.id) }}
            </div>
            <div class="badge-info">
              <h4>{{ badgeDef.name }}</h4>
              <p>{{ badgeDef.description }}</p>
              <p v-if="isBadgeEarned(badgeDef.id)" class="earned-at">
                获得时间：{{ getEarnedDate(badgeDef.id) }}
              </p>
              <p v-else class="locked-hint">🔒 未解锁</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="badgesStore.badges.length === 0" class="empty-state">
      <p>还没有获得任何勋章，继续签到解锁吧！</p>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useBadgesStore } from '../stores/badges'

const badgesStore = useBadgesStore()

const earnedBadgesMap = computed(() => {
  const map = {}
  badgesStore.badges.forEach(badge => {
    map[badge.id] = badge.earned_at
  })
  return map
})

const isBadgeEarned = (badgeId) => {
  return !!earnedBadgesMap.value[badgeId]
}

const getEarnedDate = (badgeId) => {
  const earnedAt = earnedBadgesMap.value[badgeId]
  if (!earnedAt) return ''
  return earnedAt.slice(0, 10)
}

const getBadgeIcon = (badgeId) => {
  const iconMap = {
    'day_1': '🌱',
    'day_7': '📅',
    'day_30': '🌙',
    'day_100': '🔄',
    'day_180': '💫',
    'day_365': '🏆',
    'streak_3': '🔥',
    'streak_7': '⚡',
    'streak_15': '🌟',
    'streak_30': '💪',
    'streak_100': '👑',
    'late_night': '🌙',
    'early_bird': '🌅',
    'quote_master': '📝'
  }
  return iconMap[badgeId] || '⭐'
}

onMounted(async () => {
  await badgesStore.fetchBadges()
  await badgesStore.fetchAllDefinitions()
})
</script>

<style scoped>
.badges-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px;
}

.badges-header {
  text-align: center;
  margin-bottom: 32px;
}

.badges-header h2 {
  color: #F5A623;
  margin-bottom: 12px;
}

.badges-stats {
  color: #666;
  font-size: 16px;
}

.badge-section {
  margin-bottom: 32px;
}

.badge-section h3 {
  color: #333;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 2px solid #F5A623;
}

.badge-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.badge-card-wrapper {
  display: flex;
}

.badge-card {
  background: linear-gradient(135deg, #FFF9F0 0%, #FFF5E6 100%);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  width: 100%;
  transition: transform 0.2s, box-shadow 0.2s;
}

.badge-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
}

.badge-card.locked {
  background: #f5f5f5;
  opacity: 0.7;
}

.badge-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.badge-info h4 {
  color: #333;
  font-size: 16px;
  margin-bottom: 8px;
}

.badge-info p {
  color: #666;
  font-size: 13px;
  margin-bottom: 8px;
}

.earned-at {
  color: #4CAF50;
  font-size: 12px;
}

.locked-hint {
  color: #999;
  font-size: 13px;
}

.empty-state {
  text-align: center;
  padding: 48px;
  color: #999;
}
</style>
