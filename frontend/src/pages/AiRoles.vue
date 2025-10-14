<template>
  <div class="min-h-screen p-2 md:p-4">
    <div class="max-w-6xl mx-auto">
      <!-- 角色选择阶段 -->
      <div v-if="!selectedRole">
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold text-gray-900 mb-2">AI 心理助手</h1>
          <p class="text-gray-600">选择适合您的专业心理师 AI，每个 AI 都有独特的背景与风格</p>
        </div>

        <!-- 角色卡片 -->
        <div class="grid md:grid-cols-2 gap-6 mb-8">
          <div 
            v-for="role in aiRoles" 
            :key="role.id"
            class="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow cursor-pointer border border-gray-100"
            @click="selectRole(role)"
          >
            <div class="bg-gradient-to-r from-purple-500 to-pink-500 p-6 text-white">
              <div class="flex items-center mb-4">
                <div class="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center mr-4">
                  <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                  </svg>
                </div>
                <div>
                  <h2 class="text-2xl font-bold">{{ role.role_name }}</h2>
                  <p class="text-purple-100">专业心理咨询师</p>
                </div>
              </div>
            </div>
            
            <div class="p-6">
              <div class="space-y-4 mb-6">
                <div class="flex items-start">
                  <div class="w-2 h-2 bg-purple-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                  <p class="text-sm text-gray-600">{{ getRoleDescription(role.role_name) }}</p>
                </div>
              </div>
              
              <button class="w-full bg-purple-600 text-white py-3 px-6 rounded-xl font-semibold hover:bg-purple-700 transition-colors">
                选择 {{ role.role_name }}
              </button>
            </div>
          </div>
        </div>

        <!-- 加载状态 -->
        <div v-if="isLoadingRoles" class="text-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
          <p class="mt-4 text-gray-600">加载AI角色中...</p>
        </div>
      </div>

      <!-- 聊天界面 -->
      <div v-else class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100" style="height: 80vh;">
        <!-- 聊天头部 -->
        <div class="bg-gradient-to-r from-purple-500 to-pink-500 p-4 text-white">
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <button 
                @click="goBackToRoles"
                class="mr-4 p-2 hover:bg-white/20 rounded-lg transition-colors"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
                </svg>
              </button>
              <div class="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center mr-3">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </div>
              <div>
                <h2 class="font-bold">{{ selectedRole.role_name }}</h2>
                <p class="text-sm text-purple-100">在线 · 随时为您服务</p>
              </div>
            </div>
            <button 
              @click="clearChat"
              class="p-2 hover:bg-white/20 rounded-lg transition-colors"
              title="清空聊天记录"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
              </svg>
            </button>
          </div>
        </div>

        <!-- 聊天消息区域 -->
        <div class="flex-1 overflow-y-auto p-4 space-y-4" style="height: calc(80vh - 140px);" ref="chatContainer">
          <!-- 欢迎消息 -->
          <div v-if="chatHistory.length === 0" class="text-center py-8">
            <div class="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-800 mb-2">欢迎与{{ selectedRole.role_name }}对话</h3>
            <p class="text-gray-600">您可以向我倾诉任何心理困扰，我会用专业的知识帮助您</p>
          </div>

          <!-- 聊天消息 -->
          <div 
            v-for="(message, index) in chatHistory" 
            :key="index"
            class="flex"
            :class="message.is_user ? 'justify-end' : 'justify-start'"
          >
            <div 
              class="max-w-xs lg:max-w-md px-4 py-2 rounded-lg"
              :class="message.is_user 
                ? 'bg-purple-600 text-white' 
                : 'bg-gray-100 text-gray-800'"
            >
              <div v-if="message.image_url" class="mb-2">
                <img :src="message.image_url" alt="image" class="rounded-lg max-h-48 object-contain" />
              </div>
              <div v-if="message.is_user" class="text-sm whitespace-pre-wrap">{{ message.message }}</div>
              <div v-else class="prose prose-sm max-w-none" v-html="renderMarkdown(message.message)"></div>
              <p class="text-xs mt-1 opacity-70">
                {{ formatTime(message.timestamp) }}
              </p>
            </div>
          </div>

          <!-- 正在输入提示 -->
          <div v-if="showTyping" class="flex justify-start">
            <div class="bg-gray-100 text-gray-800 px-4 py-2 rounded-lg max-w-xs">
              <div class="flex items-center space-x-1">
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- 输入区域 -->
        <div class="border-t bg-gray-50 p-4">
          <form @submit.prevent="sendMessage" class="flex flex-col gap-2 md:flex-row md:items-center md:space-x-2">
            <input 
              v-model="newMessage"
              type="text" 
              placeholder="输入您的消息..."
              class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
              :disabled="isTyping || isSending"
            />
            <input type="file" accept="image/*" @change="onPickImage" class="hidden" ref="imagePicker" />
            <button type="button" @click="imagePicker.click()" class="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">图片</button>
            <div v-if="pendingImageUrl" class="flex items-center gap-2 text-sm text-gray-600">
              <img :src="pendingImageUrl" class="h-8 w-8 object-cover rounded" alt="preview" />
              <button type="button" @click="clearPendingImage" class="text-gray-500 hover:text-gray-700">移除</button>
            </div>
            <div class="flex items-center gap-2">
              <button 
                type="submit"
                :disabled="!newMessage.trim() || isTyping || isSending"
                class="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ isSending || isTyping ? '发送中...' : '发送' }}
              </button>
            </div>
            <!-- 速度调节 -->
            
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
const isTyping = ref(false) // 不再使用打字机
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
    chatHistory.value = data.reverse() // 反转以显示最新消息在底部
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

  // 添加用户消息到聊天历史
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
    // 直接渲染完整回复
    const data = await callWithRetry(() => aiApi.chat(
      userId,
      selectedRole.value.id,
      message,
      imageUrl || null,
      null,
      {
        // 通过 extraFields 传递 image_data_url，避免重写 body
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

// 选择图片并上传，得到 URL
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

// 渲染 Markdown 并进行 XSS 清理
function renderMarkdown(text) {
  try {
    const html = marked.parse(String(text || ''))
    return DOMPurify.sanitize(html)
  } catch (e) {
    return DOMPurify.sanitize(String(text || ''))
  }
}

// 带指数退避的重试
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
    '温柔心理师': '专注于提供温暖、理解和支持的心理咨询服务，擅长倾听和情感疏导',
    '元气生活教练': '充满活力的生活指导师，专注于积极心态建设和生活方式优化'
  }
  return descriptions[roleName] || '专业的心理健康咨询师，为您提供个性化的心理支持'
}

// 格式化时间
const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

onMounted(() => {
  loadAiRoles()
})
</script> 