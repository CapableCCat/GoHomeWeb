<template>
  <div class="profile-container">
    <div class="profile-card">
      <h2>个人资料</h2>

      <form @submit.prevent="handleSave" class="profile-form">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            type="text"
            id="username"
            v-model="form.username"
            class="form-input"
            disabled
          >
          <p class="form-hint">用户名不可修改</p>
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

        <div class="form-section">
          <h3>家人配置</h3>

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
        </div>

        <button type="submit" class="btn btn-primary btn-block" :disabled="saving">
          {{ saving ? '保存中...' : '保存修改' }}
        </button>
      </form>

      <p v-if="error" class="error-message">{{ error }}</p>
      <p v-if="success" class="success-message">保存成功！</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import { profileAPI } from '../api'

const userStore = useUserStore()

const form = ref({
  username: '',
  hometown: '',
  current_city: '',
  leave_home_date: '',
  family_role: '妈妈',
  nickname: '',
  tone_style: '唠叨型'
})

const saving = ref(false)
const error = ref('')
const success = ref(false)

const handleSave = async () => {
  saving.value = true
  error.value = ''
  success.value = false

  try {
    const response = await profileAPI.update({
      hometown: form.value.hometown,
      current_city: form.value.current_city,
      leave_home_date: form.value.leave_home_date,
      family_role: form.value.family_role,
      nickname: form.value.nickname,
      tone_style: form.value.tone_style
    })

    if (response.data.success) {
      success.value = true
      await userStore.fetchProfile()
    }
  } catch (err) {
    error.value = err.response?.data?.message || '保存失败'
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  await userStore.fetchProfile()
  form.value = {
    username: userStore.username,
    hometown: userStore.hometown || '',
    current_city: userStore.current_city || '',
    leave_home_date: userStore.leave_home_date || '',
    family_role: userStore.family_role || '妈妈',
    nickname: userStore.nickname || '',
    tone_style: userStore.tone_style || '唠叨型'
  }
})
</script>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 24px;
}

.profile-card {
  background: #fff;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.profile-card h2 {
  text-align: center;
  color: #F5A623;
  margin-bottom: 24px;
}

.form-section {
  margin: 32px 0 24px;
  padding-top: 24px;
  border-top: 2px solid #F5A623;
}

.form-section h3 {
  color: #F5A623;
  margin-bottom: 16px;
}

.form-hint {
  color: #999;
  font-size: 12px;
  margin-top: 4px;
}

.btn-block {
  width: 100%;
  margin-top: 24px;
}

.error-message {
  color: #FF6B6B;
  text-align: center;
  margin-top: 16px;
}

.success-message {
  color: #4CAF50;
  text-align: center;
  margin-top: 16px;
}
</style>
