<template>
  <div class="min-h-screen flex items-center justify-center relative overflow-hidden animate-gradient-flow bg-gradient-to-br from-blue-600 via-cyan-500 to-teal-600">
    <!-- 动态背景装饰 -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute w-96 h-96 -top-10 -right-10 bg-white/10 rounded-full blur-3xl animate-float"></div>
      <div class="absolute w-96 h-96 -bottom-10 -left-10 bg-cyan-300/20 rounded-full blur-3xl animate-float" style="animation-delay: 1s;"></div>
      <div class="absolute w-64 h-64 top-1/3 right-1/3 bg-teal-300/10 rounded-full blur-2xl animate-float" style="animation-delay: 2s;"></div>
    </div>

    <!-- 注册卡片 -->
    <div class="relative z-10 w-full max-w-md px-6 animate-fade-in-scale">
      <!-- 玻璃态卡片 -->
      <div class="glass-effect rounded-3xl shadow-2xl p-8 sm:p-10 border border-white/20">
        <!-- Logo 和标题 -->
        <div class="text-center mb-8 animate-fade-in">
          <div class="inline-block mb-4 animate-bounce-in">
            <div class="w-16 h-16 mx-auto bg-gradient-to-br from-white/30 to-white/10 rounded-2xl flex items-center justify-center shadow-lg">
              <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path>
              </svg>
            </div>
          </div>
          <h1 class="text-3xl font-bold text-white mb-2 animate-fade-in delay-100">
            开始你的旅程
          </h1>
          <p class="text-white/80 animate-fade-in delay-200">
            创建 Hai 心理健康账号
          </p>
        </div>

        <!-- 注册表单 -->
        <form @submit.prevent="handleRegister" class="space-y-5">
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
                minlength="3"
                placeholder="3-20个字符"
                class="w-full pl-12 pr-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:border-white/40 focus:bg-white/15 transition-all duration-300 input-focus"
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
                minlength="6"
                placeholder="至少6个字符"
                class="w-full pl-12 pr-12 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:border-white/40 focus:bg-white/15 transition-all duration-300 input-focus"
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

          <!-- 确认密码 -->
          <div class="animate-fade-in delay-500">
            <label class="block text-sm font-medium text-white/90 mb-2">
              确认密码
            </label>
            <div class="relative group">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-white/60 group-focus-within:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <input
                v-model="confirmPassword"
                :type="showPassword ? 'text' : 'password'"
                required
                placeholder="再次输入密码"
                class="w-full pl-12 pr-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:border-white/40 focus:bg-white/15 transition-all duration-300 input-focus"
                :class="{ 'border-red-500/50': confirmPassword && password !== confirmPassword }"
              />
            </div>
            <p v-if="confirmPassword && password !== confirmPassword" class="text-red-300 text-xs mt-2">
              两次密码不一致
            </p>
          </div>

          <!-- 错误/成功提示 -->
          <div v-if="errorMessage" class="bg-red-500/20 border border-red-500/30 text-white px-4 py-3 rounded-xl animate-shake">
            <div class="flex items-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              {{ errorMessage }}
            </div>
          </div>

          <div v-if="successMessage" class="bg-green-500/20 border border-green-500/30 text-white px-4 py-3 rounded-xl">
            <div class="flex items-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              {{ successMessage }}
            </div>
          </div>

          <!-- 注册按钮 -->
          <button
            type="submit"
            :disabled="isLoading || (confirmPassword && password !== confirmPassword)"
            class="w-full py-3.5 bg-white text-blue-600 rounded-xl font-semibold text-lg hover:bg-white/90 focus:outline-none focus:ring-4 focus:ring-white/30 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 shadow-lg hover:shadow-xl button-hover animate-fade-in delay-600"
          >
            <span v-if="!isLoading">注册</span>
            <span v-else class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              注册中...
            </span>
          </button>
        </form>

        <!-- 登录链接 -->
        <div class="mt-6 text-center animate-fade-in delay-700">
          <p class="text-white/80 text-sm">
            已有账号？
            <router-link
              to="/login"
              class="text-white font-semibold hover:underline ml-1 transition-all duration-300"
            >
              立即登录
            </router-link>
          </p>
        </div>
      </div>

      <!-- 底部文字 -->
      <div class="text-center mt-8 animate-fade-in delay-800">
        <p class="text-white/60 text-sm">
          注册即表示您同意我们的服务条款和隐私政策
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
const confirmPassword = ref('')
const showPassword = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const handleRegister = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  if (password.value !== confirmPassword.value) {
    errorMessage.value = '两次密码输入不一致'
    return
  }

  if (password.value.length < 6) {
    errorMessage.value = '密码长度至少6个字符'
    return
  }

  isLoading.value = true

  try {
    const data = await userApi.register(username.value, password.value)
    
    if (data && data.user_id) {
      successMessage.value = '注册成功！正在跳转登录页...'
      setTimeout(() => {
    router.push('/login')
      }, 1500)
    } else {
      errorMessage.value = '注册失败，请稍后再试'
    }
  } catch (error) {
    console.error('注册错误:', error)
    errorMessage.value = error.message || '注册失败，该用户名可能已存在'
  } finally {
    isLoading.value = false
  }
}
</script> 

<style scoped>
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus {
  -webkit-text-fill-color: white;
  -webkit-box-shadow: 0 0 0px 1000px rgba(255, 255, 255, 0.1) inset;
  transition: background-color 5000s ease-in-out 0s;
}
</style>
