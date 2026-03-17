<template>
  <div class="family-greeting">
    <div class="greeting-header">
      <span class="family-role">{{ family_role }}</span>
      <span v-if="dialect" class="dialect-tag">{{ dialect }}</span>
    </div>
    <p class="greeting-content">{{ content }}</p>
    <p class="greeting-time">{{ time }}</p>
  </div>
</template>

<script setup>
defineProps({
  family_role: {
    type: String,
    default: '妈妈'
  },
  nickname: {
    type: String,
    default: ''
  },
  content: {
    type: String,
    required: true
  },
  dialect: {
    type: String,
    default: ''
  },
  time: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.family-greeting {
  background: linear-gradient(135deg, #FFF9F0 0%, #FFF5E6 100%);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
}

.greeting-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
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
  margin-bottom: 12px;
}

.greeting-time {
  color: #999;
  font-size: 13px;
  text-align: right;
}
</style>
