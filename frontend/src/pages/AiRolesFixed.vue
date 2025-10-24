<template>
  <div class="ai-roles-container">
    <!-- 顶部导航 -->
    <nav class="top-nav">
      <div class="nav-content">
        <button @click="goBack" class="back-button">
          <svg class="back-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
          </svg>
          返回
        </button>
        <h1 class="nav-title">AI 心理咨询</h1>
        <div class="nav-spacer"></div>
      </div>
    </nav>

    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 角色选择（未选择时显示） -->
      <div v-if="!selectedRole" class="roles-section">
        <h2 class="section-title">选择您的专属 AI 心理师</h2>
        <p class="section-subtitle">每位 AI 都有独特的专业领域和咨询风格</p>
        
        <div class="roles-grid">
          <div
            v-for="role in aiRoles"
            :key="role.id"
            @click="selectRole(role)"
            class="role-card"
          >
            <div class="role-icon" :style="{ background: role.gradient }">
              <span class="role-emoji">{{ role.emoji }}</span>
            </div>
            <div class="role-info">
              <h3 class="role-name">{{ role.name }}</h3>
              <p class="role-description">{{ role.description }}</p>
              <div class="role-tags">
                <span v-for="tag in role.tags" :key="tag" class="role-tag">{{ tag }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 聊天界面（选择角色后显示） -->
      <div v-else class="chat-section">
        <!-- 聊天头部 -->
        <div class="chat-header">
          <button @click="selectedRole = null" class="change-role-btn">
            <svg class="change-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
            </svg>
          </button>
          <div class="chat-role-info">
            <div class="chat-role-avatar" :style="{ background: selectedRole.gradient }">
              <span class="chat-role-emoji">{{ selectedRole.emoji }}</span>
            </div>
            <div>
              <h3 class="chat-role-name">{{ selectedRole.name }}</h3>
              <p class="chat-role-status">在线 · 随时为您服务</p>
            </div>
          </div>
          <button @click="clearChat" class="clear-chat-btn">
            <svg class="clear-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
            </svg>
          </button>
        </div>

        <!-- 聊天消息区 -->
        <div class="chat-messages" ref="chatMessages">
          <div
            v-for="(message, index) in messages"
            :key="index"
            :class="['message', message.role === 'user' ? 'message-user' : 'message-ai']"
          >
            <div v-if="message.role === 'assistant'" class="message-avatar ai-avatar" :style="{ background: selectedRole.gradient }">
              <span class="avatar-emoji">{{ selectedRole.emoji }}</span>
            </div>
            <div class="message-content">
              <div class="message-bubble">
                <p class="message-text">{{ message.content }}</p>
              </div>
              <span class="message-time">{{ formatTime(message.timestamp) }}</span>
            </div>
            <div v-if="message.role === 'user'" class="message-avatar user-avatar">
              <svg class="user-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
            </div>
          </div>
          
          <!-- AI正在输入 -->
          <div v-if="isAiTyping" class="message message-ai">
            <div class="message-avatar ai-avatar" :style="{ background: selectedRole.gradient }">
              <span class="avatar-emoji">{{ selectedRole.emoji }}</span>
            </div>
            <div class="message-content">
              <div class="message-bubble typing-bubble">
                <div class="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 输入框 -->
        <div class="chat-input-area">
          <form @submit.prevent="sendMessage" class="chat-input-form">
            <textarea
              v-model="currentMessage"
              placeholder="输入您的消息..."
              class="chat-textarea"
              rows="1"
              @keydown.enter.exact.prevent="sendMessage"
            ></textarea>
            <button type="submit" class="send-button" :disabled="!currentMessage.trim() || isAiTyping">
              <svg class="send-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
              </svg>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AiRolesFixed',
  data() {
    return {
      selectedRole: null,
      messages: [],
      currentMessage: '',
      isAiTyping: false,
      aiRoles: []
    }
  },
  methods: {
    goBack() {
      this.$router.push('/home')
    },
    async fetchRoles() {
      try {
        const res = await fetch('http://localhost:8000/api/ai/roles')
        const data = await res.json()
        this.aiRoles = (data || []).map((r, idx) => ({
          id: r.id,
          name: r.role_name || `AI 心理师 #${r.id}`,
          emoji: r.emoji || this.pickEmoji(r.role_name),  // 使用后端返回的emoji
          description: r.description || '专业心理支持，提供个性化建议',  // 使用后端返回的描述
          tags: r.tags ? r.tags.split(',') : [],  // 使用后端返回的标签
          gradient: r.gradient || this.pickGradient(idx)  // 使用后端返回的渐变色
        }))
      } catch (e) {
        // 回退到内置角色集合（保障页面可用）
        this.aiRoles = [
          { id: 1, name: '认知行为咨询师', emoji: '🧠', description: '帮助您识别和改变消极思维模式', tags: [], gradient: this.pickGradient(0) },
          { id: 2, name: '情绪管理专家', emoji: '💝', description: '理解和管理情绪，提升情绪智力', tags: [], gradient: this.pickGradient(1) },
          { id: 3, name: '正念疗愈师', emoji: '🧘', description: '通过正念冥想帮助您活在当下', tags: [], gradient: this.pickGradient(2) }
        ]
      }
    },
    pickGradient(i) {
      const gs = [
        'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
        'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
        'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
      ]
      return gs[i % gs.length]
    },
    pickEmoji(name = '') {
      if (name && (name.includes('认知') || name.includes('CBT'))) return '🧠'
      if (name && (name.includes('情绪') || name.includes('情感'))) return '💝'
      if (name && (name.includes('正念') || name.includes('冥想'))) return '🧘'
      if (name && name.includes('睡眠')) return '😴'
      if (name && name.includes('关系')) return '🤝'
      if (name && name.includes('成长')) return '🌟'
      return '🧠'
    },
    selectRole(role) {
      this.selectedRole = role
      this.messages = [
        {
          role: 'assistant',
          content: `您好！我是${role.name}，很高兴为您服务。${role.description}请随时告诉我您的困扰，我会尽力帮助您。`,
          timestamp: new Date()
        }
      ]
    },
    async sendMessage() {
      if (!this.currentMessage.trim() || this.isAiTyping) return

      const userMessage = {
        role: 'user',
        content: this.currentMessage,
        timestamp: new Date()
      }
      
      this.messages.push(userMessage)
      const messageToSend = this.currentMessage
      this.currentMessage = ''
      this.isAiTyping = true

      // 滚动到底部
      this.$nextTick(() => {
        this.scrollToBottom()
      })

      try {
        const userStr = localStorage.getItem('user')
        if (!userStr) {
          throw new Error('用户未登录，请先登录')
        }
        const user = JSON.parse(userStr)
        const userId = user.id || user.user_id || 1  // 容错处理
        console.log('Sending chat request:', { user_id: userId, role_id: this.selectedRole.id, message: messageToSend })
        
        const response = await fetch(`http://localhost:8000/api/ai/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            user_id: userId,
            role_id: this.selectedRole.id,
            message: messageToSend
          })
        })

        if (!response.ok) {
          const errorText = await response.text()
          throw new Error(`AI响应失败: ${response.status} ${errorText}`)
        }

        // 处理普通JSON响应
        const data = await response.json()
        console.log('AI响应:', data)
        
        this.isAiTyping = false
        
        // 添加AI回复到消息列表
        this.messages.push({
          role: 'assistant',
          content: data.reply || data.content || '抱歉，我暂时无法回复。',
          timestamp: new Date()
        })
        
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      } catch (error) {
        console.error('发送消息错误:', error)
        this.messages.push({
          role: 'assistant',
          content: '抱歉，我暂时无法回复。请稍后再试。',
          timestamp: new Date()
        })
        this.isAiTyping = false
      }
    },
    async clearChat() {
      this.messages = []
      this.$nextTick(() => this.scrollToBottom())
    },
    formatTime(date) {
      const hours = date.getHours().toString().padStart(2, '0')
      const minutes = date.getMinutes().toString().padStart(2, '0')
      return `${hours}:${minutes}`
    },
    scrollToBottom() {
      const messagesDiv = this.$refs.chatMessages
      if (messagesDiv) {
        messagesDiv.scrollTop = messagesDiv.scrollHeight
      }
    }
  },
  created() {
    this.fetchRoles()
  }
}
</script>

<style scoped>
/* 基础容器 */
.ai-roles-container {
  min-height: 100vh;
  background: linear-gradient(to bottom right, #f9fafb, #ffffff, #f3f4f6);
  font-family: 'Inter var', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  display: flex;
  flex-direction: column;
}

/* 顶部导航 */
.top-nav {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid #e5e7eb;
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 50;
}

.nav-content {
  max-width: 80rem;
  margin: 0 auto;
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: transparent;
  border: none;
  color: #667eea;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  border-radius: 0.5rem;
  transition: all 0.2s ease;
}

.back-button:hover {
  background: #f3f4f6;
}

.back-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.nav-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.nav-spacer {
  width: 5rem;
}

/* 主内容区 */
.main-content {
  flex: 1;
  max-width: 80rem;
  margin: 0 auto;
  padding: 2rem 1.5rem;
  width: 100%;
}

/* 角色选择区域 */
.roles-section {
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  text-align: center;
  margin: 0 0 0.5rem 0;
}

.section-subtitle {
  font-size: 1.125rem;
  color: #6b7280;
  text-align: center;
  margin: 0 0 3rem 0;
}

.roles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.role-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.role-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border-color: #667eea;
}

.role-icon {
  width: 4rem;
  height: 4rem;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.role-emoji {
  font-size: 2rem;
}

.role-info {
  flex: 1;
}

.role-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
}

.role-description {
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.5;
  margin: 0 0 1rem 0;
}

.role-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.role-tag {
  padding: 0.25rem 0.75rem;
  background: #f3f4f6;
  color: #6b7280;
  font-size: 0.75rem;
  border-radius: 9999px;
}

/* 聊天界面 */
.chat-section {
  height: calc(100vh - 10rem);
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.chat-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.change-role-btn,
.clear-chat-btn {
  padding: 0.5rem;
  background: transparent;
  border: none;
  color: #6b7280;
  cursor: pointer;
  border-radius: 0.5rem;
  transition: all 0.2s ease;
}

.change-role-btn:hover,
.clear-chat-btn:hover {
  background: #f3f4f6;
  color: #1f2937;
}

.change-icon,
.clear-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.chat-role-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.chat-role-avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-role-emoji {
  font-size: 1.25rem;
}

.chat-role-name {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.chat-role-status {
  font-size: 0.75rem;
  color: #10b981;
  margin: 0;
}

/* 聊天消息 */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message {
  display: flex;
  gap: 0.75rem;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.ai-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.avatar-emoji {
  font-size: 1.25rem;
}

.user-avatar {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.user-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: white;
}

.message-content {
  max-width: 70%;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.message-user .message-content {
  align-items: flex-end;
}

.message-bubble {
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  background: #f3f4f6;
  color: #1f2937;
}

.message-user .message-bubble {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.message-text {
  margin: 0;
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-word;
}

.message-time {
  font-size: 0.75rem;
  color: #9ca3af;
  padding: 0 0.5rem;
}

/* 打字指示器 */
.typing-bubble {
  padding: 1rem;
}

.typing-indicator {
  display: flex;
  gap: 0.25rem;
}

.typing-indicator span {
  width: 0.5rem;
  height: 0.5rem;
  background: #9ca3af;
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
  }
}

/* 输入框区域 */
.chat-input-area {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.chat-input-form {
  display: flex;
  gap: 0.75rem;
  align-items: flex-end;
}

.chat-textarea {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-family: inherit;
  color: #1f2937;
  resize: none;
  max-height: 120px;
  transition: all 0.2s ease;
}

.chat-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.send-button {
  padding: 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(102, 126, 234, 0.4);
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-icon {
  width: 1.5rem;
  height: 1.5rem;
}

/* 响应式 */
@media (max-width: 768px) {
  .roles-grid {
    grid-template-columns: 1fr;
  }

  .message-content {
    max-width: 85%;
  }

  .chat-section {
    height: calc(100vh - 8rem);
  }
}
</style>
