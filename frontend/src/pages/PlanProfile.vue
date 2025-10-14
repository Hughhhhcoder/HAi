<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 to-amber-100 p-6">
    <div class="max-w-3xl mx-auto">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">生活作息填写</h1>
        <p class="text-gray-600">填写并保存作息信息，可基于最近测评生成恢复计划</p>
      </div>

      <!-- 信息提示 -->
      <div v-if="errorMessage" class="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">{{ errorMessage }}</div>
      <div v-if="successMessage" class="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg text-green-700">{{ successMessage }}</div>

      <!-- 表单卡片 -->
      <div class="bg-white rounded-2xl shadow-lg p-6 mb-8">
        <form @submit.prevent="onSave">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">建议入睡时间</label>
              <input v-model="sleepTime" type="time" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">建议起床时间</label>
              <input v-model="wakeTime" type="time" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500" />
            </div>
          </div>

          <div class="mt-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">个人偏好（可选）</label>
            <textarea v-model="preferences" rows="3" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500" placeholder="例如：喜欢晨跑、晚间阅读、清淡饮食"></textarea>
          </div>

          <div class="mt-6 flex flex-col md:flex-row gap-3">
            <button type="submit" :disabled="isSaving" class="px-6 py-3 bg-orange-600 text-white rounded-xl hover:bg-orange-700 transition-colors disabled:opacity-60">
              {{ isSaving ? '保存中...' : '保存作息' }}
            </button>
            <button type="button" @click="onGenerate" :disabled="isGenerating" class="px-6 py-3 bg-amber-600 text-white rounded-xl hover:bg-amber-700 transition-colors disabled:opacity-60">
              {{ isGenerating ? '生成中...' : '生成恢复计划' }}
            </button>
          </div>
        </form>
      </div>

      <!-- 生成结果 -->
      <div v-if="generatedPlan" class="bg-white rounded-2xl shadow-lg p-6 mb-8">
        <div class="flex items-center justify-between mb-3">
          <h2 class="text-xl font-semibold text-gray-800">最新计划</h2>
          <span class="text-sm text-gray-500">阶段：{{ generatedPlan.stage }}</span>
        </div>
        <pre class="whitespace-pre-wrap text-gray-800">{{ generatedPlan.plan_text }}</pre>
      </div>

      <!-- 历史计划 -->
      <div class="bg-white rounded-2xl shadow-lg p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold text-gray-800">历史计划</h2>
          <button @click="loadHistory" class="text-sm text-orange-600 hover:text-orange-700">刷新</button>
        </div>
        <div v-if="planHistory.length === 0" class="text-gray-500 text-sm">暂无历史计划</div>
        <div v-else class="space-y-4">
          <div v-for="p in planHistory" :key="p.id" class="p-4 rounded-lg border border-gray-100 bg-gray-50">
            <div class="text-sm text-gray-500 mb-1">阶段：{{ p.stage }} · {{ formatDate(p.created_at) }}</div>
            <div class="text-gray-800 whitespace-pre-wrap">{{ p.plan_text }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { planApi } from '../api/index.js'

const userId = localStorage.getItem('user_id')

// 表单状态
const sleepTime = ref('')
const wakeTime = ref('')
const preferences = ref('')
const isSaving = ref(false)
const isGenerating = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

// 结果与历史
const generatedPlan = ref(null)
const planHistory = ref([])

// 加载当前作息
async function loadProfile() {
  if (!userId) return
  try {
    const data = await planApi.getProfile(userId)
    sleepTime.value = data.sleep_time || ''
    wakeTime.value = data.wake_time || ''
    preferences.value = data.preferences || ''
  } catch (e) {
    // 未设置时 404，忽略
  }
}

// 保存
async function onSave() {
  if (!userId) return
  isSaving.value = true
  successMessage.value = ''
  errorMessage.value = ''
  try {
    const resp = await planApi.updateProfile(userId, sleepTime.value, wakeTime.value, preferences.value)
    successMessage.value = resp.msg || '已保存'
  } catch (e) {
    errorMessage.value = e.message || '保存失败'
  } finally {
    isSaving.value = false
  }
}

// 生成计划
async function onGenerate() {
  if (!userId) return
  isGenerating.value = true
  successMessage.value = ''
  errorMessage.value = ''
  try {
    const resp = await planApi.generatePlan(userId)
    generatedPlan.value = resp
    await loadHistory()
  } catch (e) {
    errorMessage.value = e.message || '生成失败'
  } finally {
    isGenerating.value = false
  }
}

// 历史
async function loadHistory() {
  if (!userId) return
  try {
    planHistory.value = await planApi.getHistory(userId)
  } catch (e) {
    // 忽略
  }
}

function formatDate(ts) {
  try {
    return new Date(ts).toLocaleString('zh-CN')
  } catch {
    return String(ts)
  }
}

onMounted(async () => {
  await loadProfile()
  await loadHistory()
})
</script>