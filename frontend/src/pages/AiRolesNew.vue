<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
    <!-- 顶部导航栏 -->
    <nav class="sticky top-0 z-50 glass border-b border-white/20 backdrop-blur-xl">
      <div class="container-custom">
        <div class="flex items-center justify-between h-16">
          <button 
            @click="goBack"
            class="flex items-center space-x-2 text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
            </svg>
            <span class="font-medium">返回</span>
          </button>
          
          <h1 class="text-xl font-bold text-gray-900 dark:text-white">
            {{ selectedRole ? selectedRole.name : 'AI 心理咨询' }}
          </h1>
          
          <button 
            v-if="selectedRole"
            @click="confirmClearChat"
            class="px-4 py-2 text-sm font-medium text-danger-600 hover:bg-danger-50 dark:hover:bg-danger-900/20 rounded-lg transition-colors"
          >
            清空对话
          </button>
          <div v-else class="w-20"></div>
        </div>
      </div>
    </nav>

    <!-- 主内容区 -->
    <div class="container-custom py-8">
      <!-- AI角色选择（未选择时显示） -->
      <div v-if="!selectedRole" class="max-w-6xl mx-auto">
        <div 
          v-motion
          :initial="{ opacity: 0, y: -20 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 600 } }"
          class="text-center mb-12"
        >
          <h2 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            选择您的 <span class="text-gradient-primary">AI 心理师</span>
          </h2>
          <p class="text-lg text-gray-600 dark:text-gray-300">
            10位专业AI心理师，为您提供个性化的心理支持
          </p>
        </div>

        <!-- 角色卡片网格 -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="(role, index) in aiRoles"
            :key="role.id"
            v-motion
            :initial="{ opacity: 0, y: 50 }"
            :enter="{ opacity: 1, y: 0, transition: { delay: index * 100, duration: 500 } }"
            @click="selectRole(role)"
            class="group cursor-pointer"
          >
            <div class="glass-card p-6 h-full hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 relative overflow-hidden">
              <!-- 装饰性背景 -->
              <div class="absolute inset-0 bg-gradient-to-br opacity-0 group-hover:opacity-10 transition-opacity duration-300"
                   :style="{ background: `linear-gradient(135deg, ${role.color || '#8b5cf6'}, ${role.color2 || '#06b6d4'})` }">
              </div>

              <!-- 头像 -->
              <div class="relative z-10 mb-4 flex justify-center">
                <div class="w-20 h-20 rounded-2xl flex items-center justify-center shadow-xl transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-300"
                     :style="{ background: `linear-gradient(135deg, ${role.color || '#8b5cf6'}, ${role.color2 || '#06b6d4'})` }">
                  <span class="text-3xl">{{ role.emoji || '🧠' }}</span>
                </div>
              </div>

              <!-- 角色信息 -->
              <div class="relative z-10 text-center">
                <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">
                  {{ role.name }}
                </h3>
                <p class="text-sm text-gray-600 dark:text-gray-400 mb-4 line-clamp-3">
                  {{ role.description }}
                </p>
                
                <!-- 标签 -->
                <div class="flex flex-wrap justify-center gap-2 mb-4">
                  <span 
                    v-for="tag in role.tags" 
                    :key="tag"
                    class="badge text-xs"
                    :style="{ 
                      backgroundColor: `${role.color || '#8b5cf6'}20`,
                      color: role.color || '#8b5cf6'
                    }"
                  >
                    {{ tag }}
                  </span>
                </div>

                <!-- 选择按钮 -->
                <button class="btn btn-primary w-full opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  开始对话
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 聊天界面（选择角色后显示） -->
      <div v-else class="max-w-5xl mx-auto">
        <div class="glass-card p-0 overflow-hidden">
          <!-- 角色信息头部 -->
          <div class="bg-gradient-to-r p-6 border-b border-white/20"
               :style="{ background: `linear-gradient(135deg, ${selectedRole.color || '#8b5cf6'}, ${selectedRole.color2 || '#06b6d4'})` }">
            <div class="flex items-center space-x-4">
              <div class="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center shadow-xl">
                <span class="text-3xl">{{ selectedRole.emoji || '🧠' }}</span>
              </div>
              <div class="flex-1">
                <h3 class="text-2xl font-bold text-white mb-1">{{ selectedRole.name }}</h3>
                <p class="text-white/80 text-sm">{{ selectedRole.description }}</p>
              </div>
              <div class="hidden sm:flex space-x-2">
                <span 
                  v-for="tag in selectedRole.tags?.slice(0, 3)" 
                  :key="tag"
                  class="px-3 py-1 bg-white/20 backdrop-blur-sm rounded-full text-xs text-white font-medium"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>

          <!-- 聊天消息区域 -->
          <div 
            ref="chatContainer"
            class="h-[500px] overflow-y-auto p-6 space-y-4 scrollbar-thin bg-gradient-to-b from-transparent to-gray-50/50 dark:to-gray-900/50"
          >
            <!-- 欢迎消息 -->
            <div 
              v-if="messages.length === 0"
              v-motion
              :initial="{ opacity: 0, scale: 0.9 }"
              :enter="{ opacity: 1, scale: 1, transition: { duration: 500 } }"
              class="text-center py-12"
            >
              <div class="w-24 h-24 mx-auto mb-6 rounded-3xl flex items-center justify-center shadow-2xl transform animate-float"
                   :style="{ background: `linear-gradient(135deg, ${selectedRole.color || '#8b5cf6'}, ${selectedRole.color2 || '#06b6d4'})` }">
                <span class="text-5xl">{{ selectedRole.emoji || '🧠' }}</span>
              </div>
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">
                你好！我是 {{ selectedRole.name }}
              </h3>
              <p class="text-gray-600 dark:text-gray-400 max-w-md mx-auto">
                {{ selectedRole.greeting || '有什么我可以帮助你的吗？' }}
              </p>
            </div>

            <!-- 消息列表 -->
            <div
              v-for="(msg, index) in messages"
              :key="index"
              v-motion
              :initial="{ opacity: 0, y: 20 }"
              :enter="{ opacity: 1, y: 0, transition: { duration: 400 } }"
              :class="[
                'flex',
                msg.role === 'user' ? 'justify-end' : 'justify-start'
              ]"
            >
              <!-- AI消息 -->
              <div v-if="msg.role === 'assistant'" class="flex items-start space-x-3 max-w-[80%]">
                <div class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 shadow-lg transform hover:scale-110 transition-transform"
                     :style="{ background: `linear-gradient(135deg, ${selectedRole.color || '#8b5cf6'}, ${selectedRole.color2 || '#06b6d4'})` }">
                  <span class="text-xl">{{ selectedRole.emoji || '🧠' }}</span>
                </div>
                <div class="flex-1">
                  <div class="glass-card-strong p-4 rounded-2xl rounded-tl-sm">
                    <p class="text-gray-900 dark:text-white whitespace-pre-wrap leading-relaxed">
                      {{ msg.content }}
                    </p>
                    <!-- 图片显示 -->
                    <div v-if="msg.images && msg.images.length > 0" class="mt-3 space-y-2">
                      <img 
                        v-for="(imgUrl, imgIdx) in msg.images" 
                        :key="imgIdx"
                        :src="imgUrl" 
                        class="max-w-full h-auto rounded-xl shadow-lg hover:scale-105 transition-transform cursor-pointer"
                        @click="previewImage(imgUrl)"
                      />
                    </div>
                  </div>
                  <p class="text-xs text-gray-400 dark:text-gray-500 mt-2 ml-1">
                    {{ formatTime(msg.timestamp) }}
                  </p>
                </div>
              </div>

              <!-- 用户消息 -->
              <div v-else class="flex items-start space-x-3 max-w-[80%]">
                <div class="flex-1">
                  <div class="bg-gradient-to-r from-primary-600 to-secondary-600 p-4 rounded-2xl rounded-tr-sm shadow-lg">
                    <p class="text-white whitespace-pre-wrap leading-relaxed">
                      {{ msg.content }}
                    </p>
                    <!-- 图片显示 -->
                    <div v-if="msg.images && msg.images.length > 0" class="mt-3 space-y-2">
                      <img 
                        v-for="(imgUrl, imgIdx) in msg.images" 
                        :key="imgIdx"
                        :src="imgUrl" 
                        class="max-w-full h-auto rounded-xl shadow-lg hover:scale-105 transition-transform cursor-pointer"
                        @click="previewImage(imgUrl)"
                      />
                    </div>
                  </div>
                  <p class="text-xs text-gray-400 dark:text-gray-500 mt-2 mr-1 text-right">
                    {{ formatTime(msg.timestamp) }}
                  </p>
                </div>
                <div class="w-10 h-10 bg-gradient-to-br from-primary-400 to-secondary-400 rounded-xl flex items-center justify-center flex-shrink-0 shadow-lg">
                  <span class="text-white font-semibold text-sm">{{ username.charAt(0).toUpperCase() }}</span>
                </div>
              </div>
            </div>

            <!-- AI正在输入 -->
            <div v-if="isTyping" class="flex items-start space-x-3">
              <div class="w-10 h-10 rounded-xl flex items-center justify-center shadow-lg animate-pulse"
                   :style="{ background: `linear-gradient(135deg, ${selectedRole.color || '#8b5cf6'}, ${selectedRole.color2 || '#06b6d4'})` }">
                <span class="text-xl">{{ selectedRole.emoji || '🧠' }}</span>
              </div>
              <div class="glass-card-strong p-4 rounded-2xl rounded-tl-sm">
                <div class="flex space-x-2">
                  <div class="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
                  <div class="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style="animation-delay: 0.2s"></div>
                  <div class="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style="animation-delay: 0.4s"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- 输入区域 -->
          <div class="border-t border-gray-200 dark:border-gray-700 p-4 bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm">
            <!-- 图片预览 -->
            <div v-if="selectedImages.length > 0" class="mb-4 flex flex-wrap gap-2">
              <div 
                v-for="(img, index) in selectedImages" 
                :key="index"
                class="relative group"
              >
                <img 
                  :src="img.preview" 
                  class="w-20 h-20 object-cover rounded-lg shadow-lg"
                />
                <button 
                  @click="removeImage(index)"
                  class="absolute -top-2 -right-2 w-6 h-6 bg-danger-500 hover:bg-danger-600 text-white rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity shadow-lg"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
              </div>
            </div>

            <!-- 输入框 -->
            <div class="flex items-end space-x-3">
              <!-- 图片上传 -->
              <label class="flex-shrink-0 cursor-pointer">
                <input 
                  type="file" 
                  accept="image/*" 
                  multiple
                  @change="handleImageSelect"
                  class="hidden"
                />
                <div class="w-10 h-10 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-xl flex items-center justify-center transition-colors">
                  <svg class="w-5 h-5 text-gray-600 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                </div>
              </label>

              <!-- 文本输入 -->
              <textarea
                v-model="inputMessage"
                @keydown.enter.exact.prevent="sendMessage"
                placeholder="输入您的消息..."
                rows="1"
                class="flex-1 px-4 py-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                :disabled="isTyping"
              ></textarea>

              <!-- 发送按钮 -->
              <button
                @click="sendMessage"
                :disabled="!inputMessage.trim() || isTyping"
                class="flex-shrink-0 w-10 h-10 bg-gradient-to-r from-primary-600 to-secondary-600 hover:from-primary-700 hover:to-secondary-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-xl flex items-center justify-center shadow-lg transition-all transform hover:scale-110 active:scale-95"
              >
                <svg class="w-5 h-5 text-white transform rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                </svg>
              </button>
            </div>

            <!-- 提示文字 -->
            <p class="text-xs text-gray-400 dark:text-gray-500 mt-2 text-center">
              按 Enter 发送，Shift + Enter 换行
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 用户数据
const username = ref(localStorage.getItem('username') || '用户')
const userId = localStorage.getItem('user_id')

