<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
    <!-- 顶部欢迎区域 -->
    <div class="max-w-7xl mx-auto">
      <!-- 用户欢迎信息 -->
      <div class="bg-white rounded-2xl shadow-lg p-6 mb-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 mb-2">
              欢迎回来，{{ username }}！
            </h1>
            <p class="text-gray-600">让我们一起开始今天的健康之旅</p>
          </div>
          <div class="flex items-center space-x-4">
            <div class="text-center">
              <div class="text-2xl font-bold text-indigo-600">{{ userPoints }}</div>
              <div class="text-sm text-gray-500">积分</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-green-600">{{ checkinStreak }}</div>
              <div class="text-sm text-gray-500">连续打卡</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 今日状态卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <!-- 今日打卡 -->
        <div class="bg-white rounded-xl shadow-md p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-800">今日打卡</h3>
            <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
          </div>
          <div v-if="todayCheckin">
            <p class="text-sm text-gray-600 mb-2">已打卡 ✅</p>
            <p class="text-sm text-gray-500">心情: {{ todayCheckin.mood || '未记录' }}</p>
            <p class="text-sm text-gray-500">睡眠: {{ todayCheckin.sleep_hours || '未记录' }}小时</p>
          </div>
          <div v-else>
            <p class="text-sm text-gray-600 mb-3">今日还未打卡</p>
            <router-link to="/checkin/daily" class="inline-flex items-center px-3 py-2 bg-green-600 text-white text-sm rounded-lg hover:bg-green-700 transition-colors">
              立即打卡
            </router-link>
          </div>
        </div>

        <!-- 心理状态 -->
        <div class="bg-white rounded-xl shadow-md p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-800">心理状态</h3>
            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
              </svg>
            </div>
          </div>
          <div v-if="latestPsychTest">
            <p class="text-sm text-gray-600 mb-2">{{ latestPsychTest.test_type }} 测评</p>
            <div class="flex items-center">
              <span class="text-lg font-bold" :class="getPsychScoreColor(latestPsychTest.score)">
                {{ latestPsychTest.score }}分
              </span>
              <span class="text-xs text-gray-500 ml-2">
                {{ formatDate(latestPsychTest.date) }}
              </span>
            </div>
          </div>
          <div v-else>
            <p class="text-sm text-gray-600 mb-3">还未进行心理测评</p>
            <router-link to="/psych/choose" class="inline-flex items-center px-3 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors">
              开始测评
            </router-link>
          </div>
        </div>

        <!-- AI助手 -->
        <div class="bg-white rounded-xl shadow-md p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-800">AI助手</h3>
            <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
              </svg>
            </div>
          </div>
          <p class="text-sm text-gray-600 mb-3">与专业心理师AI对话</p>
          <router-link to="/ai/roles" class="inline-flex items-center px-3 py-2 bg-purple-600 text-white text-sm rounded-lg hover:bg-purple-700 transition-colors">
            开始对话
          </router-link>
        </div>
      </div>

      <!-- 功能模块网格 -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
        <!-- 每日打卡 -->
        <router-link to="/checkin/daily" class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer">
          <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <h3 class="text-center font-semibold text-gray-800 mb-2">每日打卡</h3>
          <p class="text-center text-sm text-gray-600">记录心情和睡眠</p>
        </router-link>

        <!-- 心理测评 -->
        <router-link to="/psych/choose" class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer">
          <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
            </svg>
          </div>
          <h3 class="text-center font-semibold text-gray-800 mb-2">心理测评</h3>
          <p class="text-center text-sm text-gray-600">专业量表测试</p>
        </router-link>

        <!-- AI对话 -->
        <router-link to="/ai/roles" class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer">
          <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
            </svg>
          </div>
          <h3 class="text-center font-semibold text-gray-800 mb-2">AI对话</h3>
          <p class="text-center text-sm text-gray-600">智能心理咨询</p>
        </router-link>

        <!-- 康复计划 -->
        <router-link to="/plan/profile" class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer">
          <div class="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
          </div>
          <h3 class="text-center font-semibold text-gray-800 mb-2">康复计划</h3>
          <p class="text-center text-sm text-gray-600">个性化恢复方案</p>
        </router-link>

        <!-- 积分奖励 -->
        <router-link to="/rewards/points" class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer">
          <div class="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <h3 class="text-center font-semibold text-gray-800 mb-2">积分奖励</h3>
          <p class="text-center text-sm text-gray-600">查看积分记录</p>
        </router-link>

        <!-- 设置 -->
        <div class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer" @click="logout">
          <div class="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
            </svg>
          </div>
          <h3 class="text-center font-semibold text-gray-800 mb-2">退出登录</h3>
          <p class="text-center text-sm text-gray-600">安全退出系统</p>
        </div>

        <!-- 占位卡片 -->
        <div class="bg-gray-50 rounded-xl p-6 opacity-50">
          <div class="w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
            </svg>
          </div>
          <h3 class="text-center font-semibold text-gray-400 mb-2">更多功能</h3>
          <p class="text-center text-sm text-gray-400">敬请期待</p>
        </div>
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

    // 获取打卡历史（用于计算连续打卡天数）
    const checkinData = await checkinApi.getHistory(userId)
    if (checkinData.length > 0) {
      // 检查今天是否已打卡
      const today = new Date().toISOString().split('T')[0]
      todayCheckin.value = checkinData.find(record => record.date === today)
      
      // 计算连续打卡天数（简化版）
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