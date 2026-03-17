<template>
  <div class="badge-card" :class="{ locked: !earned }">
    <div class="badge-icon">{{ icon }}</div>
    <div class="badge-info">
      <h3>{{ name }}</h3>
      <p>{{ description }}</p>
      <p v-if="earned" class="earned-at">获得时间：{{ earned_at }}</p>
      <p v-else class="locked-hint">🔒 未解锁</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  id: {
    type: String,
    required: true
  },
  name: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  icon: {
    type: String,
    default: '⭐'
  },
  earned: {
    type: Boolean,
    default: false
  },
  earned_at: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.badge-card {
  background: linear-gradient(135deg, #FFF9F0 0%, #FFF5E6 100%);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
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

.badge-info h3 {
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
</style>
