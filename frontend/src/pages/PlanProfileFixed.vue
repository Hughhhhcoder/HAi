<template>
  <div class="plan-page">
    <!-- 动态背景 -->
    <div class="animated-background">
      <div class="floating-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
        <div class="shape shape-4"></div>
      </div>
    </div>

    <div class="container">
      <!-- 标题区域 -->
      <div class="title-section">
        <div class="title-icon">🌅</div>
        <h1 class="main-title">生活作息填写</h1>
        <p class="subtitle">填写并保存作息信息，可基于最近测评生成恢复计划</p>
        <div class="title-decoration"></div>
      </div>

      <!-- 消息提示 -->
      <transition name="slide-down">
        <div v-if="errorMessage" class="message error-message">
          <div class="message-icon">⚠️</div>
          <span>{{ errorMessage }}</span>
        </div>
      </transition>
      <transition name="slide-down">
        <div v-if="successMessage" class="message success-message">
          <div class="message-icon">✅</div>
          <span>{{ successMessage }}</span>
        </div>
      </transition>

      <!-- 表单卡片 -->
      <div class="form-card">
        <form @submit.prevent="onSave" class="form">
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">🌙</span>
                建议入睡时间
              </label>
              <div class="input-wrapper">
                <input 
                  v-model="sleepTime" 
                  type="time" 
                  class="form-input"
                  placeholder="选择入睡时间"
                />
                <div class="input-glow"></div>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">☀️</span>
                建议起床时间
              </label>
              <div class="input-wrapper">
                <input 
                  v-model="wakeTime" 
                  type="time" 
                  class="form-input"
                  placeholder="选择起床时间"
                />
                <div class="input-glow"></div>
              </div>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">
              <span class="label-icon">💝</span>
              个人偏好（可选）
            </label>
            <div class="textarea-wrapper">
              <textarea 
                v-model="preferences" 
                rows="3" 
                class="form-textarea"
                placeholder="例如：喜欢晨跑、晚间阅读、清淡饮食"
              ></textarea>
              <div class="textarea-glow"></div>
            </div>
          </div>

          <div class="button-group">
            <button 
              type="submit" 
              :disabled="isSaving" 
              class="btn btn-primary"
              :class="{ 'btn-loading': isSaving }"
            >
              <span v-if="!isSaving" class="btn-content">
                <span class="btn-icon">💾</span>
                保存作息
              </span>
              <span v-else class="btn-content">
                <div class="spinner"></div>
                保存中...
              </span>
            </button>
            <button 
              type="button" 
              @click="onGenerate" 
              :disabled="isGenerating"
              class="btn btn-secondary"
              :class="{ 'btn-loading': isGenerating }"
            >
              <span v-if="!isGenerating" class="btn-content">
                <span class="btn-icon">✨</span>
                生成恢复计划
              </span>
              <span v-else class="btn-content">
                <div class="spinner"></div>
                生成中...
              </span>
            </button>
          </div>
        </form>
      </div>

      <!-- 生成结果 -->
      <transition name="fade-up">
        <div v-if="generatedPlan" class="plan-card">
          <div class="plan-header">
            <div class="plan-title">
              <div class="title-icon">✨</div>
              <h2>智能生成计划</h2>
            </div>
            <div class="plan-meta">
              <span class="plan-date">{{ formatDate(new Date()) }}</span>
              <span v-if="generatedPlan.priority_level" class="priority-badge" :class="`priority-${generatedPlan.priority_level}`">
                {{ generatedPlan.priority_level }}
              </span>
            </div>
          </div>
          
          <!-- 重点关注领域 -->
          <div v-if="generatedPlan.focus_areas && generatedPlan.focus_areas.length > 0" class="focus-areas">
            <h3 class="focus-title">
              <span class="focus-icon">🎯</span>
              重点关注领域
            </h3>
            <div class="focus-tags">
              <span 
                v-for="(area, index) in generatedPlan.focus_areas" 
                :key="area"
                class="focus-tag"
                :style="{ animationDelay: `${index * 0.1}s` }"
              >
                {{ area }}
              </span>
            </div>
          </div>
          
          <!-- 计划内容 -->
          <div class="plan-content">
            <div class="content-wrapper">
              <pre class="plan-text">{{ generatedPlan.plan_text }}</pre>
            </div>
          </div>
        </div>
      </transition>

      <!-- 历史计划 -->
      <div v-if="historyList.length > 0" class="history-card">
        <div class="history-header">
          <div class="history-title">
            <div class="title-icon">📚</div>
            <h2>历史计划</h2>
          </div>
          <div class="history-count">{{ historyList.length }} 个计划</div>
        </div>
        <div class="history-list">
          <transition-group name="list" tag="div" class="history-items">
            <div 
              v-for="(plan, idx) in historyList" 
              :key="plan.id || idx"
              class="history-item"
              :style="{ animationDelay: `${idx * 0.1}s` }"
            >
              <div class="item-header">
                <span class="item-number">计划 #{{ idx + 1 }}</span>
                <span class="item-stage">{{ plan.stage || '未知阶段' }}</span>
              </div>
              <div class="item-content">
                <pre class="item-text">{{ plan.plan_text }}</pre>
              </div>
            </div>
          </transition-group>
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

