<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 p-6">
    <div class="max-w-2xl mx-auto">
      <!-- 页面标题 -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">每日打卡</h1>
        <p class="text-gray-600">记录今天的心情和状态，获得积分奖励</p>
        <div class="text-sm text-gray-500 mt-2">
          {{ new Date().toLocaleDateString('zh-CN', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric',
            weekday: 'long'
          }) }}
        </div>
      </div>

      <!-- 打卡状态提示 -->
      <div v-if="hasCheckedIn" class="bg-green-100 border border-green-200 rounded-xl p-6 mb-8 text-center">
        <div class="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
        </div>
        <h2 class="text-xl font-semibold text-green-800 mb-2">今日已打卡</h2>
        <p class="text-green-700">继续保持，明天再来打卡吧！</p>
        <router-link to="/home" class="inline-block mt-4 px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
          返回首页
        </router-link>
      </div>

      <!-- 打卡表单 -->
      <div v-else class="bg-white rounded-2xl shadow-lg p-8">
        <form @submit.prevent="submitCheckin">
          <!-- 心情选择 -->
          <div class="mb-8">
            <label class="block text-lg font-semibold text-gray-800 mb-4">今天的心情如何？</label>
            <div class="grid grid-cols-5 gap-4">
              <div 
                v-for="mood in moods" 
                :key="mood.value"
                class="text-center cursor-pointer p-4 rounded-xl border-2 transition-all"
                :class="selectedMood === mood.value ? 'border-green-500 bg-green-50' : 'border-gray-200 hover:border-green-300'"
                @click="selectedMood = mood.value"
              >
                <div class="text-3xl mb-2">{{ mood.emoji }}</div>
                <div class="text-sm font-medium text-gray-700">{{ mood.label }}</div>
              </div>
            </div>
          </div>

          <!-- 睡眠时间 -->
          <div class="mb-8">
            <label for="sleepHours" class="block text-lg font-semibold text-gray-800 mb-4">
              昨晚睡了几个小时？
            </label>
            <div class="flex items-center space-x-4">
              <input 
                id="sleepHours"
                v-model.number="sleepHours" 
                type="number" 
                min="0" 
                max="24" 
                step="0.5"
                class="w-24 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 text-center text-lg"
                placeholder="8"
              />
              <span class="text-gray-600">小时</span>
              <div class="flex-1">
                <input 
                  type="range" 
                  min="0" 
                  max="12" 
                  step="0.5" 
                  v-model.number="sleepHours"
                  class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                />
              </div>
            </div>
            <div class="mt-2 text-sm text-gray-500">
              建议成年人每晚睡眠7-9小时
            </div>
          </div>

          <!-- 完成的任务 -->
          <div class="mb-8">
            <label for="completedTasks" class="block text-lg font-semibold text-gray-800 mb-4">
              今天完成了哪些任务？
            </label>
            <textarea 
              id="completedTasks"
              v-model="completedTasks" 
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 resize-none"
              rows="4"
              placeholder="例如：完成工作报告、运动30分钟、阅读一章书..."
            ></textarea>
            <div class="mt-2 text-sm text-gray-500">
              记录今天的成就，让每一天都有意义
            </div>
          </div>

          <!-- 错误提示 -->
          <div v-if="errorMessage" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-sm text-red-600">{{ errorMessage }}</p>
          </div>

          <!-- 成功提示 -->
          <div v-if="successMessage" class="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
            <p class="text-sm text-green-600">{{ successMessage }}</p>
          </div>

          <!-- 提交按钮 -->
          <div class="flex space-x-4">
            <button 
              type="submit"
              class="flex-1 bg-green-600 text-white py-4 px-6 rounded-xl font-semibold text-lg hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="isLoading || !selectedMood"
            >
              <span v-if="isLoading">提交中...</span>
              <span v-else>完成打卡 (+5积分)</span>
            </button>
            
            <router-link 
              to="/home" 
              class="px-6 py-4 border border-gray-300 text-gray-700 rounded-xl font-semibold hover:bg-gray-50 transition-colors text-center"
            >
              取消
            </router-link>
          </div>
        </form>
      </div>

      <!-- 历史打卡记录 -->
      <div v-if="checkinHistory.length > 0" class="mt-8 bg-white rounded-2xl shadow-lg p-6">
        <h2 class="text-xl font-semibold text-gray-800 mb-4">最近的打卡记录</h2>
        <div class="space-y-3">
          <div 
            v-for="record in checkinHistory.slice(0, 5)" 
            :key="record.date"
            class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
          >
            <div class="flex items-center space-x-4">
              <div class="text-2xl">
                {{ getMoodEmoji(record.mood) }}
              </div>
              <div>
                <div class="font-medium text-gray-800">
                  {{ formatDate(record.date) }}
                </div>
                <div class="text-sm text-gray-600">
                  睡眠: {{ record.sleep_hours || '未记录' }}小时
                </div>
              </div>
            </div>
            <div class="text-right">
              <div class="text-sm text-green-600 font-medium">+5积分</div>
            </div>
          </div>
        </div>
        
        <div class="mt-4 text-center">
          <button 
            @click="loadMoreHistory"
            class="text-green-600 hover:text-green-700 text-sm font-medium"
          >
            查看更多记录
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { checkinApi } from '../api/index.js'

