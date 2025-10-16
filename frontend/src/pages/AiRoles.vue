<template>
  <div class="min-h-screen animate-gradient-flow bg-gradient-to-br from-purple-50 via-pink-50 to-indigo-50 p-4 md:p-6">
    <div class="max-w-6xl mx-auto">
      <!-- 角色选择阶段 -->
      <div v-if="!selectedRole">
        <div class="text-center mb-10 animate-fade-in">
          <h1 class="text-4xl font-bold mb-3">
            <span class="gradient-text-purple">AI 心理助手</span>
          </h1>
          <p class="text-gray-600 text-lg">选择适合您的专业心理师 AI，每个 AI 都有独特的背景与风格</p>
        </div>

        <!-- 角色卡片网格 -->
        <div class="grid md:grid-cols-2 gap-6 mb-8">
          <div 
            v-for="(role, index) in aiRoles" 
            :key="role.id"
            class="glass-effect rounded-3xl shadow-xl overflow-hidden border border-white/30 card-hover cursor-pointer group animate-fade-in"
            :style="{ animationDelay: `${index * 0.1}s` }"
            @click="selectRole(role)"
          >
            <!-- 渐变头部 -->
            <div class="bg-gradient-to-br from-purple-500 via-pink-500 to-indigo-500 p-8 text-white relative overflow-hidden">
              <!-- 背景装饰 -->
              <div class="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full blur-2xl -mr-16 -mt-16"></div>
              
              <div class="flex items-center relative z-10">
                <!-- 头像 -->
                <div class="w-20 h-20 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center mr-5 shadow-lg group-hover:scale-110 transition-transform duration-300">
                  <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                  </svg>
                </div>
                <div>
                  <h2 class="text-2xl font-bold mb-1">{{ role.role_name }}</h2>
                  <p class="text-purple-100 text-sm flex items-center">
                    <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
                    </svg>
                    专业心理咨询师
                  </p>
                </div>
              </div>
            </div>
            
            <!-- 卡片内容 -->
            <div class="p-6 bg-white/50">
              <div class="space-y-3 mb-6">
                <div class="flex items-start">
                  <div class="w-2 h-2 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full mt-2 mr-3 flex-shrink-0 animate-pulse"></div>
                  <p class="text-sm text-gray-700 leading-relaxed">{{ getRoleDescription(role.role_name) }}</p>
                </div>
              </div>
              
              <!-- 选择按钮 -->
              <button class="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3.5 px-6 rounded-xl font-semibold hover:from-purple-700 hover:to-pink-700 transition-all shadow-lg button-hover flex items-center justify-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                </svg>
                选择 {{ role.role_name }}
              </button>
            </div>
          </div>
        </div>

        <!-- 加载状态 -->
        <div v-if="isLoadingRoles" class="text-center py-16">
          <div class="animate-spin rounded-full h-16 w-16 border-4 border-purple-200 border-t-purple-600 mx-auto"></div>
          <p class="mt-4 text-gray-600 font-medium">加载AI角色中...</p>
        </div>
      </div>

      <!-- 聊天界面 -->
      <div v-else class="glass-effect rounded-3xl shadow-2xl overflow-hidden border border-white/30 animate-fade-in-scale" style="height: 85vh;">
        <!-- 聊天头部 -->
        <div class="bg-gradient-to-r from-purple-600 via-pink-600 to-indigo-600 p-5 text-white relative overflow-hidden">
          <!-- 背景装饰 -->
          <div class="absolute inset-0">
            <div class="absolute w-64 h-64 bg-white/10 rounded-full blur-3xl -top-32 -right-32"></div>
            <div class="absolute w-48 h-48 bg-white/10 rounded-full blur-2xl -bottom-24 -left-24"></div>
          </div>
          
          <div class="flex items-center justify-between relative z-10">
            <div class="flex items-center">
              <!-- 返回按钮 -->
              <button 
                @click="goBackToRoles"
                class="mr-4 p-2.5 hover:bg-white/20 rounded-xl transition-all duration-300 hover:scale-105"
              >
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"></path>
                </svg>
              </button>
              
              <!-- AI 头像和信息 -->
              <div class="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center mr-4 animate-float">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </div>
              <div>
                <h2 class="font-bold text-lg">{{ selectedRole.role_name }}</h2>
                <p class="text-sm text-purple-100 flex items-center">
                  <span class="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></span>
                  在线 · 随时为您服务
                </p>
              </div>
            </div>
            
            <!-- 清空按钮 -->
            <button 
              @click="clearChat"
              class="p-2.5 hover:bg-white/20 rounded-xl transition-all duration-300 hover:scale-105"
              title="清空聊天记录"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
              </svg>
            </button>
          </div>
        </div>

        <!-- 聊天消息区域 -->
        <div class="flex-1 overflow-y-auto p-6 space-y-6 bg-gradient-to-br from-white/30 to-white/10" style="height: calc(85vh - 180px);" ref="chatContainer">
          <!-- 欢迎消息 -->
          <div v-if="chatHistory.length === 0" class="text-center py-12 animate-fade-in">
            <div class="w-20 h-20 bg-gradient-to-br from-purple-400 to-pink-400 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-lg animate-bounce-in">
              <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-gray-800 mb-3">欢迎与{{ selectedRole.role_name }}对话</h3>
            <p class="text-gray-600 max-w-md mx-auto">请随时分享您的想法和感受，我会用专业的视角为您提供支持</p>
          </div>

          <!-- 聊天消息 -->
          <div 
            v-for="(msg, idx) in chatHistory" 
            :key="idx"
            class="animate-fade-in"
            :style="{ animationDelay: `${idx * 0.05}s` }"
          >
            <!-- 用户消息 -->
            <div v-if="msg.is_user" class="flex justify-end">
              <div class="max-w-[75%]">
                <div class="bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-2xl rounded-tr-sm px-5 py-3.5 shadow-lg">
                  <p class="whitespace-pre-wrap break-words">{{ msg.message }}</p>
                  <img v-if="msg.image_url" :src="msg.image_url" class="mt-3 rounded-xl max-w-full shadow-md" />
                </div>
                <p class="text-xs text-gray-500 mt-2 text-right">{{ formatTime(msg.timestamp) }}</p>
              </div>
            </div>

            <!-- AI消息 -->
            <div v-else class="flex justify-start">
              <div class="flex items-start max-w-[75%] gap-3">
                <!-- AI头像 -->
                <div class="w-10 h-10 bg-gradient-to-br from-purple-400 to-pink-400 rounded-xl flex items-center justify-center flex-shrink-0 shadow-md">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                  </svg>
                </div>
                
                <!-- 消息气泡 -->
                <div>
                  <div class="bg-white/80 backdrop-blur-sm rounded-2xl rounded-tl-sm px-5 py-3.5 shadow-lg border border-white/50">
                    <div class="prose prose-sm max-w-none" v-html="renderMarkdown(msg.message)"></div>
                  </div>
                  <p class="text-xs text-gray-500 mt-2">{{ formatTime(msg.timestamp) }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 正在输入提示 -->
          <div v-if="showTyping" class="flex justify-start animate-fade-in">
            <div class="flex items-start max-w-[75%] gap-3">
              <div class="w-10 h-10 bg-gradient-to-br from-purple-400 to-pink-400 rounded-xl flex items-center justify-center flex-shrink-0 shadow-md animate-pulse">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                </svg>
              </div>
              <div class="bg-white/80 backdrop-blur-sm rounded-2xl rounded-tl-sm px-6 py-4 shadow-lg border border-white/50">
                <div class="flex gap-2">
                  <div class="w-2.5 h-2.5 bg-purple-500 rounded-full animate-bounce"></div>
                  <div class="w-2.5 h-2.5 bg-purple-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                  <div class="w-2.5 h-2.5 bg-purple-500 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 输入区域 -->
        <div class="bg-white/80 backdrop-blur-sm p-5 border-t border-white/50">
          <form @submit.prevent="sendMessage" class="flex items-end gap-3">
            <!-- 图片上传 -->
            <input ref="imagePicker" type="file" accept="image/*" @change="onPickImage" class="hidden" />
            <button 
              type="button"
              @click="imagePicker.click()"
              class="p-3 bg-gradient-to-br from-purple-100 to-pink-100 text-purple-600 rounded-xl hover:from-purple-200 hover:to-pink-200 transition-all shadow-md hover:shadow-lg hover:scale-105"
              title="上传图片"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
            </button>

            <!-- 输入框区域 -->
            <div class="flex-1">
              <!-- 图片预览 -->
              <div v-if="pendingImageUrl" class="mb-3 relative inline-block">
                <img :src="pendingImageUrl" class="h-20 rounded-lg shadow-md border-2 border-purple-200" />
                <button 
                  @click="clearPendingImage"
                  class="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors shadow-lg flex items-center justify-center"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
              </div>
              
              <!-- 文本输入 -->
              <textarea
                v-model="newMessage"
                @keydown.enter.exact.prevent="sendMessage"
                placeholder="输入您的消息... (Enter发送，Shift+Enter换行)"
                rows="1"
                class="w-full px-5 py-3.5 bg-white/80 border-2 border-purple-200 rounded-xl focus:outline-none focus:border-purple-400 focus:ring-4 focus:ring-purple-100 resize-none transition-all duration-300 placeholder-gray-400"
                :disabled="isTyping || isSending"
              ></textarea>
            </div>

            <!-- 发送按钮 -->
            <button 
              type="submit"
              :disabled="!newMessage.trim() || isTyping || isSending"
              class="px-8 py-3.5 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl font-semibold hover:from-purple-700 hover:to-pink-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl button-hover"
            >
              <span v-if="!isSending && !isTyping" class="flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                </svg>
                发送
              </span>
              <span v-else class="flex items-center">
                <svg class="animate-spin h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                发送中
              </span>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import { aiApi } from '../api/index.js'

const userId = localStorage.getItem('user_id')

// 数据状态
const aiRoles = ref([])
const selectedRole = ref(null)
const chatHistory = ref([])
const newMessage = ref('')
const isLoadingRoles = ref(false)
const isTyping = ref(false)
const isSending = ref(false)
const showTyping = ref(false)
let typingTimer = null
const chatContainer = ref(null)
const imagePicker = ref(null)
const pendingImageUrl = ref('')
const pendingImageDataUrl = ref('')

// 加载AI角色列表
const loadAiRoles = async () => {
  isLoadingRoles.value = true
  try {
    const data = await aiApi.getRoles()
    aiRoles.value = data
  } catch (error) {
    console.error('加载AI角色失败:', error)
  } finally {
    isLoadingRoles.value = false
  }
}

// 选择角色
const selectRole = async (role) => {
  selectedRole.value = role
  await loadChatHistory()
}

// 返回角色选择
const goBackToRoles = () => {
  selectedRole.value = null
  chatHistory.value = []
}

// 加载聊天历史
const loadChatHistory = async () => {
  if (!userId || !selectedRole.value) return

  try {
    const data = await aiApi.getHistory(userId, selectedRole.value.id, 20)
    chatHistory.value = data.reverse()
    await scrollToBottom()
  } catch (error) {
    console.error('加载聊天历史失败:', error)
  }
}

// 发送消息
const sendMessage = async () => {
  if (!newMessage.value.trim() || !selectedRole.value || isTyping.value) return

  const message = newMessage.value.trim()
  const imageUrl = pendingImageUrl.value
  const imageDataUrl = pendingImageDataUrl.value
  
  newMessage.value = ''
  pendingImageUrl.value = ''
  pendingImageDataUrl.value = ''

  // 添加用户消息
  chatHistory.value.push({
    message: message,
    is_user: true,
    timestamp: new Date().toISOString(),
    image_url: imageUrl || null
  })

  await scrollToBottom()
  showTyping.value = true
  isSending.value = true

  try {
    const data = await callWithRetry(() => aiApi.chat(
      userId,
      selectedRole.value.id,
      message,
      imageUrl || null,
      null,
      {
        extraFields: { image_data_url: imageDataUrl || '' },
      }
    ), 2)
    
    const reply = (data && (data.reply || data.ai_response)) || ''
    showTyping.value = false
    
    chatHistory.value.push({
      message: String(reply),
      is_user: false,
      timestamp: new Date().toISOString()
    })
  } catch (error) {
    console.error('发送消息失败:', error)
    chatHistory.value.push({
      message: error.message || '抱歉，我现在无法回复，请稍后再试。',
      is_user: false,
      timestamp: new Date().toISOString()
    })
  } finally {
    isTyping.value = false
    isSending.value = false
    await scrollToBottom()
  }
}

// 清空聊天记录
const clearChat = async () => {
  if (!selectedRole.value) return
  if (!confirm('确定要清空聊天记录吗？此操作不可撤销。')) return
  
  try {
    stopTyping()
    isTyping.value = false
    showTyping.value = false
    await aiApi.clearHistory(userId, selectedRole.value.id)
    chatHistory.value = []
  } catch (e) {
    console.error('清空失败', e)
  }
}

// 滚动到底部
const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

function stopTyping() {
  if (typingTimer) {
    clearInterval(typingTimer)
    typingTimer = null
  }
}

// 选择图片并上传
async function onPickImage(e) {
  const file = e.target.files && e.target.files[0]
  if (!file) return
  
  try {
    const formData = new FormData()
    formData.append('file', file)
    const resp = await fetch('/api/upload/image', { method: 'POST', body: formData })
    const data = await resp.json()
    pendingImageUrl.value = data.url || ''
    pendingImageDataUrl.value = data.data_url || ''
  } catch (err) {
    console.error('图片上传失败', err)
    pendingImageUrl.value = ''
  } finally {
    if (imagePicker.value) imagePicker.value.value = ''
  }
}

function clearPendingImage() {
  pendingImageUrl.value = ''
  pendingImageDataUrl.value = ''
}

// 渲染 Markdown
function renderMarkdown(text) {
  try {
    const html = marked.parse(String(text || ''))
    return DOMPurify.sanitize(html)
  } catch (e) {
    return DOMPurify.sanitize(String(text || ''))
  }
}

// 带重试的请求
async function callWithRetry(fn, retries = 2) {
  let attempt = 0
  let lastErr
  
  while (attempt <= retries) {
    try {
      return await fn()
    } catch (e) {
      lastErr = e
      const delay = Math.min(1500 * Math.pow(2, attempt), 4000)
      await new Promise(r => setTimeout(r, delay))
      attempt++
    }
  }
  throw lastErr || new Error('请求失败')
}

// 获取角色描述
const getRoleDescription = (roleName) => {
  const descriptions = {
    '温柔心理师': '专注于提供温暖、理解和支持的心理咨询服务，擅长倾听和情感疏导，用温柔的方式帮助您探索内心世界',
    '元气生活教练': '充满活力的生活指导师，专注于积极心态建设和生活方式优化，帮助您发现生活的美好',
    '认知行为治疗师': '专精CBT认知行为疗法，帮助识别和改变负面思维模式，提供结构化的问题解决方案',
    '正念减压导师': '专注于正念冥想和减压技巧，引导您活在当下，减轻焦虑和压力',
    '情绪调节专家': '专长于情绪识别和管理，帮助您理解和调节复杂情绪，建立健康的情绪表达方式',
    '人际关系咨询师': '擅长处理人际关系问题，包括家庭、友情、爱情，帮助您建立健康的社交模式',
    '创伤康复治疗师': '专注于创伤后应激障碍（PTSD）和创伤治疗，提供安全的疗愈环境',
    '青少年心理导师': '专门服务青少年群体，理解年轻人的困扰，提供成长期的心理支持',
    '职场压力顾问': '专注于职场心理健康，帮助应对工作压力、职业倦怠和工作生活平衡',
    '睡眠健康教练': '专注于改善睡眠质量，提供科学的睡眠卫生建议和放松技巧'
  }
  return descriptions[roleName] || '专业的心理健康咨询师，为您提供个性化的心理支持和专业指导'
}

// 格式化时间
const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

// 初始化
onMounted(() => {
  loadAiRoles()
})
</script>

<style scoped>
/* Markdown 样式美化 */
:deep(.prose) {
  color: #374151;
  line-height: 1.75;
}

:deep(.prose p) {
  margin: 0.75em 0;
}

:deep(.prose strong) {
  color: #1f2937;
  font-weight: 600;
}

:deep(.prose ul) {
  list-style-type: disc;
  padding-left: 1.5em;
  margin: 0.75em 0;
}

:deep(.prose ol) {
  list-style-type: decimal;
  padding-left: 1.5em;
  margin: 0.75em 0;
}

:deep(.prose li) {
  margin: 0.5em 0;
}

:deep(.prose code) {
  background: #f3f4f6;
  padding: 0.2em 0.4em;
  border-radius: 0.25rem;
  font-size: 0.9em;
}

:deep(.prose pre) {
  background: #1f2937;
  color: #f9fafb;
  padding: 1em;
  border-radius: 0.5rem;
  overflow-x: auto;
  margin: 1em 0;
}

/* 滚动条美化 */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(139, 92, 246, 0.3);
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(139, 92, 246, 0.5);
}
</style>
