<template>
  <div class="min-h-screen flex">
    <!-- 左侧：品牌展示区 (隐藏在移动端) -->
    <div class="hidden lg:flex lg:w-1/2 relative overflow-hidden bg-gradient-to-br from-primary-600 via-primary-700 to-primary-900">
      <!-- 粒子背景效果 -->
      <div class="absolute inset-0">
        <div v-for="i in 20" :key="i"
          class="absolute w-2 h-2 bg-white rounded-full opacity-20"
          :style="{
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            animation: `float ${3 + Math.random() * 4}s ease-in-out ${Math.random() * 2}s infinite`,
            animationDelay: `${Math.random() * 2}s`
          }"
        ></div>
      </div>

      <!-- 内容 -->
      <div class="relative z-10 flex flex-col justify-center items-center w-full px-12 text-white">
        <!-- Logo -->
        <div class="mb-8 animate-bounce-in">
          <div class="w-24 h-24 bg-white/20 backdrop-blur-xl rounded-3xl flex items-center justify-center shadow-2xl">
            <svg class="w-14 h-14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
            </svg>
          </div>
        </div>

        <!-- 标题 -->
        <h1 class="text-5xl font-bold mb-6 text-center animate-fade-in-up" style="animation-delay: 0.1s">
          Hai 心理健康平台
        </h1>
        
        <p class="text-xl text-white/90 text-center mb-12 max-w-md leading-relaxed animate-fade-in-up" style="animation-delay: 0.2s">
          专业的心理评估与AI辅导服务
          <br/>
          让科技成为您的心理健康伙伴
        </p>

        <!-- 特性列表 -->
        <div class="space-y-6 w-full max-w-md">
          <div v-for="(feature, index) in features" :key="index"
            class="flex items-start space-x-4 animate-fade-in-left"
            :style="{ animationDelay: `${0.3 + index * 0.1}s` }"
          >
            <div class="flex-shrink-0 w-12 h-12 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
            </div>
            <div class="flex-1">
              <h3 class="font-semibold text-lg mb-1">{{ feature.title }}</h3>
              <p class="text-white/80 text-sm">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 装饰波浪 -->
      <div class="absolute bottom-0 left-0 right-0">
        <svg viewBox="0 0 1440 320" class="w-full h-auto">
          <path fill="rgba(255, 255, 255, 0.1)" fill-opacity="1" d="M0,96L48,112C96,128,192,160,288,165.3C384,171,480,149,576,133.3C672,117,768,107,864,122.7C960,139,1056,181,1152,186.7C1248,192,1344,160,1392,144L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
        </svg>
      </div>
    </div>

    <!-- 右侧：登录表单区 -->
    <div class="flex-1 flex items-center justify-center px-6 py-12 bg-gradient-to-br from-gray-50 via-white to-gray-100">
      <div class="w-full max-w-md">
        <!-- 移动端Logo -->
        <div class="lg:hidden text-center mb-8">
          <div class="inline-block w-16 h-16 bg-gradient-to-br from-primary-600 to-primary-700 rounded-2xl flex items-center justify-center shadow-xl mb-4">
            <svg class="w-9 h-9 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-gray-900">Hai 心理健康</h2>
        </div>

        <!-- 登录卡片 -->
        <div class="glass-strong rounded-3xl shadow-2xl p-8 sm:p-10 border border-white/50 animate-scale-in">
          <!-- 标题 -->
          <div class="text-center mb-8">
            <h2 class="text-3xl font-bold text-gray-900 mb-2">
              欢迎回来
            </h2>
            <p class="text-gray-600">
              登录您的账号继续使用
            </p>
          </div>

          <!-- 表单 -->
          <form @submit.prevent="handleLogin" class="space-y-6">
            <!-- 用户名 -->
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700 pl-1">
                用户名
              </label>
              <div class="relative group">
                <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-400 group-focus-within:text-primary-600 transition-colors">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                  </svg>
                </div>
                <input
                  v-model="username"
                  type="text"
                  required
                  placeholder="请输入用户名"
                  class="w-full pl-12 pr-4 py-3.5 bg-white/80 border-2 border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:border-primary-500 focus:ring-4 focus:ring-primary-500/20 transition-all duration-300"
                />
              </div>
            </div>

            <!-- 密码 -->
            <div class="space-y-2">
              <div class="flex items-center justify-between pl-1">
                <label class="block text-sm font-medium text-gray-700">
                  密码
                </label>
                <a href="#" class="text-sm text-primary-600 hover:text-primary-700 font-medium">
                  忘记密码?
                </a>
              </div>
              <div class="relative group">
                <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-400 group-focus-within:text-primary-600 transition-colors">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                  </svg>
                </div>
                <input
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  required
                  placeholder="请输入密码"
                  class="w-full pl-12 pr-12 py-3.5 bg-white/80 border-2 border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:border-primary-500 focus:ring-4 focus:ring-primary-500/20 transition-all duration-300"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute inset-y-0 right-0 pr-4 flex items-center text-gray-400 hover:text-gray-600 transition-colors"
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

            <!-- 记住我 -->
            <div class="flex items-center">
              <input
                id="remember"
                v-model="remember"
                type="checkbox"
                class="w-4 h-4 text-primary-600 bg-gray-100 border-gray-300 rounded focus:ring-primary-500 focus:ring-2"
              />
              <label for="remember" class="ml-2 text-sm text-gray-600">
                记住我
              </label>
            </div>

            <!-- 错误提示 -->
            <div v-if="errorMessage" class="bg-danger-50 border-l-4 border-danger-500 text-danger-700 p-4 rounded-lg animate-shake">
              <div class="flex items-center">
                <svg class="w-5 h-5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                </svg>
                <span>{{ errorMessage }}</span>
              </div>
            </div>

            <!-- 登录按钮 -->
            <button
              type="submit"
              :disabled="isLoading"
              class="w-full relative overflow-hidden py-3.5 px-6 bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-primary-500/50 disabled:opacity-50 disabled:cursor-not-allowed transform hover:-translate-y-0.5 active:translate-y-0 transition-all duration-300"
            >
              <span v-if="!isLoading" class="flex items-center justify-center">
                <span>登录</span>
                <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                </svg>
              </span>
              <span v-else class="flex items-center justify-center">
                <svg class="animate-spin h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                登录中...
              </span>
            </button>

            <!-- 分隔线 -->
            <div class="relative my-6">
              <div class="absolute inset-0 flex items-center">
                <div class="w-full border-t border-gray-300"></div>
              </div>
              <div class="relative flex justify-center text-sm">
                <span class="px-4 bg-white/80 text-gray-500">或</span>
              </div>
            </div>

            <!-- 注册链接 -->
            <div class="text-center">
              <p class="text-sm text-gray-600">
                还没有账号?
                <router-link to="/register" class="font-semibold text-primary-600 hover:text-primary-700 transition-colors">
                  立即注册
                </router-link>
              </p>
            </div>
          </form>
        </div>

        <!-- 底部提示 -->
        <div class="mt-8 text-center">
          <p class="text-sm text-gray-500">
            继续即表示您同意我们的
            <a href="#" class="text-primary-600 hover:text-primary-700">服务条款</a>
            和
            <a href="#" class="text-primary-600 hover:text-primary-700">隐私政策</a>
          </p>
        </div>
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
const remember = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')

const features = [
  {
    title: '专业量表评估',
    description: '192题国际标准心理测评系统'
  },
  {
    title: 'AI智能分析',
    description: '自动生成专业心理评估报告'
  },
  {
    title: '个性化辅导',
    description: '10位专业AI心理咨询师'
  },
  {
    title: '长期记忆跟踪',
    description: '持续了解您的心理健康状态'
  }
]

const handleLogin = async () => {
  errorMessage.value = ''
  isLoading.value = true

  try {
    const data = await userApi.login(username.value, password.value)
    
    if (data && data.user_id) {
      localStorage.setItem('isLoggedIn', 'true')
      localStorage.setItem('user_id', data.user_id)
      localStorage.setItem('username', username.value)
      
      // 成功动画后跳转
      setTimeout(() => {
        router.push('/home')
      }, 300)
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
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(168, 85, 247, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(168, 85, 247, 0.5);
}
</style>

