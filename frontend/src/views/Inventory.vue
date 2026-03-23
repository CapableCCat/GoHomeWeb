<template>
  <div class="inventory-container">
    <h2 class="page-title">我的背包</h2>
    
    <div class="inventory-section">
      <h3><span class="icon">🖼️</span> 头像框</h3>
      <div class="item-grid">
        <div v-for="frame in ownedFrames" :key="frame.id" class="item-card">
          <div class="item-preview" :style="{ borderColor: frame.color }">
            <img src="../assets/default-avatar.svg" />
          </div>
          <span class="item-name">{{ frame.name }}</span>
        </div>
      </div>
    </div>

    <div class="inventory-section">
      <h3><span class="icon">🏷️</span> 称号</h3>
      <div class="item-grid">
        <div v-for="title in ownedTitles" :key="title.id" class="item-card title-card">
          <span class="item-name">{{ title.name }}</span>
        </div>
      </div>
    </div>

    <div class="inventory-section">
      <h3><span class="icon">🎫</span> 功能卡</h3>
      <div class="item-grid">
        <div v-for="card in ownedCards" :key="card.id" class="item-card card-item">
          <div class="card-icon">{{ card.icon }}</div>
          <div class="card-info">
            <span class="item-name">{{ card.name }}</span>
            <span class="item-quantity">数量: {{ card.quantity }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 模拟已拥有的道具数据
const ownedFrames = ref([
  { id: 2, name: '黄金边框', color: '#FFD700' },
  { id: 3, name: '天空之蓝', color: '#87CEEB' }
])

const ownedTitles = ref([
  { id: 4, name: '思乡游子' }
])

const ownedCards = ref([
  { id: 1, name: '补签卡', icon: '🎫', quantity: 2 },
  { id: 5, name: '双倍积分卡', icon: '✨', quantity: 1 }
])
</script>

<style scoped>
.inventory-container {
  max-width: 900px;
  margin: 0 auto;
}

.page-title {
  margin-bottom: 24px;
}

.inventory-section {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.inventory-section h3 {
  margin-top: 0;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.item-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 16px;
}

.item-card {
  background: #fcfcfc;
  border-radius: 8px;
  padding: 12px;
  text-align: center;
  border: 1px solid #f0f0f0;
}

.item-preview {
  width: 50px;
  height: 50px;
  margin: 0 auto 8px;
  border-radius: 50%;
  border: 4px solid #eee;
  padding: 2px;
}

.item-preview img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
}

.item-name {
  font-size: 13px;
  color: #333;
  font-weight: 500;
}

.title-card {
  height: 86px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.card-icon {
  font-size: 24px;
}

.card-info {
  display: flex;
  flex-direction: column;
}

.item-quantity {
  font-size: 12px;
  color: #999;
}
</style>