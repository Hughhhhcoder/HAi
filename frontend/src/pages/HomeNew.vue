<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
    <!-- 顶部导航栏 -->
    <nav class="sticky top-0 z-50 glass border-b border-white/20 backdrop-blur-xl">
      <div class="container-custom">
        <div class="flex items-center justify-between h-16">
          <!-- Logo 和品牌 -->
          <div class="flex items-center space-x-4">
            <div 
              v-motion
              :initial="{ scale: 0, rotate: -180 }"
              :enter="{ scale: 1, rotate: 0, transition: { type: 'spring', stiffness: 200 } }"
              class="w-10 h-10 bg-gradient-to-br from-primary-600 to-secondary-600 rounded-xl flex items-center justify-center shadow-lg cursor-pointer hover:scale-110 transition-transform"
            >
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
              </svg>
            </div>
            <span class="text-xl font-bold text-gradient-primary">Hai</span>
          </div>

          <!-- 右侧功能 -->
          <div class="flex items-center space-x-4">
            <!-- 通知 -->
            <button 
              class="relative p-2 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-700 transition-all group"
              @click="showNotifications = !showNotifications"
            >
              <svg class="w-6 h-6 text-gray-600 dark:text-gray-300 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
              </svg>
              <span class="absolute top-1 right-1 w-2 h-2 bg-danger-500 rounded-full animate-pulse"></span>
            </button>

            <!-- 用户头像 -->
            <div class="flex items-center space-x-3 cursor-pointer group">
              <div class="w-10 h-10 bg-gradient-to-br from-primary-400 to-secondary-400 rounded-full flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform">
                <span class="text-white font-semibold text-sm">{{ username.charAt(0).toUpperCase() }}</span>
              </div>
              <div class="hidden sm:block">
                <p class="text-sm font-semibold text-gray-900 dark:text-white">{{ username }}</p>
                <p class="text-xs text-gray-500 dark:text-gray-400">会员</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主内容区 -->
    <main class="container-custom py-8">
      <!-- 欢迎区域 -->
      <div 
        v-motion
        :initial="{ opacity: 0, y: -20 }"
        :enter="{ opacity: 1, y: 0, transition: { duration: 600 } }"
        class="mb-8"
      >
        <h1 class="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-2">
          你好，<span class="text-gradient-primary">{{ username }}</span>！👋
        </h1>
        <p class="text-lg text-gray-600 dark:text-gray-300">
          {{ getGreeting() }}，今天是 {{ getCurrentDate() }}
        </p>
      </div>

      <!-- 数据统计卡片 -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <!-- 积分卡片 -->
        <div
          v-motion
          :initial="{ opacity: 0, y: 50 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 100, duration: 500 } }"
          class="group relative overflow-hidden"
        >
          <div class="glass-card card-hover p-6 relative z-10">
            <div class="flex items-start justify-between mb-4">
              <div class="w-14 h-14 bg-gradient-to-br from-warning-400 to-warning-600 rounded-2xl flex items-center justify-center shadow-xl transform group-hover:scale-110 group-hover:rotate-12 transition-all duration-300">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <span class="badge badge-success animate-pulse">+12</span>
            </div>
            <h3 class="text-3xl font-bold text-gray-900 dark:text-white mb-1 group-hover:scale-105 transition-transform">
              {{ userPoints }}
            </h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">总积分</p>
            
            <!-- 进度条 -->
            <div class="mt-4 progress-bar">
              <div class="progress-bar-fill" :style="{ width: `${(userPoints % 100)}%` }"></div>
            </div>
          </div>
          <!-- 装饰性背景 -->
          <div class="absolute inset-0 bg-gradient-to-br from-warning-500/10 to-orange-500/10 rounded-3xl transform group-hover:scale-105 transition-transform"></div>
        </div>

        <!-- 连续打卡 -->
        <div
          v-motion
          :initial="{ opacity: 0, y: 50 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 200, duration: 500 } }"
          class="group relative overflow-hidden"
        >
          <div class="glass-card card-hover p-6 relative z-10">
            <div class="flex items-start justify-between mb-4">
              <div class="w-14 h-14 bg-gradient-to-br from-success-400 to-success-600 rounded-2xl flex items-center justify-center shadow-xl transform group-hover:scale-110 group-hover:-rotate-12 transition-all duration-300">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
                </svg>
              </div>
              <span class="badge badge-primary">连续</span>
            </div>
            <h3 class="text-3xl font-bold text-gray-900 dark:text-white mb-1 group-hover:scale-105 transition-transform">
              {{ checkinStreak }} 天
            </h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">连续打卡</p>
            
            <!-- 火焰图标 -->
            <div class="mt-4 flex space-x-1">
              <div v-for="i in Math.min(checkinStreak, 7)" :key="i" class="w-2 h-6 bg-gradient-to-t from-warning-500 to-danger-500 rounded-full animate-pulse" :style="{ animationDelay: `${i * 100}ms` }"></div>
            </div>
          </div>
          <div class="absolute inset-0 bg-gradient-to-br from-success-500/10 to-emerald-500/10 rounded-3xl transform group-hover:scale-105 transition-transform"></div>
        </div>

        <!-- 测评完成 -->
        <div
          v-motion
          :initial="{ opacity: 0, y: 50 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 300, duration: 500 } }"
          class="group relative overflow-hidden"
        >
          <div class="glass-card card-hover p-6 relative z-10">
            <div class="flex items-start justify-between mb-4">
              <div class="w-14 h-14 bg-gradient-to-br from-primary-400 to-primary-600 rounded-2xl flex items-center justify-center shadow-xl transform group-hover:scale-110 group-hover:rotate-12 transition-all duration-300">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                </svg>
              </div>
              <span class="badge badge-warning">本周</span>
            </div>
            <h3 class="text-3xl font-bold text-gray-900 dark:text-white mb-1 group-hover:scale-105 transition-transform">
              3 次
            </h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">心理测评</p>
            
            <!-- 迷你图表 -->
            <div class="mt-4 flex items-end space-x-1 h-6">
              <div class="w-full bg-primary-200 rounded-t" style="height: 40%"></div>
              <div class="w-full bg-primary-300 rounded-t" style="height: 60%"></div>
              <div class="w-full bg-primary-400 rounded-t" style="height: 80%"></div>
              <div class="w-full bg-primary-500 rounded-t" style="height: 100%"></div>
              <div class="w-full bg-primary-600 rounded-t" style="height: 70%"></div>
            </div>
          </div>
          <div class="absolute inset-0 bg-gradient-to-br from-primary-500/10 to-secondary-500/10 rounded-3xl transform group-hover:scale-105 transition-transform"></div>
        </div>

        <!-- AI对话 -->
        <div
          v-motion
          :initial="{ opacity: 0, y: 50 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 400, duration: 500 } }"
          class="group relative overflow-hidden"
        >
          <div class="glass-card card-hover p-6 relative z-10">
            <div class="flex items-start justify-between mb-4">
              <div class="w-14 h-14 bg-gradient-to-br from-secondary-400 to-secondary-600 rounded-2xl flex items-center justify-center shadow-xl transform group-hover:scale-110 group-hover:-rotate-12 transition-all duration-300">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                </svg>
              </div>
              <span class="badge bg-secondary-100 text-secondary-700 animate-pulse">活跃</span>
            </div>
            <h3 class="text-3xl font-bold text-gray-900 dark:text-white mb-1 group-hover:scale-105 transition-transform">
              28 次
            </h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">AI对话</p>
            
            <!-- 脉冲点 -->
            <div class="mt-4 flex space-x-2">
              <div class="w-3 h-3 bg-secondary-500 rounded-full animate-pulse"></div>
              <div class="w-3 h-3 bg-secondary-400 rounded-full animate-pulse" style="animation-delay: 0.2s"></div>
              <div class="w-3 h-3 bg-secondary-300 rounded-full animate-pulse" style="animation-delay: 0.4s"></div>
            </div>
          </div>
          <div class="absolute inset-0 bg-gradient-to-br from-secondary-500/10 to-cyan-500/10 rounded-3xl transform group-hover:scale-105 transition-transform"></div>
        </div>
      </div>

      <!-- 主要内容区 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <!-- 今日任务 (2/3 宽度) -->
        <div 
          v-motion
          :initial="{ opacity: 0, x: -50 }"
          :enter="{ opacity: 1, x: 0, transition: { delay: 500, duration: 600 } }"
          class="lg:col-span-2"
        >
          <div class="glass-card p-6">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-2xl font-bold text-gray-900 dark:text-white">今日任务</h2>
              <span class="text-sm text-gray-500">{{ taskCompletionRate }}% 完成</span>
            </div>

            <div class="space-y-4">
              <!-- 打卡任务 -->
              <div 
                class="group relative p-5 bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 rounded-2xl border-2 border-green-200 dark:border-green-800 hover:border-green-300 dark:hover:border-green-700 transition-all cursor-pointer transform hover:scale-[1.02]"
                @click="navigateTo('/checkin/daily')"
              >
                <div class="flex items-center">
                  <div class="w-12 h-12 bg-gradient-to-br from-success-500 to-success-600 rounded-xl flex items-center justify-center shadow-lg mr-4 transform group-hover:scale-110 group-hover:rotate-6 transition-all">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                  </div>
                  <div class="flex-1">
                    <h3 class="font-semibold text-gray-900 dark:text-white mb-1">每日打卡</h3>
                    <p class="text-sm text-gray-600 dark:text-gray-400">记录今天的心情和睡眠质量</p>
                  </div>
                  <div v-if="!todayCheckin" class="btn btn-ghost btn-sm">
                    立即打卡
                  </div>
                  <div v-else class="flex items-center text-success-600">
                    <svg class="w-5 h-5 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                    </svg>
                    <span class="text-sm font-medium">已完成</span>
                  </div>
                </div>
              </div>

              <!-- 测评任务 -->
              <div 
                class="group relative p-5 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-2xl border-2 border-blue-200 dark:border-blue-800 hover:border-blue-300 dark:hover:border-blue-700 transition-all cursor-pointer transform hover:scale-[1.02]"
                @click="navigateTo('/psych/choose')"
              >
                <div class="flex items-center">
                  <div class="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center shadow-lg mr-4 transform group-hover:scale-110 group-hover:-rotate-6 transition-all">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                    </svg>
                  </div>
                  <div class="flex-1">
                    <h3 class="font-semibold text-gray-900 dark:text-white mb-1">心理测评</h3>
                    <p class="text-sm text-gray-600 dark:text-gray-400">完成一次专业心理评估</p>
                  </div>
                  <div class="btn btn-primary btn-sm">
                    开始测评
                  </div>
                </div>
              </div>

              <!-- AI对话任务 -->
              <div 
                class="group relative p-5 bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 rounded-2xl border-2 border-purple-200 dark:border-purple-800 hover:border-purple-300 dark:hover:border-purple-700 transition-all cursor-pointer transform hover:scale-[1.02]"
                @click="navigateTo('/ai/roles')"
              >
                <div class="flex items-center">
                  <div class="w-12 h-12 bg-gradient-to-br from-primary-500 via-primary-600 to-secondary-500 rounded-xl flex items-center justify-center shadow-lg mr-4 transform group-hover:scale-110 group-hover:rotate-6 transition-all">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                    </svg>
                  </div>
                  <div class="flex-1">
                    <h3 class="font-semibold text-gray-900 dark:text-white mb-1">AI心理咨询</h3>
                    <p class="text-sm text-gray-600 dark:text-gray-400">与专业AI心理师交流</p>
                  </div>
                  <div class="btn btn-secondary btn-sm">
                    开始对话
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 快速操作 (1/3 宽度) -->
        <div 
          v-motion
          :initial="{ opacity: 0, x: 50 }"
          :enter="{ opacity: 1, x: 0, transition: { delay: 500, duration: 600 } }"
        >
          <div class="glass-card p-6">
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">快速操作</h2>

            <div class="space-y-3">
              <button 
                v-for="action in quickActions" 
                :key="action.path"
                @click="navigateTo(action.path)"
                class="w-full flex items-center p-4 bg-white/50 dark:bg-gray-800/50 hover:bg-white dark:hover:bg-gray-700 rounded-xl transition-all group transform hover:scale-105"
              >
                <div :class="action.iconClass" class="w-10 h-10 rounded-lg flex items-center justify-center mr-3 transform group-hover:scale-110 group-hover:rotate-6 transition-all">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="action.iconPath"></path>
                  </svg>
                </div>
                <span class="font-medium text-gray-900 dark:text-white group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                  {{ action.label }}
                </span>
              </button>

              <!-- 退出登录 -->
              <div class="pt-4 border-t border-gray-200 dark:border-gray-700">
                <button 
                  @click="logout"
                  class="w-full flex items-center p-4 bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-xl transition-all group transform hover:scale-105"
                >
                  <div class="w-10 h-10 bg-gradient-to-br from-gray-400 to-gray-600 rounded-lg flex items-center justify-center mr-3 transform group-hover:scale-110 transition-transform">
                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
                    </svg>
                  </div>
                  <span class="font-medium text-gray-600 dark:text-gray-300 group-hover:text-gray-900 dark:group-hover:text-white transition-colors">
                    退出登录
                  </span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 最近活动 -->
      <div 
        v-motion
        :initial="{ opacity: 0, y: 50 }"
        :enter="{ opacity: 1, y: 0, transition: { delay: 600, duration: 600 } }"
      >
        <div class="glass-card p-6">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">最近活动</h2>

          <div class="space-y-4">
            <div 
              v-for="(activity, index) in recentActivities" 
              :key="index"
              class="flex items-start p-4 bg-white/50 dark:bg-gray-800/50 rounded-xl hover:bg-white dark:hover:bg-gray-700 transition-all transform hover:scale-[1.01] cursor-pointer"
            >
              <div :class="getActivityIconClass(activity.type)" class="w-10 h-10 rounded-lg flex items-center justify-center mr-4 flex-shrink-0">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="getActivityIconPath(activity.type)"></path>
                </svg>
              </div>
              <div class="flex-1 min-w-0">
                <h4 class="font-medium text-gray-900 dark:text-white mb-1">{{ activity.title }}</h4>
                <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">{{ activity.description }}</p>
                <p class="text-xs text-gray-400 dark:text-gray-500">{{ activity.time }}</p>
              </div>
              <div class="ml-4 flex-shrink-0">
                <span :class="getActivityBadgeClass(activity.type)" class="badge text-xs">
                  {{ activity.status }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 浮动操作按钮 -->
    <button 
      v-motion
      :initial="{ scale: 0, rotate: -180 }"
      :enter="{ scale: 1, rotate: 0, transition: { delay: 800, type: 'spring' } }"
      class="fixed bottom-8 right-8 w-16 h-16 bg-gradient-to-br from-primary-600 to-secondary-600 rounded-full shadow-2xl flex items-center justify-center hover:scale-110 transition-transform group z-50"
      @click="showQuickMenu = !showQuickMenu"
    >
      <svg class="w-8 h-8 text-white group-hover:rotate-90 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 用户数据
const username = ref(localStorage.getItem('username') || '用户')
const userId = localStorage.getItem('user_id')
const userPoints = ref(0)
const checkinStreak = ref(0)
const todayCheckin = ref(null)
const showNotifications = ref(false)
const showQuickMenu = ref(false)

// 快速操作列表
const quickActions = ref([
  {
    label: '每日打卡',
    path: '/checkin/daily',
    iconClass: 'bg-gradient-to-br from-green-400 to-emerald-500',
    iconPath: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'
  },
  {
    label: '心理测评',
    path: '/psych/choose',
    iconClass: 'bg-gradient-to-br from-blue-400 to-indigo-500',
    iconPath: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2'
  },
  {
    label: 'AI对话',
    path: '/ai/roles',
    iconClass: 'bg-gradient-to-br from-purple-400 to-pink-500',
    iconPath: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z'
  },
  {
    label: '康复计划',
    path: '/plan/profile',
    iconClass: 'bg-gradient-to-br from-orange-400 to-red-500',
    iconPath: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z'
  },
  {
    label: '积分奖励',
    path: '/rewards/points',
    iconClass: 'bg-gradient-to-br from-yellow-400 to-orange-500',
    iconPath: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
  }
])

// 最近活动
const recentActivities = ref([
  {
    type: 'test',
    title: '完成PHQ-9测评',
    description: '抑郁症状评估 - 中度',
    time: '2小时前',
    status: '已完成'
  },
  {
    type: 'chat',
    title: '与温柔心理师对话',
    description: '讨论了工作压力的应对方法',
    time: '5小时前',
    status: '进行中'
  },
  {
    type: 'checkin',
    title: '每日打卡',
    description: '心情：平静 | 睡眠：7小时',
    time: '今天 08:30',
    status: '已完成'
  }
])

// 计算任务完成率
const taskCompletionRate = computed(() => {
  const total = 3
  const completed = todayCheckin.value ? 1 : 0
  return Math.round((completed / total) * 100)
})

// 获取问候语
const getGreeting = () => {
  const hour = new Date().getHours()
  if (hour < 6) return '夜深了，注意休息哦'
  if (hour < 9) return '早上好'
  if (hour < 12) return '上午好'
  if (hour < 14) return '中午好'
  if (hour < 18) return '下午好'
  if (hour < 22) return '晚上好'
  return '夜深了，早点休息'
}

// 获取当前日期
const getCurrentDate = () => {
  const date = new Date()
  const days = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日 ${days[date.getDay()]}`
}

// 导航
const navigateTo = (path) => {
  router.push(path)
}

// 退出登录
const logout = () => {
  localStorage.removeItem('user_id')
  localStorage.removeItem('username')
  localStorage.removeItem('isLoggedIn')
  router.push('/login')
}

// 获取活动图标类名
const getActivityIconClass = (type) => {
  const classes = {
    checkin: 'bg-green-100 text-green-600 dark:bg-green-900/50',
    test: 'bg-blue-100 text-blue-600 dark:bg-blue-900/50',
    chat: 'bg-purple-100 text-purple-600 dark:bg-purple-900/50'
  }
  return classes[type] || 'bg-gray-100 text-gray-600'
}

// 获取活动图标路径
const getActivityIconPath = (type) => {
  const paths = {
    checkin: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
    test: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',
    chat: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z'
  }
  return paths[type] || ''
}

// 获取活动徽章类名
const getActivityBadgeClass = (type) => {
  const classes = {
    checkin: 'badge-success',
    test: 'badge-primary',
    chat: 'bg-purple-100 text-purple-700'
  }
  return classes[type] || 'badge-primary'
}

// 加载用户数据
const loadUserData = async () => {
  if (!userId) return

  try {
    // 加载积分
    const pointsRes = await fetch(`/api/rewards/points?user_id=${userId}`)
    if (pointsRes.ok) {
      const pointsData = await pointsRes.json()
      userPoints.value = pointsData.points
    }

    // 加载打卡数据
    const checkinRes = await fetch(`/api/checkin/history?user_id=${userId}`)
    if (checkinRes.ok) {
      const checkinData = await checkinRes.json()
      if (checkinData.length > 0) {
        const today = new Date().toISOString().split('T')[0]
        todayCheckin.value = checkinData.find(record => record.date === today)
        checkinStreak.value = calculateCheckinStreak(checkinData)
      }
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

onMounted(() => {
  loadUserData()
})
</script>

<style scoped>
/* 自定义延迟动画 */
.delay-100 { animation-delay: 100ms; }
.delay-200 { animation-delay: 200ms; }
.delay-300 { animation-delay: 300ms; }
.delay-400 { animation-delay: 400ms; }
.delay-500 { animation-delay: 500ms; }
.delay-600 { animation-delay: 600ms; }
.delay-700 { animation-delay: 700ms; }
.delay-800 { animation-delay: 800ms; }
</style>

