<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>登录</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            type="text"
            id="username"
            v-model="username"
            class="form-input"
            required
            minlength="3"
            placeholder="至少 3 个字符"
          >
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input
            type="password"
            id="password"
            v-model="password"
            class="form-input"
            required
            minlength="6"
            placeholder="至少 6 个字符"
          >
        </div>
        <div class="form-group checkbox-group">
          <label>
            <input type="checkbox" v-model="remember"> 记住我
          </label>
        </div>
        <button type="submit" class="btn btn-primary btn-block">登录</button>
      </form>
      <p class="auth-footer">
        没有账号？<router-link to="/register">立即注册</router-link>
      </p>
      <p v-if="error" class="error-message">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

const username = ref('')
const password = ref('')
const remember = ref(false)
const error = ref('')

const handleLogin = async () => {
  error.value = ''
  const result = await userStore.login(username.value, password.value)

  if (result.success) {
    router.push('/dashboard')
  } else {
    error.value = result.error
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #FAF8F5 0%, #FFF5E6 100%);
}

.auth-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

.auth-card h2 {
  text-align: center;
  color: #F5A623;
  margin-bottom: 24px;
}

.btn-block {
  width: 100%;
  margin-top: 16px;
}

.auth-footer {
  text-align: center;
  margin-top: 20px;
  color: #666;
}

.auth-footer a {
  color: #F5A623;
  text-decoration: none;
}

.checkbox-group {
  display: flex;
  align-items: center;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-weight: normal;
}

.error-message {
  color: #FF6B6B;
  text-align: center;
  margin-top: 16px;
}
</style>