// AI角色列表
const aiRoles = ref([])
const selectedRole = ref(null)

// 聊天数据
const messages = ref([])
const inputMessage = ref('')
const isTyping = ref(false)
const selectedImages = ref([])

// DOM引用
const chatContainer = ref(null)

// 加载AI角色
const loadAiRoles = async () => {
  try {
    const response = await fetch('/api/ai/roles')
    if (response.ok) {
      const data = await response.json()
      aiRoles.value = data.map(role => ({
        ...role,
        color: getColorForRole(role.name),
        color2: getColor2ForRole(role.name),
        emoji: getEmojiForRole(role.name),
        tags: getTagsForRole(role.name),
        greeting: getGreetingForRole(role.name)
      }))
    }
  } catch (error) {
    console.error('加载AI角色失败:', error)
  }
}

// 获取角色颜色
const getColorForRole = (name) => {
  const colors = {
    '温柔心理师': '#8b5cf6',
    'CBT治疗师': '#06b6d4',
    '正念导师': '#10b981',
    '积极心理学家': '#f59e0b',
    '情绪聚焦治疗师': '#ec4899',
    '创伤疗愈师': '#8b5cf6',
    '青少年心理师': '#06b6d4',
    '职场心理师': '#10b981',
    '关系咨询师': '#f59e0b',
    '存在主义治疗师': '#6366f1'
  }
  return colors[name] || '#8b5cf6'
}

