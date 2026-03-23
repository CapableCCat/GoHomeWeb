<template>
  <div class="stats-container">
    <h2 class="page-title">统计数据</h2>
    
    <!-- 顶部概览卡片 -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon total">Σ</div>
        <div class="stat-info">
          <span class="label">总签到次数</span>
          <span class="value">{{ totalCheckins }}次</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon streak">🔥</div>
        <div class="stat-info">
          <span class="label">连续签到天数</span>
          <span class="value">{{ currentStreak }}天</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon rate">📊</div>
        <div class="stat-info">
          <span class="label">本月签到率</span>
          <span class="value">{{ monthlyRate }}%</span>
        </div>
      </div>
    </div>

    <!-- 最近 7 天趋势 -->
    <div class="chart-section">
      <h3>最近 7 天签到趋势</h3>
      <div class="trend-chart">
        <div v-for="day in last7Days" :key="day.date" class="bar-item">
          <div class="bar-container">
            <div 
              class="bar" 
              :class="{ 'checked': day.checked }"
              :style="{ height: day.checked ? '100%' : '10%' }"
            ></div>
          </div>
          <span class="day-label">{{ day.label }}</span>
        </div>
      </div>
    </div>

    <!-- 更多详细统计占位 -->
    <div class="details-section">
      <div class="detail-row">
        <span>年度累计签到</span>
        <span class="detail-value">45 天</span>
      </div>
      <div class="detail-row">
        <span>历史最长连续</span>
        <span class="detail-value">12 天</span>
      </div>
      <div class="detail-row">
        <span>平均签到时间</span>
        <span class="detail-value">08:30</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const totalCheckins = ref(45)
const currentStreak = ref(5)
const monthlyRate = ref(85)

const last7Days = ref([
  { date: '03-17', label: '周日', checked: true },
  { date: '03-18', label: '周一', checked: true },
  { date: '03-19', label: '周二', checked: false },
  { date: '03-20', label: '周三', checked: true },
  { date: '03-21', label: '周四', checked: true },
  { date: '03-22', label: '周五', checked: true },
  { date: '03-23', label: '今日', checked: false }
])
</script>

<style scoped>
.stats-container {
  max-width: 800px;
  margin: 0 auto;
}

.page-title {
  margin-bottom: 24px;
  color: #333;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.stat-icon.total { background: #e6f7ff; color: #1890ff; }
.stat-icon.streak { background: #fff7e6; color: #fa8c16; }
.stat-icon.rate { background: #f6ffed; color: #52c41a; }

.stat-info {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 13px;
  color: #888;
}

.value {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.chart-section {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 30px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.chart-section h3 {
  margin-bottom: 20px;
  font-size: 16px;
  color: #333;
}

.trend-chart {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  height: 120px;
  padding: 0 10px;
}

.bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.bar-container {
  width: 12px;
  height: 80px;
  background: #f0f0f0;
  border-radius: 6px;
  overflow: hidden;
  display: flex;
  align-items: flex-end;
}

.bar {
  width: 100%;
  transition: height 0.3s ease;
  background: #d9d9d9;
}

.bar.checked {
  background: #F5A623;
}

.day-label {
  font-size: 12px;
  color: #999;
}

.details-section {
  background: #fff;
  border-radius: 12px;
  padding: 16px 24px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
  font-size: 14px;
  color: #666;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-value {
  font-weight: 500;
  color: #333;
}
</style>