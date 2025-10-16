<template>
  <div class="min-h-screen animate-gradient-flow bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 p-4 sm:p-6 lg:p-8">
    <div class="max-w-7xl mx-auto">
      <!-- 顶部欢迎卡片 - 玻璃态效果 -->
      <div class="glass-effect rounded-3xl shadow-2xl p-6 sm:p-8 mb-8 border border-white/30 animate-fade-in">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <!-- 欢迎文字 -->
          <div class="animate-slide-in-left">
            <h1 class="text-3xl sm:text-4xl font-bold mb-2">
              <span class="gradient-text-purple">欢迎回来</span>
              <span class="text-gray-800">, {{ username }}！</span>
              <span class="inline-block animate-float">👋</span>
            </h1>
            <p class="text-gray-600 text-lg">让我们一起开始今天的健康之旅</p>
          </div>
          
          <!-- 数据统计 -->
          <div class="flex gap-6 animate-slide-in-right">
            <!-- 积分 -->
            <div class="text-center bg-gradient-to-br from-yellow-400 to-orange-500 rounded-2xl p-4 shadow-lg hover:scale-105 transition-transform duration-300">
              <div class="text-3xl font-bold text-white">{{ userPoints }}</div>
              <div class="text-sm text-yellow-50">积分</div>
            </div>
            <!-- 连续打卡 -->
            <div class="text-center bg-gradient-to-br from-green-400 to-emerald-500 rounded-2xl p-4 shadow-lg hover:scale-105 transition-transform duration-300">
              <div class="text-3xl font-bold text-white">{{ checkinStreak }}</div>
              <div class="text-sm text-green-50">天</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 今日状态卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <!-- 今日打卡 -->
        <div class="glass-effect rounded-2xl shadow-xl p-6 border border-white/30 card-hover animate-fade-in delay-100">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-xl font-bold text-gray-800">今日打卡</h3>
            <div class="w-14 h-14 bg-gradient-to-br from-green-400 to-emerald-500 rounded-2xl flex items-center justify-center shadow-lg animate-float">
              <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
          </div>
          <div v-if="todayCheckin" class="space-y-2">
            <div class="flex items-center text-green-600 font-semibold">
              <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
              </svg>
              已打卡
            </div>
            <p class="text-sm text-gray-700"><span class="font-medium">心情:</span> {{ todayCheckin.mood || '未记录' }}</p>
            <p class="text-sm text-gray-700"><span class="font-medium">睡眠:</span> {{ todayCheckin.sleep_hours || '未记录' }}小时</p>
          </div>
          <div v-else>
            <p class="text-gray-600 mb-4">今日还未打卡，记录你的心情吧</p>
            <router-link to="/checkin/daily" class="inline-flex items-center px-4 py-2.5 bg-gradient-to-r from-green-500 to-emerald-500 text-white text-sm font-semibold rounded-xl hover:from-green-600 hover:to-emerald-600 shadow-lg button-hover transition-all">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
              </svg>
              立即打卡
            </router-link>
          </div>
        </div>

        <!-- 心理状态 -->
        <div class="glass-effect rounded-2xl shadow-xl p-6 border border-white/30 card-hover animate-fade-in delay-200">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-xl font-bold text-gray-800">心理状态</h3>
            <div class="w-14 h-14 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-2xl flex items-center justify-center shadow-lg animate-float" style="animation-delay: 0.5s;">
              <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
              </svg>
            </div>
          </div>
          <div v-if="latestPsychTest">
            <p class="text-sm text-gray-600 mb-2 font-medium">{{ latestPsychTest.test_type }} 测评</p>
            <div class="flex items-center justify-between">
              <span class="text-2xl font-bold" :class="getPsychScoreColor(latestPsychTest.score)">
                {{ latestPsychTest.score }}分
              </span>
              <span class="text-xs text-gray-500 bg-gray-100 px-3 py-1 rounded-full">
                {{ formatDate(latestPsychTest.date) }}
              </span>
            </div>
          </div>
          <div v-else>
            <p class="text-gray-600 mb-4">还未进行心理测评</p>
            <router-link to="/psych/choose" class="inline-flex items-center px-4 py-2.5 bg-gradient-to-r from-blue-500 to-indigo-500 text-white text-sm font-semibold rounded-xl hover:from-blue-600 hover:to-indigo-600 shadow-lg button-hover transition-all">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
              </svg>
              开始测评
            </router-link>
          </div>
        </div>

        <!-- AI助手 -->
        <div class="glass-effect rounded-2xl shadow-xl p-6 border border-white/30 card-hover animate-fade-in delay-300">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-xl font-bold text-gray-800">AI助手</h3>
            <div class="w-14 h-14 bg-gradient-to-br from-purple-400 to-pink-500 rounded-2xl flex items-center justify-center shadow-lg animate-float" style="animation-delay: 1s;">
              <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
              </svg>
            </div>
          </div>
          <p class="text-gray-600 mb-4">与专业心理师AI对话，获得专业支持</p>
          <router-link to="/ai/roles" class="inline-flex items-center px-4 py-2.5 bg-gradient-to-r from-purple-500 to-pink-500 text-white text-sm font-semibold rounded-xl hover:from-purple-600 hover:to-pink-600 shadow-lg button-hover transition-all">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
            </svg>
            开始对话
          </router-link>
        </div>
      </div>

      <!-- 功能模块网格 -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
        <!-- 每日打卡 -->
        <router-link to="/checkin/daily" class="glass-effect rounded-2xl shadow-lg p-6 border border-white/30 card-hover cursor-pointer group animate-fade-in delay-400">
          <div class="w-14 h-14 bg-gradient-to-br from-green-400 to-emerald-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg group-hover:scale-110 transition-transform duration-300">
            <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <h3 class="text-center font-bold text-gray-800 mb-2">每日打卡</h3>
          <p class="text-center text-sm text-gray-600">记录心情和睡眠</p>
        </router-link>

        <!-- 心理测评 -->
        <router-link to="/psych/choose" class="glass-effect rounded-2xl shadow-lg p-6 border border-white/30 card-hover cursor-pointer group animate-fade-in delay-500">
          <div class="w-14 h-14 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg group-hover:scale-110 transition-transform duration-300">
            <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
            </svg>
          </div>
          <h3 class="text-center font-bold text-gray-800 mb-2">心理测评</h3>
          <p class="text-center text-sm text-gray-600">专业量表测试</p>
        </router-link>

        <!-- AI对话 -->
        <router-link to="/ai/roles" class="glass-effect rounded-2xl shadow-lg p-6 border border-white/30 card-hover cursor-pointer group animate-fade-in delay-600">
          <div class="w-14 h-14 bg-gradient-to-br from-purple-400 to-pink-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg group-hover:scale-110 transition-transform duration-300">
            <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
            </svg>
          </div>
          <h3 class="text-center font-bold text-gray-800 mb-2">AI对话</h3>
          <p class="text-center text-sm text-gray-600">智能心理咨询</p>
        </router-link>

        <!-- 康复计划 -->
        <router-link to="/plan/profile" class="glass-effect rounded-2xl shadow-lg p-6 border border-white/30 card-hover cursor-pointer group animate-fade-in delay-700">
          <div class="w-14 h-14 bg-gradient-to-br from-orange-400 to-red-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg group-hover:scale-110 transition-transform duration-300">
            <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
          </div>
          <h3 class="text-center font-bold text-gray-800 mb-2">康复计划</h3>
          <p class="text-center text-sm text-gray-600">个性化恢复方案</p>
        </router-link>

        <!-- 积分奖励 -->
        <router-link to="/rewards/points" class="glass-effect rounded-2xl shadow-lg p-6 border border-white/30 card-hover cursor-pointer group animate-fade-in delay-800">
          <div class="w-14 h-14 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg group-hover:scale-110 transition-transform duration-300">
            <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <h3 class="text-center font-bold text-gray-800 mb-2">积分奖励</h3>
          <p class="text-center text-sm text-gray-600">查看积分记录</p>
        </router-link>

        <!-- 退出登录 -->
        <div @click="logout" class="glass-effect rounded-2xl shadow-lg p-6 border border-white/30 card-hover cursor-pointer group animate-fade-in delay-900">
          <div class="w-14 h-14 bg-gradient-to-br from-gray-400 to-gray-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg group-hover:scale-110 transition-transform duration-300">
            <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
            </svg>
          </div>
          <h3 class="text-center font-bold text-gray-800 mb-2">退出登录</h3>
          <p class="text-center text-sm text-gray-600">安全退出系统</p>
        </div>

        <!-- 占位卡片 -->
        <div class="glass-effect rounded-2xl shadow-lg p-6 border border-white/20 opacity-60 animate-fade-in" style="animation-delay: 1s;">
          <div class="w-14 h-14 bg-gray-200 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <svg class="w-7 h-7 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
            </svg>
          </div>
          <h3 class="text-center font-bold text-gray-400 mb-2">更多功能</h3>
          <p class="text-center text-sm text-gray-400">敬请期待</p>
        </div>

        <!-- 占位卡片2 -->
        <div class="glass-effect rounded-2xl shadow-lg p-6 border border-white/20 opacity-60 animate-fade-in" style="animation-delay: 1.1s;">
          <div class="w-14 h-14 bg-gray-200 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <svg class="w-7 h-7 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"></path>
            </svg>
          </div>
          <h3 class="text-center font-bold text-gray-400 mb-2">新功能</h3>
          <p class="text-center text-sm text-gray-400">即将上线</p>
        </div>
      </div>

      <!-- 底部提示 -->
      <div class="mt-8 text-center animate-fade-in" style="animation-delay: 1.2s;">
        <p class="text-gray-500 text-sm">
          💡 每天打卡、完成测评可获得积分奖励
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { rewardsApi, checkinApi, psychApi } from '../api/index.js'

