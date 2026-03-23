<template>
  <div class="calendar-container">
    <div class="calendar-card">
      <div class="calendar-header">
        <h2>签到日历</h2>
        <div class="stats-mini">
          <div class="stat-item">
            <span class="label">连续签到</span>
            <span class="value">{{ streak }}天</span>
          </div>
          <div class="stat-item">
            <span class="label">本月签到</span>
            <span class="value">{{ monthlyCount }}次</span>
          </div>
        </div>
      </div>

      <!-- 日历骨架：后续对接实际日历组件或逻辑 -->
      <div class="calendar-view">
        <div class="month-selector">
          <button class="arrow">&lt;</button>
          <span class="current-month">{{ currentMonthText }}</span>
          <button class="arrow">&gt;</button>
        </div>
        
        <div class="calendar-grid">
          <div class="weekday" v-for="day in weekDays" :key="day">{{ day }}</div>
          <div 
            v-for="n in 31" 
            :key="n" 
            class="day-cell"
            :class="{ 'checked': isChecked(n), 'missed': isMissed(n) }"
          >
            <span class="day-num">{{ n }}</span>
            <div v-if="isChecked(n)" class="check-mark">✓</div>
          </div>
        </div>
      </div>

      <div class="calendar-footer">
        <div class="legend">
          <span class="dot checked"></span> 已签到
          <span class="dot missed"></span> 漏签
        </div>
        <button class="btn-補签" v-if="hasMissed">使用补签卡</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const streak = ref(5)
const monthlyCount = ref(12)
const currentMonthText = ref('2024年3月')
const weekDays = ['日', '一', '二', '三', '四', '五', '六']

// 模拟数据逻辑
const isChecked = (day) => [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 15, 16].includes(day)
const isMissed = (day) => [6, 7, 13, 14].includes(day)
const hasMissed = ref(true)
</script>

<style scoped>
.calendar-container {
  max-width: 800px;
  margin: 0 auto;
}

.calendar-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.stats-mini {
  display: flex;
  gap: 20px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.stat-item .label {
  font-size: 12px;
  color: #999;
}

.stat-item .value {
  font-size: 18px;
  font-weight: bold;
  color: #F5A623;
}

.calendar-view {
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 16px;
}

.month-selector {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}

.weekday {
  text-align: center;
  font-size: 14px;
  color: #999;
  padding-bottom: 8px;
}

.day-cell {
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  background: #f9f9f9;
  position: relative;
  cursor: pointer;
}

.day-cell.checked {
  background: #fff9f0;
  color: #F5A623;
}

.day-cell.missed {
  background: #fff1f0;
}

.day-num {
  font-size: 14px;
}

.check-mark {
  font-size: 12px;
  font-weight: bold;
}

.calendar-footer {
  margin-top: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.legend {
  font-size: 13px;
  color: #666;
}

.dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin: 0 4px 0 12px;
}

.dot.checked { background: #F5A623; }
.dot.missed { background: #ff4d4f; }

.btn-補签 {
  background: #F5A623;
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
}
</style>