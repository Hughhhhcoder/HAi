<template>
  <div style="min-height: calc(100vh - 4rem); background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); padding: 2rem 1rem;">
    <div style="max-width: 42rem; margin: 0 auto;">
      <!-- 标题 -->
      <div style="text-center; margin-bottom: 2rem;">
        <h1 style="font-size: 2rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">每日打卡</h1>
        <p style="color: #6b7280;">记录今天的心情和状态，获得积分奖励</p>
        <div style="font-size: 0.875rem; color: #9ca3af; margin-top: 0.5rem;">
          {{ new Date().toLocaleDateString('zh-CN', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric',
            weekday: 'long'
          }) }}
        </div>
      </div>

      <!-- 已打卡提示 -->
      <div v-if="hasCheckedIn" style="background: #d1fae5; border: 2px solid #6ee7b7; border-radius: 1rem; padding: 2rem; text-align: center; margin-bottom: 2rem;">
        <div style="width: 4rem; height: 4rem; background: #10b981; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem;">
          <svg style="width: 2rem; height: 2rem; color: white;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path>
          </svg>
        </div>
        <h2 style="font-size: 1.25rem; font-weight: 600; color: #065f46; margin-bottom: 0.5rem;">今日已打卡</h2>
        <p style="color: #047857;">继续保持，明天再来打卡吧！</p>
        <div style="display: flex; gap: 1rem; justify-content: center; margin-top: 1rem;">
          <button 
            @click="showCheckinHistory"
            style="padding: 0.75rem 1.5rem; background: #3b82f6; color: white; border-radius: 0.75rem; border: none; font-weight: 600; cursor: pointer; transition: background 0.2s;"
            @mouseenter="e => e.target.style.background = '#2563eb'"
            @mouseleave="e => e.target.style.background = '#3b82f6'"
          >
            📊 打卡记录
          </button>
          <router-link 
            to="/home" 
            style="display: inline-block; padding: 0.75rem 1.5rem; background: #10b981; color: white; border-radius: 0.75rem; text-decoration: none; font-weight: 600; transition: background 0.2s;"
            @mouseenter="e => e.target.style.background = '#059669'"
            @mouseleave="e => e.target.style.background = '#10b981'"
          >
            返回首页
          </router-link>
        </div>
      </div>

      <!-- 打卡表单 -->
      <div v-else style="background: white; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); padding: 2rem;">
        <form @submit.prevent="submitCheckin">
          <!-- 心情选择 -->
          <div style="margin-bottom: 2rem;">
            <label style="display: block; font-size: 1.125rem; font-weight: 600; color: #1f2937; margin-bottom: 1rem;">今天的心情如何？</label>
            <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem;">
              <div 
                v-for="mood in moods" 
                :key="mood.value"
                @click="selectedMood = mood.value"
                :style="getMoodStyle(mood.value)"
              >
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{{ mood.emoji }}</div>
                <div style="font-size: 0.875rem; font-weight: 500; color: #374151;">{{ mood.label }}</div>
              </div>
            </div>
          </div>

          <!-- 睡眠时长 -->
          <div style="margin-bottom: 2rem;">
            <label style="display: block; font-size: 1.125rem; font-weight: 600; color: #1f2937; margin-bottom: 1rem;">昨晚睡了几小时？</label>
            <input 
              v-model.number="sleepHours" 
              type="number" 
              min="0" 
              max="24" 
              step="0.5"
              style="width: 100%; padding: 0.75rem; border: 2px solid #e5e7eb; border-radius: 0.75rem; font-size: 1rem; transition: border-color 0.2s;"
              @focus="e => e.target.style.borderColor = '#10b981'"
              @blur="e => e.target.style.borderColor = '#e5e7eb'"
              placeholder="例如：8"
            />
          </div>

          <!-- 完成任务 -->
          <div style="margin-bottom: 2rem;">
            <label style="display: block; font-size: 1.125rem; font-weight: 600; color: #1f2937; margin-bottom: 1rem;">今天完成了哪些任务？</label>
            <textarea 
              v-model="completedTasks" 
              rows="4"
              style="width: 100%; padding: 0.75rem; border: 2px solid #e5e7eb; border-radius: 0.75rem; font-size: 1rem; resize: vertical; transition: border-color 0.2s;"
              @focus="e => e.target.style.borderColor = '#10b981'"
              @blur="e => e.target.style.borderColor = '#e5e7eb'"
              placeholder="例如：完成了工作任务、做了30分钟运动、阅读1小时..."
            ></textarea>
          </div>

          <!-- 提交按钮 -->
          <button 
            type="submit" 
            :disabled="!selectedMood || isSubmitting"
            style="width: 100%; padding: 1rem; background: #10b981; color: white; border-radius: 0.75rem; border: none; font-size: 1.125rem; font-weight: 600; cursor: pointer; transition: all 0.2s;"
            :style="{ opacity: (!selectedMood || isSubmitting) ? 0.5 : 1, cursor: (!selectedMood || isSubmitting) ? 'not-allowed' : 'pointer' }"
            @mouseenter="e => { if (selectedMood && !isSubmitting) e.target.style.background = '#059669' }"
            @mouseleave="e => { if (selectedMood && !isSubmitting) e.target.style.background = '#10b981' }"
          >
            {{ isSubmitting ? '提交中...' : '提交打卡' }}
          </button>
        </form>
      </div>
    </div>

    <!-- 打卡记录弹窗 -->
    <div v-if="showHistoryModal" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 0, 0, 0.5); display: flex; align-items: center; justify-content: center; z-index: 1000;" @click="closeHistoryModal">
      <div style="background: white; border-radius: 1rem; width: 90%; max-width: 600px; max-height: 80vh; overflow: hidden; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);" @click.stop>
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 1.5rem; border-bottom: 1px solid #e5e7eb; background: linear-gradient(135deg, #3b82f6, #2563eb); color: white;">
          <h3 style="font-size: 1.25rem; font-weight: 600; margin: 0;">📊 每日打卡记录</h3>
          <button @click="closeHistoryModal" style="background: rgba(255, 255, 255, 0.2); border: none; border-radius: 0.5rem; padding: 0.5rem; cursor: pointer; transition: background 0.2s;" @mouseenter="e => e.target.style.background = 'rgba(255, 255, 255, 0.3)'">
            <svg style="width: 1.25rem; height: 1.25rem; color: white;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <div style="display: flex; gap: 2rem; padding: 1.5rem; background: #f8fafc; border-bottom: 1px solid #e5e7eb;">
          <div style="display: flex; flex-direction: column; gap: 0.25rem;">
            <span style="font-size: 0.875rem; color: #6b7280;">总打卡数</span>
            <span style="font-size: 1.125rem; font-weight: 600; color: #1f2937;">{{ checkinHistoryStats.totalCheckins }}</span>
          </div>
          <div style="display: flex; flex-direction: column; gap: 0.25rem;">
            <span style="font-size: 0.875rem; color: #6b7280;">最近打卡</span>
            <span style="font-size: 1.125rem; font-weight: 600; color: #1f2937;">{{ checkinHistoryStats.lastCheckinTime }}</span>
          </div>
        </div>

        <div style="max-height: 400px; overflow-y: auto; padding: 1rem;">
          <div v-for="(record, index) in checkinHistoryRecords" :key="index" style="padding: 1rem; border-bottom: 1px solid #f3f4f6; transition: background 0.2s;" @mouseenter="e => e.target.style.background = '#f8fafc'" @mouseleave="e => e.target.style.background = 'white'">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
              <span style="font-size: 0.75rem; color: #9ca3af;">{{ formatTimestamp(record.created_at) }}</span>
              <span style="font-size: 0.75rem; padding: 0.25rem 0.5rem; border-radius: 0.375rem; background: #e5e7eb; color: #374151;">{{ record.date }}</span>
            </div>
            <div style="margin-top: 0.5rem;">
              <p style="font-size: 0.875rem; color: #374151; line-height: 1.5; margin: 0;">心情：{{ record.mood || '未记录' }} | 睡眠：{{ record.sleep_hours || '未记录' }}小时</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { checkinApi } from '../api/index.js'

