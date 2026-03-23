<template>
  <div id="app">
    <nav class="navbar" v-if="showNav">
      <div class="nav-container">
        <div class="nav-left">
          <img src="./assets/GoHomeLogo.svg" alt="GoHome Icon" class="icon" style="width: 40px; height: 40px;"/>  
          <router-link to="/" class="content">思乡 GoHome</router-link>
        </div>
        <div class="nav-right">
          <div class="nav-links">
            <router-link to="/dashboard">首页</router-link>
            <router-link to="/calendar">签到日历</router-link>
            <router-link to="/stats">统计数据</router-link>
            <router-link to="/store">道具商城</router-link>
          </div>
          <div class="user-menu" @click="toggleDropdown">
            <div class="avatar-wrapper" :style="{ borderColor: userStore.activeFrame }">
              <img src="./assets/default-avatar.svg" alt="User Avatar" class="avatar" />
            </div>
            
            <div v-if="dropdownOpen" class="dropdown-menu">
              <!-- B站风格：顶部个人概览 -->
              <div class="user-overview">
                <div class="user-name-row">
                  <span class="username">{{ userStore.username }}</span>
                  <span v-if="userStore.activeTitle" class="badge-tag">{{ userStore.activeTitle }}</span>
                </div>
                <div class="user-stats">
                  <div class="stat-item">
                    <span class="num">12</span>
                    <span class="label">累签</span>
                  </div>
                  <div class="stat-item">
                    <span class="num">5</span>
                    <span class="label">勋章</span>
                  </div>
                  <div class="stat-item">
                    <span class="num">{{ userStore.points }}</span>
                    <span class="label">积分</span>
                  </div>
                </div>
              </div>

              <!-- 菜单列表 -->
              <div class="menu-list">
                <router-link to="/profile" class="menu-link">
                  <span class="icon">👤</span> 个人中心
                </router-link>
                <router-link to="/badges" class="menu-link">
                  <span class="icon">🏅</span> 我的成就
                </router-link>
                <router-link to="/inventory" class="menu-link">
                  <span class="icon">🎒</span> 我的背包
                </router-link>
                <div class="divider"></div>
                <router-link to="/settings" class="menu-link">
                  <span class="icon">⚙️</span> 设置
                </router-link>
                <a @click.stop="handleLogout" class="menu-link logout">
                  <span class="icon">🚪</span> 退出登录
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const showNav = computed(() => !['/login', '/register'].includes(route.path))

const dropdownOpen = ref(false)

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}

const handleLogout = async () => {
  try {
    await userStore.logout()
    dropdownOpen.value = false
    router.push('/login')
  } catch (error) {
    console.error('Logout failed:', error)
  }
}

const closeDropdown = (e) => {
  if (!e.target.closest('.user-menu')) {
    dropdownOpen.value = false
  }
}

onMounted(() => {
  window.addEventListener('click', closeDropdown)
})

onUnmounted(() => {
  window.removeEventListener('click', closeDropdown)
})
</script>

<style scoped>
#app {
  min-height: 100vh;
  background: #FAF8F5;
}

.navbar {
  background: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.06);
  padding: 12px 0;
}

.nav-container {
  max-width: 960px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-right {
  position: relative;
  display: flex;
  align-items: center;
  gap: 24px;
}

.user-menu {
  position: relative;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.avatar-wrapper {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 2px solid transparent;
  padding: 2px;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.dropdown-menu {
  position: absolute;
  top: 54px;
  left: 50%;
  transform: translateX(-50%);
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  width: 240px;
  z-index: 1000;
  overflow: hidden;
}

/* 概览区 */
.user-overview {
  padding: 20px 16px;
  text-align: center;
  background: linear-gradient(180deg, #fff9f0 0%, #fff 100%);
}

.user-name-row {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  margin-bottom: 16px;
}

.username {
  font-weight: bold;
  font-size: 16px;
  color: #333;
}

.badge-tag {
  font-size: 11px;
  background: #F5A623;
  color: #fff;
  padding: 1px 6px;
  border-radius: 4px;
}

.user-stats {
  display: flex;
  justify-content: space-around;
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.stat-item .num {
  font-weight: bold;
  font-size: 14px;
  color: #333;
}

.stat-item .label {
  font-size: 11px;
  color: #999;
}

/* 列表区 */
.menu-list {
  padding: 8px 0;
}

.menu-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 20px;
  color: #666;
  text-decoration: none;
  font-size: 14px;
  transition: all 0.2s;
}

.menu-link:hover {
  background: #f5f5f5;
  color: #F5A623;
}

.menu-link.logout {
  color: #999;
}

.menu-link.logout:hover {
  background: #fff1f0;
  color: #ff4d4f;
}

.divider {
  height: 1px;
  background: #eee;
  margin: 8px 0;
}

.nav-left {
  display: flex;
  align-items: center;
}

.icon {
  margin-right: 8px;
}

.content {
  font-size: 20px;
  font-weight: bold;
  color: #F5A623;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 24px;
}

.nav-links a {
  color: #333;
  text-decoration: none;
  transition: color 0.2s;
}

.nav-links a:hover {
  color: #F5A623;
}

.main-content {
  max-width: 960px;
  margin: 0 auto;
  padding: 24px 20px;
}
</style>