const router = useRouter()
const username = ref(localStorage.getItem('username') || '用户')
const userPoints = ref(0)
const checkinStreak = ref(0)
const todayCheckin = ref(null)
const latestPsychTest = ref(null)

const userId = localStorage.getItem('user_id')

// 获取用户数据
const loadUserData = async () => {
  if (!userId) return

  try {
    // 获取积分
    const pointsData = await rewardsApi.getPoints(userId)
    userPoints.value = pointsData.points

    // 获取打卡历史
    const checkinData = await checkinApi.getHistory(userId)
    if (checkinData.length > 0) {
      const today = new Date().toISOString().split('T')[0]
      todayCheckin.value = checkinData.find(record => record.date === today)
      checkinStreak.value = calculateCheckinStreak(checkinData)
    }

    // 获取最新心理测试
    const psychData = await psychApi.getHistory(userId)
    if (psychData.length > 0) {
      latestPsychTest.value = psychData[0]
    }
  } catch (error) {
    console.error('加载用户数据失败:', error)
  }
}

// 计算连续打卡天数
const calculateCheckinStreak = (checkinData) => {
  if (!checkinData.length) return 0
  
  const today = new Date()
  let streak = 0
  
  for (let i = 0; i < checkinData.length; i++) {
    const recordDate = new Date(checkinData[i].date)
    const diffDays = Math.floor((today - recordDate) / (1000 * 60 * 60 * 24))
    
    if (diffDays === streak) {
      streak++
    } else {
      break
    }
  }
  
  return streak
}

// 获取心理测试分数颜色
const getPsychScoreColor = (score) => {
  if (score < 5) return 'text-green-600'
  if (score < 10) return 'text-yellow-600'
  if (score < 15) return 'text-orange-600'
  return 'text-red-600'
}

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

// 退出登录
const logout = () => {
  localStorage.removeItem('user_id')
  localStorage.removeItem('username')
  localStorage.removeItem('isLoggedIn')
  router.push('/login')
}

onMounted(() => {
  loadUserData()
})
</script>