const userId = localStorage.getItem('user_id')
const hasCheckedIn = ref(false)
const selectedMood = ref('')
const sleepHours = ref(8)
const completedTasks = ref('')
const isSubmitting = ref(false)
const showHistoryModal = ref(false)
const checkinHistoryRecords = ref([])
const checkinHistoryStats = ref({
  totalCheckins: 0,
  lastCheckinTime: '暂无'
})

const moods = [
  { value: '很好', emoji: '😄', label: '很好' },
  { value: '不错', emoji: '😊', label: '不错' },
  { value: '一般', emoji: '😐', label: '一般' },
  { value: '不太好', emoji: '😔', label: '不太好' },
  { value: '很糟', emoji: '😢', label: '很糟' },
]

const getMoodStyle = (value) => {
  const isSelected = selectedMood.value === value
  return {
    textAlign: 'center',
    cursor: 'pointer',
    padding: '1rem',
    borderRadius: '0.75rem',
    border: isSelected ? '2px solid #10b981' : '2px solid #e5e7eb',
    background: isSelected ? '#d1fae5' : 'transparent',
    transition: 'all 0.2s',
  }
}

async function submitCheckin() {
  if (!userId || !selectedMood.value || isSubmitting.value) return
  
  isSubmitting.value = true
  try {
    await checkinApi.dailyCheckin(userId, selectedMood.value, sleepHours.value, completedTasks.value)
    hasCheckedIn.value = true
    alert('打卡成功！获得积分奖励')
  } catch (e) {
    alert('打卡失败：' + (e.message || '请稍后重试'))
  } finally {
    isSubmitting.value = false
  }
}

