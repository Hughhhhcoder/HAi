<template>
  <div class="flex-center" style="min-height:100vh;background:var(--color-bg-main);padding:2rem;">
    <div style="max-width:900px;width:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0;box-sizing:border-box;" class="login-main-wrap">
      <div class="card" style="width:100%;max-width:400px;margin:auto;position:relative;z-index:2;">
        <div style="display:flex;align-items:center;justify-content:center;margin-bottom:2rem;">
          <img src="/logo.svg" alt="logo" style="height:2.2rem;margin-right:0.5rem;" />
          <span style="font-weight:700;font-size:1.3rem;color:var(--color-text-main);">ghost.</span>
        </div>
        <div class="title text-center">Sign in</div>
        <div class="subtitle text-center mb-4">Welcome back! Please enter your details.</div>
        <button class="btn btn-primary btn-block mb-4" style="display:flex;align-items:center;justify-content:center;gap:0.5em;background:linear-gradient(90deg,#6366f1,#4f46e5);">
          <svg style="width:1.5em;height:1.5em;margin-right:0.5em;" viewBox="0 0 48 48"><g><circle fill="#fff" cx="24" cy="24" r="24"/><path fill="#4285F4" d="M34.6 24.2c0-.7-.1-1.4-.2-2H24v4.1h6c-.3 1.5-1.3 2.7-2.7 3.5v2.9h4.4c2.6-2.4 4.1-5.9 4.1-10.1z"/><path fill="#34A853" d="M24 36c3.6 0 6.6-1.2 8.8-3.2l-4.4-2.9c-1.2.8-2.7 1.3-4.4 1.3-3.4 0-6.2-2.3-7.2-5.3h-4.5v3.1C15.2 33.8 19.3 36 24 36z"/><path fill="#FBBC05" d="M16.8 25.9c-.3-.8-.5-1.7-.5-2.6s.2-1.8.5-2.6v-3.1h-4.5C11.5 20.2 12 22 12 24s-.5 3.8-1.3 5.4l4.5-3.5z"/><path fill="#EA4335" d="M24 17.9c1.9 0 3.6.6 4.9 1.7l3.7-3.7C32.6 13.8 28.6 12 24 12c-4.7 0-8.8 2.2-11.5 5.7l4.5 3.5c1-3 3.8-5.3 7.2-5.3z"/></g></svg>
          <span>Sign in with Google</span>
        </button>
        <div style="display:flex;align-items:center;gap:1em;margin:1.5em 0;">
          <div style="flex:1;height:1px;background:#e5e7eb;"></div>
          <span class="text-sm">or</span>
          <div style="flex:1;height:1px;background:#e5e7eb;"></div>
        </div>
        
        <!-- 错误消息显示 -->
        <div v-if="errorMessage" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
          <p class="text-sm text-red-600">{{ errorMessage }}</p>
        </div>
        
        <!-- 成功消息显示 -->
        <div v-if="successMessage" class="mb-4 p-3 bg-green-50 border border-green-200 rounded-md">
          <p class="text-sm text-green-600">{{ successMessage }}</p>
        </div>
        
        <form @submit.prevent="onLogin">
          <label for="username" class="text-sm mb-2" style="display:block;">Username or Email Address</label>
          <input 
            id="username" 
            v-model="username" 
            class="input mb-4" 
            placeholder="hello@example.com" 
            aria-required="true"
            :disabled="isLoading"
          />
          <div style="display:flex;align-items:center;justify-content:space-between;">
            <label for="password" class="text-sm mb-2">Password</label>
            <a href="#" class="btn-text text-sm" style="font-size:0.95em;">Forgot Password?</a>
          </div>
          <input 
            id="password" 
            v-model="password" 
            type="password" 
            class="input mb-2" 
            placeholder="••••••••" 
            aria-required="true"
            :disabled="isLoading"
          />
          <button 
            type="submit"
            class="btn btn-primary btn-block mt-2" 
            style="background:linear-gradient(90deg,#6366f1,#4f46e5);"
            :disabled="isLoading || !username || !password"
          >
            <span v-if="isLoading">Signing in...</span>
            <span v-else>Sign in</span>
          </button>
        </form>
        <div class="text-center mt-4 text-sm text-gray-600">
          No account? <a href="/register" class="btn-text">Sign up</a>
        </div>
      </div>
      <!-- 右侧插画区（大屏显示） -->
      <div style="flex:1;display:none;align-items:center;justify-content:center;z-index:1;" class="login-illustration-wrap">
        <img src="/illustration.svg" alt="illustration" style="max-width:100%;height:320px;object-fit:contain;filter:drop-shadow(0 8px 32px #c7d2fe88);" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { userApi } from '../api/index.js'

const router = useRouter()
const username = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// 清除消息
const clearMessages = () => {
  errorMessage.value = ''
  successMessage.value = ''
}

// 登录函数
async function onLogin() {
  // 清除之前的消息
  clearMessages()
  
  // 表单验证
  if (!username.value.trim()) {
    errorMessage.value = 'Please enter your username or email'
    return
  }
  
  if (!password.value.trim()) {
    errorMessage.value = 'Please enter your password'
    return
  }
  
  isLoading.value = true
  
  try {
    const data = await userApi.login(username.value.trim(), password.value)
    
    // 登录成功
    successMessage.value = data.msg || 'Login successful!'
    
    // 存储用户信息到localStorage（简单实现）
    localStorage.setItem('user_id', data.user_id)
    localStorage.setItem('username', username.value.trim())
    localStorage.setItem('isLoggedIn', 'true')
    
    // 延迟跳转，让用户看到成功消息
    setTimeout(() => {
      router.push('/home')
    }, 1000)
    
  } catch (error) {
    console.error('Login error:', error)
    errorMessage.value = error.message || 'Login failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
@media (min-width: 900px) {
  .login-main-wrap {
    flex-direction: row !important;
    align-items: stretch !important;
    gap: 2.5rem !important;
  }
  .login-illustration-wrap {
    display: flex !important;
  }
}
</style> 