<template>
  <div style="min-height: calc(100vh - 4rem); background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%); padding: 2rem 1rem;">
    <div style="max-width: 48rem; margin: 0 auto;">
      <!-- 标题 -->
      <div style="text-center; margin-bottom: 2rem;">
        <h1 style="font-size: 2rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">生活作息填写</h1>
        <p style="color: #6b7280;">填写并保存作息信息，可基于最近测评生成恢复计划</p>
      </div>

      <!-- 消息提示 -->
      <div v-if="errorMessage" style="margin-bottom: 1rem; padding: 1rem; background: #fee2e2; border: 1px solid #fecaca; border-radius: 0.75rem; color: #991b1b;">
        {{ errorMessage }}
      </div>
      <div v-if="successMessage" style="margin-bottom: 1rem; padding: 1rem; background: #d1fae5; border: 1px solid #6ee7b7; border-radius: 0.75rem; color: #065f46;">
        {{ successMessage }}
      </div>

      <!-- 表单卡片 -->
      <div style="background: white; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); padding: 2rem; margin-bottom: 2rem;">
        <form @submit.prevent="onSave">
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
            <div>
              <label style="display: block; font-size: 0.875rem; font-weight: 600; color: #374151; margin-bottom: 0.5rem;">建议入睡时间</label>
              <input 
                v-model="sleepTime" 
                type="time" 
                style="width: 100%; padding: 0.75rem 1rem; border: 2px solid #e5e7eb; border-radius: 0.75rem; font-size: 1rem; transition: border-color 0.2s;"
                @focus="e => e.target.style.borderColor = '#f97316'"
                @blur="e => e.target.style.borderColor = '#e5e7eb'"
              />
            </div>
            <div>
              <label style="display: block; font-size: 0.875rem; font-weight: 600; color: #374151; margin-bottom: 0.5rem;">建议起床时间</label>
              <input 
                v-model="wakeTime" 
                type="time" 
                style="width: 100%; padding: 0.75rem 1rem; border: 2px solid #e5e7eb; border-radius: 0.75rem; font-size: 1rem; transition: border-color 0.2s;"
                @focus="e => e.target.style.borderColor = '#f97316'"
                @blur="e => e.target.style.borderColor = '#e5e7eb'"
              />
            </div>
          </div>

          <div style="margin-top: 1.5rem;">
            <label style="display: block; font-size: 0.875rem; font-weight: 600; color: #374151; margin-bottom: 0.5rem;">个人偏好（可选）</label>
            <textarea 
              v-model="preferences" 
              rows="3" 
              style="width: 100%; padding: 0.75rem 1rem; border: 2px solid #e5e7eb; border-radius: 0.75rem; font-size: 1rem; resize: vertical; transition: border-color 0.2s;"
              @focus="e => e.target.style.borderColor = '#f97316'"
              @blur="e => e.target.style.borderColor = '#e5e7eb'"
              placeholder="例如：喜欢晨跑、晚间阅读、清淡饮食"
            ></textarea>
          </div>

          <div style="margin-top: 1.5rem; display: flex; flex-wrap: wrap; gap: 0.75rem;">
            <button 
              type="submit" 
              :disabled="isSaving" 
              style="padding: 0.75rem 1.5rem; background: #f97316; color: white; border-radius: 0.75rem; border: none; font-weight: 600; cursor: pointer; transition: all 0.2s;"
              :style="{ opacity: isSaving ? 0.6 : 1 }"
              @mouseenter="e => { if (!isSaving) e.target.style.background = '#ea580c' }"
              @mouseleave="e => { if (!isSaving) e.target.style.background = '#f97316' }"
            >
              {{ isSaving ? '保存中...' : '保存作息' }}
            </button>
            <button 
              type="button" 
              @click="onGenerate" 
              :disabled="isGenerating"
              style="padding: 0.75rem 1.5rem; background: #f59e0b; color: white; border-radius: 0.75rem; border: none; font-weight: 600; cursor: pointer; transition: all 0.2s;"
              :style="{ opacity: isGenerating ? 0.6 : 1 }"
              @mouseenter="e => { if (!isGenerating) e.target.style.background = '#d97706' }"
              @mouseleave="e => { if (!isGenerating) e.target.style.background = '#f59e0b' }"
            >
              {{ isGenerating ? '生成中...' : '生成恢复计划' }}
            </button>
          </div>
        </form>
      </div>

      <!-- 生成结果 -->
      <div v-if="generatedPlan" style="background: white; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); padding: 2rem; margin-bottom: 2rem;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
          <h2 style="font-size: 1.25rem; font-weight: 600; color: #1f2937;">智能生成计划</h2>
          <div style="display: flex; gap: 1rem; align-items: center;">
            <span style="font-size: 0.875rem; color: #9ca3af;">{{ formatDate(new Date()) }}</span>
            <span v-if="generatedPlan.priority_level" style="font-size: 0.75rem; padding: 0.25rem 0.5rem; border-radius: 0.5rem; background: #fef3c7; color: #92400e;">
              优先级：{{ generatedPlan.priority_level }}
            </span>
          </div>
        </div>
        
        <!-- 重点关注领域 -->
        <div v-if="generatedPlan.focus_areas && generatedPlan.focus_areas.length > 0" style="margin-bottom: 1rem; padding: 1rem; background: #f0f9ff; border-radius: 0.75rem; border: 1px solid #bae6fd;">
          <h3 style="font-size: 0.875rem; font-weight: 600; color: #0369a1; margin-bottom: 0.5rem;">🎯 重点关注领域</h3>
          <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
            <span 
              v-for="area in generatedPlan.focus_areas" 
              :key="area"
              style="font-size: 0.75rem; padding: 0.25rem 0.5rem; background: #dbeafe; color: #1e40af; border-radius: 0.375rem;"
            >
              {{ area }}
            </span>
          </div>
        </div>
        
        <!-- 计划内容 -->
        <div style="background: #fafafa; border-radius: 0.75rem; padding: 1.5rem; border: 1px solid #e5e7eb;">
          <pre style="white-space: pre-wrap; color: #1f2937; font-family: inherit; line-height: 1.6; margin: 0;">{{ generatedPlan.plan_text }}</pre>
        </div>
      </div>

      <!-- 历史计划 -->
      <div v-if="historyList.length > 0" style="background: white; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); padding: 2rem;">
        <h2 style="font-size: 1.25rem; font-weight: 600; color: #1f2937; margin-bottom: 1.5rem;">历史计划</h2>
        <div style="display: flex; flex-direction: column; gap: 1rem;">
          <div 
            v-for="(plan, idx) in historyList" 
            :key="idx"
            style="padding: 1rem; background: #fff7ed; border-radius: 0.75rem; border: 1px solid #fed7aa;"
          >
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
              <span style="font-weight: 600; color: #ea580c;">计划 #{{ idx + 1 }}</span>
              <span style="font-size: 0.875rem; color: #9ca3af;">{{ plan.stage || '未知阶段' }}</span>
            </div>
            <pre style="white-space: pre-wrap; color: #374151; font-family: inherit; font-size: 0.875rem; line-height: 1.5;">{{ plan.plan_text }}</pre>
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
const sleepTime = ref('')
const wakeTime = ref('')
const preferences = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const isSaving = ref(false)
const isGenerating = ref(false)
const generatedPlan = ref(null)
const historyList = ref([])