const router = useRouter()
const userId = localStorage.getItem('user_id')

// 表单数据
const selectedMood = ref('')
const sleepHours = ref(8)
const completedTasks = ref('')
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const hasCheckedIn = ref(false)
const checkinHistory = ref([])

// 心情选项
const moods = [
  { value: '很好', label: '很好', emoji: '😊' },
  { value: '不错', label: '不错', emoji: '🙂' },
  { value: '一般', label: '一般', emoji: '😐' },
  { value: '不太好', label: '不太好', emoji: '😔' },
  { value: '很糟', label: '很糟', emoji: '😞' }
]

// 检查今日是否已打卡
const checkTodayCheckin = async () => {
  if (!userId) return

  try {
    const data = await checkinApi.getHistory(userId)
    const today = new Date().toISOString().split('T')[0]
    hasCheckedIn.value = data.some(record => record.date === today)
    checkinHistory.value = data
  } catch (error) {
    console.error('检查打卡状态失败:', error)
  }
}

// 提交打卡
const submitCheckin = async () => {
  if (!selectedMood.value) {
    errorMessage.value = '请选择今天的心情'
    return
  }

  isLoading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const data = await checkinApi.dailyCheckin(
      userId,
      selectedMood.value,
      sleepHours.value,
      completedTasks.value
    )

    successMessage.value = `${data.msg}！当前积分：${data.points}`
    hasCheckedIn.value = true
    
    // 延迟跳转到首页
    setTimeout(() => {
      router.push('/home')
    }, 2000)
  } catch (error) {
    console.error('打卡失败:', error)
    errorMessage.value = error.message || '打卡失败，请重试'
  } finally {
    isLoading.value = false
  }
}

// 获取心情表情
const getMoodEmoji = (mood) => {
  const moodMap = {
    '很好': '😊',
    '不错': '🙂',
    '一般': '😐',
    '不太好': '😔',
    '很糟': '😞'
  }
  return moodMap[mood] || '😐'
}

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', { 
    month: 'short', 
    day: 'numeric',
    weekday: 'short'
  })
}

// 加载更多历史记录
const loadMoreHistory = () => {
  // 这里可以实现分页加载更多记录
  console.log('加载更多历史记录')
}

onMounted(() => {
  checkTodayCheckin()
})
</script>

<style scoped>
.slider::-webkit-slider-thumb {
  appearance: none;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #10b981;
  cursor: pointer;
}

.slider::-moz-range-thumb {
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #10b981;
  cursor: pointer;
  border: none;
}
</style> 