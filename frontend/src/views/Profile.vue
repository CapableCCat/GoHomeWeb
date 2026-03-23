<template>
  <div class="profile-page">
    <div class="profile-layout">
      <!-- 左侧：用户卡片与导航 -->
      <aside class="profile-sidebar">
        <div class="user-info-card">
          <div class="avatar-wrapper" :style="{ borderColor: userStore.activeFrame }">
            <img src="../assets/default-avatar.svg" alt="Avatar" class="main-avatar" />
          </div>
          <div class="user-meta">
            <h3 class="username">{{ userStore.username || '思乡人' }}</h3>
            <span class="user-id">ID: {{ userStore.id || 'GH' + (userStore.username?.length || 1024) }}</span>
            <div v-if="userStore.activeTitle" class="user-title">{{ userStore.activeTitle }}</div>
          </div>
        </div>

        <nav class="side-nav">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            class="nav-item"
            :class="{ active: currentTab === tab.id }"
            @click="currentTab = tab.id"
          >
            <span class="icon">{{ tab.icon }}</span>
            {{ tab.name }}
          </button>
        </nav>
      </aside>

      <!-- 右侧：内容区 -->
      <main class="profile-content">
        <!-- 基本资料 -->
        <div v-if="currentTab === 'basic'" class="content-card">
          <h3>基本资料</h3>
          <form @submit.prevent="saveProfile" class="profile-form">
            <div class="form-row">
              <div class="form-group">
                <label>昵称</label>
                <input v-model="form.nickname" type="text" placeholder="设置你的昵称" />
              </div>
              <div class="form-group">
                <label>家乡</label>
                <input v-model="form.hometown" type="text" placeholder="例如：湖南长沙" />
              </div>
            </div>
            <div class="form-group">
              <label>离家日期</label>
              <input v-model="form.leave_home_date" type="date" />
            </div>
            
            <div class="form-actions">
              <button type="button" class="btn-reset" @click="resetForm">重置</button>
              <button type="submit" class="btn-save">保存修改</button>
              <button type="button" class="btn-clear" @click="clearForm">清空</button>
            </div>
          </form>
        </div>

        <!-- 我的勋章 (从原导航移入) -->
        <div v-if="currentTab === 'badges'" class="content-card">
          <h3>我的勋章</h3>
          <div class="badge-wall">
            <div v-for="badge in myBadges" :key="badge.id" class="badge-item">
              <div class="badge-icon">{{ badge.icon }}</div>
              <span class="badge-name">{{ badge.name }}</span>
              <span class="badge-date">{{ badge.date }} 获得</span>
            </div>
          </div>
        </div>

        <!-- 个性装扮 (对接 Store) -->
        <div v-if="currentTab === 'decor'" class="content-card">
          <h3>个性装扮</h3>
          <div class="decor-section">
            <h4>头像框</h4>
            <div class="decor-grid">
              <div 
                v-for="frame in myFrames" 
                :key="frame.id"
                class="decor-item"
                :class="{ active: userStore.activeFrame === frame.color }"
                @click="useFrame(frame)"
              >
                <div class="frame-preview" :style="{ borderColor: frame.color }">
                  <img src="../assets/default-avatar.svg" />
                </div>
                <span>{{ frame.name }}</span>
              </div>
            </div>

            <h4 style="margin-top: 24px;">称号</h4>
            <div class="decor-grid">
              <div 
                v-for="title in myTitles" 
                :key="title.id"
                class="decor-item"
                :class="{ active: userStore.activeTitle === title.name || (title.id === 0 && !userStore.activeTitle) }"
                @click="useTitle(title)"
              >
                <div class="title-preview">{{ title.name }}</div>
                <span>使用</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 账号设置 -->
        <div v-if="currentTab === 'settings'" class="content-card">
          <h3>账号设置</h3>
          <div class="settings-list">
            <div class="setting-row">
              <div class="info">
                <span>修改密码</span>
                <p>定期更换密码以保障账号安全</p>
              </div>
              <button class="btn-outline">去修改</button>
            </div>
            <div class="setting-row">
              <div class="info">
                <span>注销账号</span>
                <p>永久删除你的账号和所有数据</p>
              </div>
              <button class="btn-danger">申请注销</button>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const currentTab = ref('basic')
const tabs = [
  { id: 'basic', name: '基本资料', icon: '👤' },
  { id: 'badges', name: '我的勋章', icon: '🏅' },
  { id: 'inventory', name: '我的背包', icon: '🎒' },
  { id: 'decor', name: '个性装扮', icon: '🎨' },
  { id: 'settings', name: '账号设置', icon: '⚙️' }
]

// 表单数据
const form = ref({
  nickname: userStore.nickname,
  hometown: userStore.hometown,
  leave_home_date: userStore.leave_home_date
})

const resetForm = () => {
  form.value = {
    nickname: userStore.nickname,
    hometown: userStore.hometown,
    leave_home_date: userStore.leave_home_date
  }
}

const clearForm = () => {
  form.value = {
    nickname: '',
    hometown: '',
    leave_home_date: ''
  }
}

const saveProfile = () => {
  userStore.nickname = form.value.nickname
  userStore.hometown = form.value.hometown
  userStore.leave_home_date = form.value.leave_home_date
  alert('资料保存成功！')
}