const showCheckinHistory = async () => {
  if (!userId) return
  
  try {
    const history = await checkinApi.getHistory(userId)
    checkinHistoryRecords.value = history || []
    checkinHistoryStats.value = {
      totalCheckins: history.length,
      lastCheckinTime: history.length > 0 ? formatTimestamp(history[0].created_at) : '暂无'
    }
    showHistoryModal.value = true
  } catch (error) {
    console.error('Error loading checkin history:', error)
    alert('加载打卡记录失败')
  }
}

const closeHistoryModal = () => {
  showHistoryModal.value = false
}

const formatTimestamp = (timestamp) => {
  if (!timestamp) return '未知时间'
  try {
    const date = new Date(timestamp)
    const now = new Date()
    const diff = now - date
    
    // 如果是今天
    if (diff < 24 * 60 * 60 * 1000 && date.getDate() === now.getDate()) {
      return date.toLocaleTimeString('zh-CN', { 
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit'
      })
    }
    
    // 如果是昨天
    const yesterday = new Date(now)
    yesterday.setDate(yesterday.getDate() - 1)
    if (date.getDate() === yesterday.getDate() && date.getMonth() === yesterday.getMonth()) {
      return `昨天 ${date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })}`
    }
    
    // 其他情况显示完整日期时间
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  } catch (error) {
    console.error('时间格式化错误:', error)
    return '时间格式错误'
  }
}

onMounted(async () => {
  if (!userId) return
  // 检查今日是否已打卡
  try {
    const history = await checkinApi.getHistory(userId)
    const today = new Date().toISOString().split('T')[0]
    hasCheckedIn.value = history.some(item => item.date?.startsWith(today))
  } catch (e) {
    console.error('检查打卡状态失败:', e)
  }
})
</script>