const getColor2ForRole = (name) => {
  const colors = {
    '温柔心理师': '#a78bfa',
    'CBT治疗师': '#22d3ee',
    '正念导师': '#34d399',
    '积极心理学家': '#fbbf24',
    '情绪聚焦治疗师': '#f472b6',
    '创伤疗愈师': '#a78bfa',
    '青少年心理师': '#22d3ee',
    '职场心理师': '#34d399',
    '关系咨询师': '#fbbf24',
    '存在主义治疗师': '#818cf8'
  }
  return colors[name] || '#a78bfa'
}

const getEmojiForRole = (name) => {
  const emojis = {
    '温柔心理师': '💝',
    'CBT治疗师': '🧠',
    '正念导师': '🧘',
    '积极心理学家': '🌟',
    '情绪聚焦治疗师': '❤️',
    '创伤疗愈师': '🌈',
    '青少年心理师': '🎯',
    '职场心理师': '💼',
    '关系咨询师': '💑',
    '存在主义治疗师': '🌌'
  }
  return emojis[name] || '🧠'
}

const getTagsForRole = (name) => {
  const tags = {
    '温柔心理师': ['人本主义', '倾听', '共情'],
    'CBT治疗师': ['认知重构', '行为改变', '实用'],
    '正念导师': ['冥想', '当下', '接纳'],
    '积极心理学家': ['优势', '幸福', '成长'],
    '情绪聚焦治疗师': ['情绪觉察', 'EFT', '深度'],
    '创伤疗愈师': ['创伤知情', 'PTSD', '安全'],
    '青少年心理师': ['青春期', '成长', '理解'],
    '职场心理师': ['职业发展', '压力管理', '效能'],
    '关系咨询师': ['亲密关系', '沟通', '修复'],
    '存在主义治疗师': ['意义', '自由', '责任']
  }
  return tags[name] || ['心理咨询']
}