// 我的勋章数据
const myBadges = ref([
  { id: 1, name: '初入江湖', icon: '🌱', date: '2024-03-01' },
  { id: 2, name: '连续签到7天', icon: '🔥', date: '2024-03-08' }
])

// 个性装扮数据 (模拟已购买内容)
const myFrames = ref([
  { id: 0, name: '无边框', color: 'transparent' },
  { id: 2, name: '黄金边框', color: '#FFD700' },
  { id: 3, name: '天空之蓝', color: '#87CEEB' }
])

const myTitles = ref([
  { id: 0, name: '无称号' },
  { id: 4, name: '思乡游子' }
])

// 穿戴逻辑 (更新到全局 Store)
const useFrame = (frame) => {
  userStore.activeFrame = frame.color
  alert(`头像框 [${frame.name}] 佩戴成功！`)
}

const useTitle = (title) => {
  userStore.activeTitle = title.id === 0 ? '' : title.name
  alert(`称号 [${title.name}] 使用成功！`)
}
</script>

<style scoped>
.profile-page {
  max-width: 1000px;
  margin: 0 auto;
}

.profile-layout {
  display: flex;
  align-items: flex-start;
  gap: 32px;
}

/* 侧边栏样式 */
.profile-sidebar {
  width: 280px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex-shrink: 0;
}

.user-info-card {
  background: #fff;
  border-radius: 16px;
  padding: 30px 20px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.avatar-wrapper {
  width: 100px;
  height: 100px;
  margin: 0 auto 16px;
  border-radius: 50%;
  border: 4px solid transparent;
  padding: 4px;
  transition: all 0.3s;
}

.main-avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.user-meta h3 { margin: 0; color: #333; }
.user-id { font-size: 12px; color: #999; }
.user-title {
  margin-top: 8px;
  display: inline-block;
  background: #fff7e6;
  color: #fa8c16;
  padding: 2px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.side-nav {
  background: #fff;
  border-radius: 16px;
  padding: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

/* 右侧内容区 */
.profile-content {
  flex: 1; /* 确保右侧占据剩余全部空间 */
  min-width: 0; /* 防止 flex 溢出 */
}

.nav-item {
  width: 100%;
  padding: 12px 16px;
  border: none;
  background: none;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
}

.nav-item:hover { background: #f9f9f9; color: #F5A623; }
.nav-item.active { background: #fff9f0; color: #F5A623; font-weight: bold; }

/* 内容区样式 */
.content-card {
  background: #fff;
  border-radius: 16px;
  padding: 30px;
  min-height: 500px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.content-card h3 { margin-top: 0; margin-bottom: 24px; border-left: 4px solid #F5A623; padding-left: 12px; }

.form-group { margin-bottom: 20px; }
.form-group label { display: block; margin-bottom: 8px; font-size: 14px; color: #666; }
.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  outline: none;
}

.form-actions {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0; /* 增加分割线，让按钮区域更独立 */
}

.btn-save {
  background: #F5A623;
  color: #fff;
  border: none;
  padding: 10px 40px; /* 适当增加宽度 */
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: opacity 0.2s;
  order: 2; /* 确保保存按钮在中间 */
}

.btn-save:hover { opacity: 0.9; }

.btn-reset {
  background: #fff;
  color: #666;
  border: 1px solid #ddd;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  order: 1;
}

.btn-reset:hover { background: #f9f9f9; }

.btn-clear {
  background: #fff;
  color: #ff4d4f;
  border: 1px solid #ffccc7;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  order: 3;
}

.btn-clear:hover { background: #fff1f0; }

/* 勋章墙 */
.badge-wall {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 20px;
}

.badge-item {
  text-align: center;
  padding: 16px;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
}

.badge-icon { font-size: 32px; margin-bottom: 8px; }
.badge-name { display: block; font-size: 13px; color: #333; font-weight: bold; }
.badge-date { font-size: 11px; color: #999; }

/* 装扮格 */
.decor-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 16px;
}

.decor-item {
  text-align: center;
  padding: 12px;
  border: 2px solid transparent;
  border-radius: 12px;
  background: #fcfcfc;
  cursor: pointer;
  transition: all 0.2s;
}

.decor-item.active { border-color: #F5A623; background: #fff9f0; }

.frame-preview {
  width: 50px;
  height: 50px;
  margin: 0 auto 8px;
  border-radius: 50%;
  border: 4px solid #eee;
  padding: 2px;
}

.frame-preview img { width: 100%; height: 100%; border-radius: 50%; }

.title-preview {
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #fa8c16;
  font-weight: bold;
}

/* 账号设置 */
.settings-list { display: flex; flex-direction: column; gap: 16px; }
.setting-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #fcfcfc;
  border-radius: 12px;
}

.setting-row .info p { margin: 4px 0 0; font-size: 12px; color: #999; }
.btn-outline { border: 1px solid #ddd; background: #fff; padding: 6px 16px; border-radius: 6px; cursor: pointer; }
.btn-danger { background: #fff1f0; color: #ff4d4f; border: 1px solid #ffccc7; padding: 6px 16px; border-radius: 6px; cursor: pointer; }
</style>