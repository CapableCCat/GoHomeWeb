<template>
  <div id="app">
    <nav class="navbar" v-if="showNav">
      <div class="nav-container">
        <router-link to="/" class="logo">思乡签到</router-link>
        <div class="nav-links">
          <router-link to="/dashboard">首页</router-link>
          <router-link to="/checkin">签到</router-link>
          <router-link to="/badges">勋章</router-link>
          <router-link to="/profile">我的</router-link>
        </div>
      </div>
    </nav>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const showNav = computed(() => !['/login', '/register'].includes(route.path))
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

.logo {
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
