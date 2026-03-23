<template>
  <div class="shop-container">
    <div class="shop-header">
      <h2>道具商城</h2>
      <div class="currency-card">
        <span class="currency-label">我的积分</span>
        <span class="currency-value">🪙 {{ userPoints }}</span>
      </div>
    </div>

    <!-- 商品分类导航 -->
    <div class="category-tabs">
      <button 
        v-for="cat in categories" 
        :key="cat.id" 
        class="tab-btn"
        :class="{ active: currentCategory === cat.id }"
        @click="currentCategory = cat.id"
      >
        {{ cat.name }}
      </button>
    </div>

    <!-- 商品列表 -->
    <div class="item-grid">
      <div v-for="item in filteredItems" :key="item.id" class="item-card">
        <div class="item-preview">
          <div v-if="item.type === 'frame'" class="frame-demo">
            <img src="../assets/default-avatar.svg" class="avatar-small" :style="{ border: `4px solid ${item.color}` }" />
          </div>
          <div v-else class="item-icon">{{ item.icon }}</div>
        </div>
        <div class="item-info">
          <h4 class="item-name">{{ item.name }}</h4>
          <p class="item-desc">{{ item.description }}</p>
          <div class="item-footer">
            <span class="item-price">🪙 {{ item.price }}</span>
            <button 
              class="buy-btn" 
              :disabled="userPoints < item.price"
              @click="handleBuy(item)"
            >
              {{ userPoints >= item.price ? '兑换' : '积分不足' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 补签卡说明 -->
    <div class="shop-notice">
      <p>💡 提示：所有道具均通过签到积分兑换，无需真实充值。</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const userPoints = ref(1250)
const currentCategory = ref('all')

const categories = [
  { id: 'all', name: '全部' },
  { id: 'card', name: '功能卡' },
  { id: 'frame', name: '头像框' },
  { id: 'title', name: '称号' }
]

const items = ref([
  { id: 1, type: 'card', name: '补签卡', description: '可弥补一次漏签记录', price: 500, icon: '🎫', category: 'card' },
  { id: 2, type: 'frame', name: '黄金边框', description: '彰显尊贵身份', price: 1000, color: '#FFD700', category: 'frame' },
  { id: 3, type: 'frame', name: '天空之蓝', description: '清新自然的气息', price: 800, color: '#87CEEB', category: 'frame' },
  { id: 4, type: 'title', name: '思乡游子', description: '佩戴在个人资料页', price: 300, icon: '🏷️', category: 'title' },
  { id: 5, type: 'card', name: '双倍积分卡', description: '下次签到获得双倍积分', price: 200, icon: '✨', category: 'card' },
  { id: 6, type: 'title', name: '签到狂人', description: '连续签到30天可见', price: 2000, icon: '🏆', category: 'title' }
])

const filteredItems = computed(() => {
  if (currentCategory.value === 'all') return items.value
  return items.value.filter(item => item.category === currentCategory.value)
})

const handleBuy = (item) => {
  if (userPoints.value >= item.price) {
    alert(`兑换成功：${item.name}！积分已扣除。`)
    userPoints.value -= item.price
  }
}
</script>

<style scoped>
.shop-container {
  max-width: 900px;
  margin: 0 auto;
}

.shop-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.currency-card {
  background: #fff;
  padding: 8px 20px;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.currency-label {
  font-size: 12px;
  color: #999;
}

.currency-value {
  font-size: 18px;
  font-weight: bold;
  color: #F5A623;
}

.category-tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.tab-btn {
  padding: 8px 16px;
  border-radius: 18px;
  border: 1px solid #ddd;
  background: #fff;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.tab-btn.active {
  background: #F5A623;
  color: #fff;
  border-color: #F5A623;
}

.item-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
}

.item-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  transition: transform 0.2s;
}

.item-card:hover {
  transform: translateY(-4px);
}

.item-preview {
  height: 120px;
  background: #fcfcfc;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #f0f0f0;
}

.item-icon {
  font-size: 48px;
}

.avatar-small {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.item-info {
  padding: 16px;
}

.item-name {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #333;
}

.item-desc {
  font-size: 13px;
  color: #888;
  height: 36px;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-price {
  font-weight: bold;
  color: #F5A623;
}

.buy-btn {
  background: #F5A623;
  color: #fff;
  border: none;
  padding: 6px 14px;
  border-radius: 15px;
  cursor: pointer;
  font-size: 13px;
}

.buy-btn:disabled {
  background: #ddd;
  cursor: not-allowed;
}

.shop-notice {
  margin-top: 40px;
  text-align: center;
  color: #999;
  font-size: 14px;
}
</style>