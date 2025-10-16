<template>
  <div class="min-h-screen flex items-center justify-center relative overflow-hidden animate-gradient-flow bg-gradient-to-br from-purple-600 via-pink-500 to-indigo-600">
    <!-- 动态背景装饰 -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute w-96 h-96 -top-10 -left-10 bg-white/10 rounded-full blur-3xl animate-float"></div>
      <div class="absolute w-96 h-96 -bottom-10 -right-10 bg-purple-300/20 rounded-full blur-3xl animate-float" style="animation-delay: 1s;"></div>
      <div class="absolute w-64 h-64 top-1/2 left-1/3 bg-pink-300/10 rounded-full blur-2xl animate-float" style="animation-delay: 2s;"></div>
    </div>

    <!-- 登录卡片 -->
    <div class="relative z-10 w-full max-w-md px-6 animate-fade-in-scale">
      <!-- 玻璃态卡片 -->
      <div class="glass-effect rounded-3xl shadow-2xl p-8 sm:p-10 border border-white/20">
        <!-- Logo 和标题 -->
        <div class="text-center mb-8 animate-fade-in">
          <div class="inline-block mb-4 animate-bounce-in">
            <div class="w-16 h-16 mx-auto bg-gradient-to-br from-white/30 to-white/10 rounded-2xl flex items-center justify-center shadow-lg">
              <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
              </svg>
            </div>
          </div>
          <h1 class="text-3xl font-bold text-white mb-2 animate-fade-in delay-100">
            欢迎回来
          </h1>
          <p class="text-white/80 animate-fade-in delay-200">
            登录 Hai 心理健康平台
          </p>
        </div>

        <!-- 登录表单 -->
        <form @submit.prevent="handleLogin" class="space-y-6">
          <!-- 用户名输入 -->
          <div class="animate-fade-in delay-300">
            <label class="block text-sm font-medium text-white/90 mb-2">
              用户名
            </label>
            <div class="relative group">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-white/60 group-focus-within:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </div>
              <input
                v-model="username"
                type="text"
                required
                placeholder="请输入用户名"
                class="w-full pl-12 pr-4 py-3.5 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:border-white/40 focus:bg-white/15 transition-all duration-300 input-focus"
              />
            </div>
          </div>

          <!-- 密码输入 -->
          <div class="animate-fade-in delay-400">
            <label class="block text-sm font-medium text-white/90 mb-2">
              密码
            </label>
            <div class="relative group">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-white/60 group-focus-within:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                </svg>
              </div>
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                required
                placeholder="请输入密码"
                class="w-full pl-12 pr-12 py-3.5 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:border-white/40 focus:bg-white/15 transition-all duration-300 input-focus"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute inset-y-0 right-0 pr-4 flex items-center text-white/60 hover:text-white transition-colors"
              >
                <svg v-if="!showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"></path>
                </svg>
              </button>
            </div>
          </div>

          <!-- 错误提示 -->
          <div v-if="errorMessage" class="bg-red-500/20 border border-red-500/30 text-white px-4 py-3 rounded-xl animate-shake">
            <div class="flex items-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              {{ errorMessage }}
            </div>
          </div>

          <!-- 登录按钮 -->
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full py-3.5 bg-white text-purple-600 rounded-xl font-semibold text-lg hover:bg-white/90 focus:outline-none focus:ring-4 focus:ring-white/30 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 shadow-lg hover:shadow-xl button-hover animate-fade-in delay-500"
          >
            <span v-if="!isLoading">登录</span>
            <span v-else class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-purple-600" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              登录中...
            </span>
          </button>
        </form>

        <!-- 注册链接 -->
        <div class="mt-6 text-center animate-fade-in delay-600">
          <p class="text-white/80 text-sm">
            还没有账号？
            <router-link
              to="/register"
              class="text-white font-semibold hover:underline ml-1 transition-all duration-300"
            >
              立即注册
            </router-link>
          </p>
        </div>

        <!-- 测试账号提示 -->
        <div class="mt-6 p-4 bg-white/10 rounded-xl border border-white/20 animate-fade-in delay-700">
          <p class="text-white/80 text-xs text-center">
            💡 测试账号: <span class="font-mono text-white">admin / admin123</span>
          </p>
        </div>
      </div>

      <!-- 底部文字 -->
      <div class="text-center mt-8 animate-fade-in delay-800">
        <p class="text-white/60 text-sm">
          © 2025 Hai 心理健康平台 · 让 AI 成为你的心理健康伙伴
        </p>
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
const showPassword = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')

const handleLogin = async () => {
  errorMessage.value = ''
  isLoading.value = true

  try {
    const data = await userApi.login(username.value, password.value)
    
    if (data && data.user_id) {
      localStorage.setItem('isLoggedIn', 'true')
      localStorage.setItem('user_id', data.user_id)
      localStorage.setItem('username', username.value)
      
      setTimeout(() => {
        router.push('/home')
      }, 500)
    } else {
      errorMessage.value = '登录失败，请检查用户名和密码'
    }
  } catch (error) {
    console.error('登录错误:', error)
    errorMessage.value = error.message || '登录失败，请稍后再试'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* 确保输入框在不同浏览器中的自动填充颜色 */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus {
  -webkit-text-fill-color: white;
  -webkit-box-shadow: 0 0 0px 1000px rgba(255, 255, 255, 0.1) inset;
  transition: background-color 5000s ease-in-out 0s;
}
</style>