async function onSave() {
  if (!userId || isSaving.value) return
  
  errorMessage.value = ''
  successMessage.value = ''
  isSaving.value = true
  
  try {
    await planApi.updateProfile(userId, sleepTime.value, wakeTime.value, preferences.value)
    successMessage.value = '作息信息保存成功！'
  } catch (e) {
    errorMessage.value = '保存失败：' + (e.message || '请稍后重试')
  } finally {
    isSaving.value = false
  }
}

async function onGenerate() {
  if (!userId || isGenerating.value) return
  
  errorMessage.value = ''
  successMessage.value = ''
  isGenerating.value = true
  
  try {
    const result = await planApi.generatePlan(userId)
    generatedPlan.value = result
    successMessage.value = '恢复计划生成成功！'
    loadHistory()
  } catch (e) {
    errorMessage.value = '生成失败：' + (e.message || '请稍后重试')
  } finally {
    isGenerating.value = false
  }
}

async function loadHistory() {
  if (!userId) return
  try {
    historyList.value = await planApi.getHistory(userId)
  } catch (e) {
    console.error('加载历史失败:', e)
  }
}

function formatDate(date) {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

onMounted(async () => {
  if (!userId) return
  
  // 加载现有配置
  try {
    const profile = await planApi.getProfile(userId)
    if (profile) {
      sleepTime.value = profile.sleep_time || ''
      wakeTime.value = profile.wake_time || ''
      preferences.value = profile.preferences || ''
    }
  } catch (e) {
    console.error('加载配置失败:', e)
  }
  
  // 加载历史计划
  loadHistory()
})
</script>