const getGreetingForRole = (name) => {
  const greetings = {
    '温柔心理师': '很高兴见到你，让我们一起探索你的内心世界吧',
    'CBT治疗师': '你好！我可以帮助你识别和改变负面思维模式',
    '正念导师': '欢迎来到正念的世界，让我们一起活在当下',
    '积极心理学家': '你好！让我们一起发现你的优势和潜能',
    '情绪聚焦治疗师': '欢迎！让我们一起探索你的情绪体验',
    '创伤疗愈师': '你好，这里是安全的空间，我会陪伴你疗愈',
    '青少年心理师': '嗨！我理解青春期的困惑，让我们一起聊聊',
    '职场心理师': '你好！职场压力不要怕，我们一起应对',
    '关系咨询师': '欢迎！让我们一起改善你的人际关系',
    '存在主义治疗师': '你好，让我们一起探索生命的意义'
  }
  return greetings[name] || '有什么我可以帮助你的吗？'
}

// 选择角色
const selectRole = async (role) => {
  selectedRole.value = role
  await loadChatHistory()
}

// 加载聊天历史
const loadChatHistory = async () => {
  if (!userId || !selectedRole.value) return

  try {
    const response = await fetch(`/api/ai/history?user_id=${userId}&role_id=${selectedRole.value.id}`)
    if (response.ok) {
      const data = await response.json()
      messages.value = data.map(msg => ({
        role: msg.role,
        content: msg.content,
        timestamp: msg.timestamp,
        images: msg.images || []
      }))
      await nextTick()
      scrollToBottom()
    }
  } catch (error) {
    console.error('加载聊天历史失败:', error)
  }
}

