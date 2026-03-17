<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>用户注册</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            type="text"
            id="username"
            v-model="form.username"
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
            v-model="form.password"
            class="form-input"
            required
            minlength="6"
            placeholder="至少 6 个字符"
          >
        </div>
        <div class="form-group">
          <label for="hometown">家乡</label>
          <input
            type="text"
            id="hometown"
            v-model="form.hometown"
            class="form-input"
            placeholder="例如：湖南长沙"
          >
        </div>
        <div class="form-group">
          <label for="current_city">当前城市</label>
          <input
            type="text"
            id="current_city"
            v-model="form.current_city"
            class="form-input"
            placeholder="例如：北京"
          >
        </div>
        <div class="form-group">
          <label for="leave_home_date">离家日期</label>
          <input
            type="date"
            id="leave_home_date"
            v-model="form.leave_home_date"
            class="form-input"
          >
        </div>

        <!-- 家人配置 -->
        <div class="form-group">
          <label for="family_role">家人称呼</label>
          <select id="family_role" v-model="form.family_role" class="form-input">
            <option value="妈妈">妈妈</option>
            <option value="爸爸">爸爸</option>
            <option value="奶奶">奶奶</option>
            <option value="姥姥">姥姥</option>
          </select>
        </div>
        <div class="form-group">
          <label for="nickname">对你的称呼</label>
          <input
            type="text"
            id="nickname"
            v-model="form.nickname"
            class="form-input"
            placeholder="如：娃、闺女"
          >
        </div>
        <div class="form-group">
          <label for="tone_style">语气风格</label>
          <select id="tone_style" v-model="form.tone_style" class="form-input">
            <option value="唠叨型">唠叨型</option>
            <option value="含蓄型">含蓄型</option>
            <option value="直白型">直白型</option>
            <option value="幽默型">幽默型</option>
          </select>
        </div>

        <button type="submit" class="btn btn-primary btn-block">注册</button>
      </form>
      <p class="auth-footer">
        已有账号？<router-link to="/login">立即登录</router-link>
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

const form = ref({
  username: '',
  password: '',
  hometown: '',
  current_city: '',
  leave_home_date: '',
  family_role: '妈妈',
  nickname: '',
  tone_style: '唠叨型'
})

const error = ref('')

const handleRegister = async () => {
  error.value = ''
  const result = await userStore.register(form.value)

  if (result.success) {
    router.push('/login')
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

.error-message {
  color: #FF6B6B;
  text-align: center;
  margin-top: 16px;
}
</style>
