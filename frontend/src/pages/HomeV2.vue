<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100">
    <!-- 顶部导航栏 -->
    <nav class="glass sticky top-0 z-50 border-b border-gray-200/50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Logo -->
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-gradient-to-br from-primary-600 to-primary-700 rounded-xl flex items-center justify-center shadow-lg">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
              </svg>
            </div>
            <span class="text-xl font-bold text-gradient-primary">Hai</span>
          </div>

          <!-- 用户信息 -->
          <div class="flex items-center space-x-4">
            <!-- 通知 -->
            <button class="relative p-2 hover:bg-gray-100 rounded-xl transition-all">
              <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
              </svg>
              <span class="absolute top-1 right-1 w-2 h-2 bg-danger-500 rounded-full"></span>
            </button>

            <!-- 用户头像 -->
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-gradient-to-br from-primary-400 to-secondary-400 rounded-full flex items-center justify-center shadow-lg">
                <span class="text-white font-semibold">{{ username.charAt(0).toUpperCase() }}</span>
              </div>
              <div class="hidden sm:block">
                <p class="text-sm font-semibold text-gray-900">{{ username }}</p>
                <p class="text-xs text-gray-500">会员</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主内容区 -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 欢迎区域 -->
      <div class="mb-8 animate-fade-in">
        <h1 class="text-4xl font-bold text-gray-900 mb-2">
          你好，{{ username }}！👋
        </h1>
        <p class="text-lg text-gray-600">欢迎回到 Hai 心理健康平台</p>
      </div>

      <!-- 快速统计卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <!-- 积分卡片 -->
        <div class="group animate-fade-in-up" style="animation-delay: 0.1s">
          <div class="glass rounded-2xl p-6 hover:shadow-xl transition-all duration-300 border border-white/50 cursor-pointer transform hover:-translate-y-1">
            <div class="flex items-start justify-between mb-4">
              <div class="w-12 h-12 bg-gradient-to-br from-warning-400 to-warning-500 rounded-xl flex items-center justify-center shadow-lg transform group-hover:scale-110 transition-transform">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <span class="text-xs font-medium text-success-600 bg-success-50 px-2 py-1 rounded-full">
                +12 今日
              </span>
            </div>
            <h3 class="text-3xl font-bold text-gray-900 mb-1">{{ userPoints }}</h3>
            <p class="text-sm text-gray-600">总积分</p>
          </div>
        </div>

        <!-- 连续打卡 -->
        <div class="group animate-fade-in-up" style="animation-delay: 0.2s">
          <div class="glass rounded-2xl p-6 hover:shadow-xl transition-all duration-300 border border-white/50 cursor-pointer transform hover:-translate-y-1">
            <div class="flex items-start justify-between mb-4">
              <div class="w-12 h-12 bg-gradient-to-br from-success-400 to-success-500 rounded-xl flex items-center justify-center shadow-lg transform group-hover:scale-110 transition-transform">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
                </svg>
              </div>
              <span class="text-xs font-medium text-primary-600 bg-primary-50 px-2 py-1 rounded-full">
                连续
              </span>
            </div>
            <h3 class="text-3xl font-bold text-gray-900 mb-1">{{ checkinStreak }} 天</h3>
            <p class="text-sm text-gray-600">连续打卡</p>
          </div>
        </div>

        <!-- 测评完成 -->
        <div class="group animate-fade-in-up" style="animation-delay: 0.3s">
          <div class="glass rounded-2xl p-6 hover:shadow-xl transition-all duration-300 border border-white/50 cursor-pointer transform hover:-translate-y-1">
            <div class="flex items-start justify-between mb-4">
              <div class="w-12 h-12 bg-gradient-to-br from-primary-400 to-primary-500 rounded-xl flex items-center justify-center shadow-lg transform group-hover:scale-110 transition-transform">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                </svg>
              </div>
              <span class="text-xs font-medium text-warning-600 bg-warning-50 px-2 py-1 rounded-full">
                本周
              </span>
            </div>
            <h3 class="text-3xl font-bold text-gray-900 mb-1">3 次</h3>
            <p class="text-sm text-gray-600">心理测评</p>
          </div>
        </div>

        <!-- AI对话 -->
        <div class="group animate-fade-in-up" style="animation-delay: 0.4s">
          <div class="glass rounded-2xl p-6 hover:shadow-xl transition-all duration-300 border border-white/50 cursor-pointer transform hover:-translate-y-1">
            <div class="flex items-start justify-between mb-4">
              <div class="w-12 h-12 bg-gradient-to-br from-secondary-400 to-secondary-500 rounded-xl flex items-center justify-center shadow-lg transform group-hover:scale-110 transition-transform">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                </svg>
              </div>
              <span class="text-xs font-medium text-secondary-600 bg-secondary-50 px-2 py-1 rounded-full">
                活跃
              </span>
            </div>
            <h3 class="text-3xl font-bold text-gray-900 mb-1">28 次</h3>
            <p class="text-sm text-gray-600">AI对话</p>
          </div>
        </div>
      </div>

      <!-- 主要功能区 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <!-- 今日任务 -->
        <div class="lg:col-span-2 animate-fade-in-left">
          <Card variant="glass" padding="lg">
            <template #header>
              <div class="flex items-center justify-between">
                <h2 class="text-2xl font-bold text-gray-900">今日任务</h2>
                <span class="text-sm text-gray-500">{{ new Date().toLocaleDateString('zh-CN') }}</span>
              </div>
            </template>

            <div class="space-y-4">
              <!-- 打卡任务 -->
              <div class="flex items-center p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl border-2 border-green-200 hover:border-green-300 transition-all cursor-pointer group">
                <div class="w-12 h-12 bg-gradient-to-br from-success-500 to-success-600 rounded-xl flex items-center justify-center shadow-lg mr-4 transform group-hover:scale-110 transition-transform">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
                <div class="flex-1">
                  <h3 class="font-semibold text-gray-900 mb-1">每日打卡</h3>
                  <p class="text-sm text-gray-600">记录今天的心情和睡眠质量</p>
                </div>
                <Button v-if="!todayCheckin" variant="success" size="sm" @click="$router.push('/checkin/daily')">
                  立即打卡
                </Button>
                <div v-else class="flex items-center text-success-600">
                  <svg class="w-5 h-5 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="text-sm font-medium">已完成</span>
                </div>
              </div>

              <!-- 测评任务 -->
              <div class="flex items-center p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border-2 border-blue-200 hover:border-blue-300 transition-all cursor-pointer group">
                <div class="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center shadow-lg mr-4 transform group-hover:scale-110 transition-transform">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                  </svg>
                </div>
                <div class="flex-1">
                  <h3 class="font-semibold text-gray-900 mb-1">心理测评</h3>
                  <p class="text-sm text-gray-600">完成一次专业心理评估</p>
                </div>
                <Button variant="primary" size="sm" @click="$router.push('/psych/choose')">
                  开始测评
                </Button>
              </div>

              <!-- AI对话任务 -->
              <div class="flex items-center p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl border-2 border-purple-200 hover:border-purple-300 transition-all cursor-pointer group">
                <div class="w-12 h-12 bg-gradient-to-br from-primary-500 via-primary-600 to-secondary-500 rounded-xl flex items-center justify-center shadow-lg mr-4 transform group-hover:scale-110 transition-transform">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                  </svg>
                </div>
                <div class="flex-1">
                  <h3 class="font-semibold text-gray-900 mb-1">AI心理咨询</h3>
                  <p class="text-sm text-gray-600">与专业AI心理师交流</p>
                </div>
                <Button variant="secondary" size="sm" @click="$router.push('/ai/roles')">
                  开始对话
                </Button>
              </div>
            </div>
          </Card>
        </div>

        <!-- 快速操作 -->
        <div class="animate-fade-in-right">
          <Card variant="glass" padding="lg">
            <template #header>
              <h2 class="text-2xl font-bold text-gray-900">快速操作</h2>
            </template>

            <div class="space-y-3">
              <button @click="$router.push('/checkin/daily')" class="w-full flex items-center p-4 bg-white/50 hover:bg-white rounded-xl transition-all group">
                <div class="w-10 h-10 bg-gradient-to-br from-green-400 to-emerald-500 rounded-lg flex items-center justify-center mr-3">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
                <span class="font-medium text-gray-900 group-hover:text-primary-600 transition-colors">每日打卡</span>
              </button>

              <button @click="$router.push('/psych/choose')" class="w-full flex items-center p-4 bg-white/50 hover:bg-white rounded-xl transition-all group">
                <div class="w-10 h-10 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-lg flex items-center justify-center mr-3">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                  </svg>
                </div>
                <span class="font-medium text-gray-900 group-hover:text-primary-600 transition-colors">心理测评</span>
              </button>

              <button @click="$router.push('/ai/roles')" class="w-full flex items-center p-4 bg-white/50 hover:bg-white rounded-xl transition-all group">
                <div class="w-10 h-10 bg-gradient-to-br from-purple-400 to-pink-500 rounded-lg flex items-center justify-center mr-3">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                  </svg>
                </div>
                <span class="font-medium text-gray-900 group-hover:text-primary-600 transition-colors">AI对话</span>
              </button>

              <button @click="$router.push('/plan/profile')" class="w-full flex items-center p-4 bg-white/50 hover:bg-white rounded-xl transition-all group">
                <div class="w-10 h-10 bg-gradient-to-br from-orange-400 to-red-500 rounded-lg flex items-center justify-center mr-3">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                  </svg>
                </div>
                <span class="font-medium text-gray-900 group-hover:text-primary-600 transition-colors">康复计划</span>
              </button>

              <button @click="$router.push('/rewards/points')" class="w-full flex items-center p-4 bg-white/50 hover:bg-white rounded-xl transition-all group">
                <div class="w-10 h-10 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-lg flex items-center justify-center mr-3">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
                <span class="font-medium text-gray-900 group-hover:text-primary-600 transition-colors">积分奖励</span>
              </button>

              <div class="pt-4 border-t border-gray-200">
                <button @click="logout" class="w-full flex items-center p-4 bg-gray-50 hover:bg-gray-100 rounded-xl transition-all group">
                  <div class="w-10 h-10 bg-gradient-to-br from-gray-400 to-gray-600 rounded-lg flex items-center justify-center mr-3">
                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
                    </svg>
                  </div>
                  <span class="font-medium text-gray-600 group-hover:text-gray-900 transition-colors">退出登录</span>
                </button>
              </div>
            </div>
          </Card>
        </div>
      </div>

      <!-- 最近活动 -->
      <div class="animate-fade-in" style="animation-delay: 0.5s">
        <Card variant="glass" padding="lg">
          <template #header>
            <h2 class="text-2xl font-bold text-gray-900">最近活动</h2>
          </template>

          <div class="space-y-4">
            <div v-for="(activity, index) in recentActivities" :key="index" 
              class="flex items-start p-4 bg-white/50 rounded-xl hover:bg-white transition-all">
              <div :class="[
                'w-10 h-10 rounded-lg flex items-center justify-center mr-4',
                activity.type === 'checkin' ? 'bg-green-100 text-green-600' :
                activity.type === 'test' ? 'bg-blue-100 text-blue-600' :
                activity.type === 'chat' ? 'bg-purple-100 text-purple-600' :
                'bg-gray-100 text-gray-600'
              ]">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path v-if="activity.type === 'checkin'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  <path v-else-if="activity.type === 'test'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                  <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                </svg>
              </div>
              <div class="flex-1">
                <h4 class="font-medium text-gray-900">{{ activity.title }}</h4>
                <p class="text-sm text-gray-600">{{ activity.description }}</p>
                <p class="text-xs text-gray-400 mt-1">{{ activity.time }}</p>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Button from '../components/ui/Button.vue'