// 发送消息
const sendMessage = async () => {
  if (!inputMessage.value.trim() || isTyping.value || !selectedRole.value) return

  const userMessage = inputMessage.value.trim()
  const images = selectedImages.value.map(img => img.dataUrl)

  // 添加用户消息到界面
  messages.value.push({
    role: 'user',
    content: userMessage,
    timestamp: new Date().toISOString(),
    images: selectedImages.value.map(img => img.preview)
  })

  inputMessage.value = ''
  selectedImages.value = []
  isTyping.value = true

  await nextTick()
  scrollToBottom()

  try {
    const response = await fetch('/api/ai/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: parseInt(userId),
        role_id: selectedRole.value.id,
        message: userMessage,
        image_data_urls: images
      }),
    })

    if (response.ok) {
      const data = await response.json()
      messages.value.push({
        role: 'assistant',
        content: data.response,
        timestamp: new Date().toISOString()
      })
      await nextTick()
      scrollToBottom()
    } else {
      throw new Error('发送失败')
    }
  } catch (error) {
    console.error('发送消息失败:', error)
    messages.value.push({
      role: 'assistant',
      content: '抱歉，我现在无法回复。请稍后再试。',
      timestamp: new Date().toISOString()
    })
  } finally {
    isTyping.value = false
  }
}

// 图片选择
const handleImageSelect = (event) => {
  const files = Array.from(event.target.files)
  files.forEach(file => {
    if (file.type.startsWith('image/') && selectedImages.value.length < 3) {
      const reader = new FileReader()
      reader.onload = (e) => {
        selectedImages.value.push({
          file,
          preview: e.target.result,
          dataUrl: e.target.result
        })
      }
      reader.readAsDataURL(file)
    }
  })
}

// 移除图片
const removeImage = (index) => {
  selectedImages.value.splice(index, 1)
}

// 图片预览
const previewImage = (url) => {
  window.open(url, '_blank')
}

// 清空对话
const confirmClearChat = () => {
  if (confirm('确定要清空对话记录吗？')) {
    clearChat()
  }
}

const clearChat = async () => {
  if (!userId || !selectedRole.value) return

  try {
    const response = await fetch('/api/ai/clear', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: parseInt(userId),
        role_id: selectedRole.value.id
      }),
    })

    if (response.ok) {
      messages.value = []
    }
  } catch (error) {
    console.error('清空对话失败:', error)
  }
}

// 返回
const goBack = () => {
  if (selectedRole.value) {
    selectedRole.value = null
    messages.value = []
  } else {
    router.push('/home')
  }
}

// 滚动到底部
const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

// 格式化时间
const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  return date.toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

// 监听选中角色变化
watch(selectedRole, (newRole) => {
  if (newRole) {
    scrollToBottom()
  }
})

onMounted(() => {
  loadAiRoles()
})
</script>

<style scoped>
/* 行截断 */
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