<style scoped>
/* 页面整体样式 */
.plan-page {
  min-height: calc(100vh - 4rem);
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem 1rem;
}

/* 动态背景 */
.animated-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  z-index: 0;
}

.floating-shapes {
  position: relative;
  width: 100%;
  height: 100%;
}

.shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 6s ease-in-out infinite;
}

.shape-1 {
  width: 80px;
  height: 80px;
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.shape-2 {
  width: 120px;
  height: 120px;
  top: 60%;
  right: 15%;
  animation-delay: 2s;
}

.shape-3 {
  width: 60px;
  height: 60px;
  top: 80%;
  left: 20%;
  animation-delay: 4s;
}

.shape-4 {
  width: 100px;
  height: 100px;
  top: 30%;
  right: 30%;
  animation-delay: 1s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(180deg); }
}

/* 容器 */
.container {
  max-width: 48rem;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

/* 标题区域 */
.title-section {
  text-align: center;
  margin-bottom: 3rem;
  position: relative;
}

.title-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  animation: pulse 2s ease-in-out infinite;
}

.main-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: white;
  margin-bottom: 0.5rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  animation: slideInDown 0.8s ease-out;
}

.subtitle {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
  animation: slideInDown 0.8s ease-out 0.2s both;
}

.title-decoration {
  width: 60px;
  height: 4px;
  background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
  margin: 0 auto;
  border-radius: 2px;
  animation: slideInDown 0.8s ease-out 0.4s both;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

@keyframes slideInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 消息提示 */
.message {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  border-radius: 1rem;
  margin-bottom: 1.5rem;
  font-weight: 500;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.error-message {
  background: linear-gradient(135deg, #fee2e2, #fecaca);
  border: 1px solid #fca5a5;
  color: #991b1b;
}

.success-message {
  background: linear-gradient(135deg, #d1fae5, #a7f3d0);
  border: 1px solid #6ee7b7;
  color: #065f46;
}

.message-icon {
  font-size: 1.25rem;
}

/* 过渡动画 */
.slide-down-enter-active, .slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}

.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* 表单卡片 */
.form-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 1.5rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  padding: 2.5rem;
  margin-bottom: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  animation: slideInUp 0.8s ease-out 0.3s both;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 表单样式 */
.form {
  width: 100%;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.form-group {
  position: relative;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.75rem;
}

.label-icon {
  font-size: 1.1rem;
}

.input-wrapper, .textarea-wrapper {
  position: relative;
}

.form-input, .form-textarea {
  width: 100%;
  padding: 1rem 1.25rem;
  border: 2px solid #e5e7eb;
  border-radius: 1rem;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.form-input:focus, .form-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  transform: translateY(-2px);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.input-glow, .textarea-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 1rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.form-input:focus + .input-glow,
.form-textarea:focus + .textarea-glow {
  opacity: 0.1;
}

/* 按钮组 */
.button-group {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-top: 2rem;
}

.btn {
  position: relative;
  padding: 1rem 2rem;
  border: none;
  border-radius: 1rem;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
  min-width: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  box-shadow: 0 4px 15px 0 rgba(102, 126, 234, 0.4);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px 0 rgba(102, 126, 234, 0.6);
}

.btn-secondary {
  background: linear-gradient(135deg, #f093fb, #f5576c);
  color: white;
  box-shadow: 0 4px 15px 0 rgba(240, 147, 251, 0.4);
}

.btn-secondary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px 0 rgba(240, 147, 251, 0.6);
}

.btn-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-icon {
  font-size: 1.1rem;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 计划卡片 */
.plan-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 1.5rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  padding: 2.5rem;
  margin-bottom: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  animation: slideInUp 0.8s ease-out;
}

.plan-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.plan-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.plan-title h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.plan-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.plan-date {
  font-size: 0.9rem;
  color: #6b7280;
  background: rgba(107, 114, 128, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 0.75rem;
}

.priority-badge {
  font-size: 0.8rem;
  padding: 0.4rem 0.8rem;
  border-radius: 0.5rem;
  font-weight: 600;
}

.priority-高 {
  background: #fee2e2;
  color: #dc2626;
}

.priority-中 {
  background: #fef3c7;
  color: #d97706;
}

.priority-低 {
  background: #d1fae5;
  color: #059669;
}

/* 重点关注领域 */
.focus-areas {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
  border-radius: 1rem;
  border: 1px solid #bae6fd;
}

.focus-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: #0369a1;
  margin-bottom: 1rem;
}

.focus-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.focus-tag {
  font-size: 0.85rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #dbeafe, #bfdbfe);
  color: #1e40af;
  border-radius: 2rem;
  font-weight: 500;
  animation: tagAppear 0.6s ease-out both;
  box-shadow: 0 2px 4px rgba(30, 64, 175, 0.1);
}

@keyframes tagAppear {
  from {
    opacity: 0;
    transform: scale(0.8) translateY(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* 计划内容 */
.plan-content {
  background: #fafafa;
  border-radius: 1rem;
  padding: 2rem;
  border: 1px solid #e5e7eb;
}

.content-wrapper {
  position: relative;
}

.plan-text {
  white-space: pre-wrap;
  color: #1f2937;
  font-family: inherit;
  line-height: 1.7;
  margin: 0;
  font-size: 0.95rem;
}

/* 历史计划 */
.history-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 1.5rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  padding: 2.5rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  animation: slideInUp 0.8s ease-out 0.5s both;
}

.history-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.history-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.history-title h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.history-count {
  font-size: 0.9rem;
  color: #6b7280;
  background: rgba(107, 114, 128, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 0.75rem;
}

.history-list {
  width: 100%;
}

.history-items {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.history-item {
  padding: 1.5rem;
  background: linear-gradient(135deg, #fff7ed, #fed7aa);
  border-radius: 1rem;
  border: 1px solid #fed7aa;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  animation: itemSlideIn 0.6s ease-out both;
  transition: all 0.3s ease;
}

.history-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.1);
}

@keyframes itemSlideIn {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.item-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.item-number {
  font-weight: 700;
  color: #ea580c;
  font-size: 1rem;
}

.item-stage {
  font-size: 0.85rem;
  color: #6b7280;
  background: rgba(107, 114, 128, 0.1);
  padding: 0.25rem 0.75rem;
  border-radius: 0.5rem;
}

.item-content {
  position: relative;
}

.item-text {
  white-space: pre-wrap;
  font-size: 0.9rem;
  color: #374151;
  font-family: inherit;
  line-height: 1.6;
  margin: 0;
}

/* 过渡动画 */
.fade-up-enter-active, .fade-up-leave-active {
  transition: all 0.5s ease;
}

.fade-up-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.fade-up-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}

.list-enter-active, .list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .plan-page {
    padding: 1rem;
  }
  
  .main-title {
    font-size: 2rem;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .button-group {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
  
  .plan-header, .history-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .plan-meta {
    width: 100%;
    justify-content: flex-start;
  }
}

@media (max-width: 480px) {
  .form-card, .plan-card, .history-card {
    padding: 1.5rem;
  }
  
  .main-title {
    font-size: 1.75rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
}
</style>