import Card from '../components/ui/Card.vue'
import { rewardsApi, checkinApi, psychApi } from '../api/index.js'

const router = useRouter()
const username = ref(localStorage.getItem('username') || '用户')
const userPoints = ref(0)
const checkinStreak = ref(0)
const todayCheckin = ref(null)
const userId = localStorage.getItem('user_id')

const recentActivities = ref([
  {
    type: 'test',
    title: '完成PHQ-9测评',
    description: '抑郁症状评估 - 中度',
    time: '2小时前'
  },
  {
    type: 'chat',
    title: '与温柔心理师对话',
    description: '讨论了工作压力的应对方法',
    time: '5小时前'
  },
  {
    type: 'checkin',
    title: '每日打卡',
    description: '心情：平静 | 睡眠：7小时',
    time: '今天 08:30'
  }
])

const loadUserData = async () => {
  if (!userId) return

  try {
    const pointsData = await rewardsApi.getPoints(userId)
    userPoints.value = pointsData.points

    const checkinData = await checkinApi.getHistory(userId)
    if (checkinData.length > 0) {
      const today = new Date().toISOString().split('T')[0]
      todayCheckin.value = checkinData.find(record => record.date === today)
      checkinStreak.value = calculateCheckinStreak(checkinData)
    }
  } catch (error) {
    console.error('加载用户数据失败:', error)
  }
}

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

