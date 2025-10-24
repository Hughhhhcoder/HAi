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
          <div class="chat-actions">
            <button @click="clearChat" class="clear-chat-btn">
              <svg class="clear-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
              </svg>
            </button>
          </div>
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
                <div class="message-text" v-html="renderMarkdown(message.content)"></div>
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

    <!-- 历史咨询回顾弹窗 -->
    <div v-if="showConsultationModal" class="consultation-modal" @click="closeConsultationModal">
      <div class="consultation-modal-content" @click.stop>
        <div class="consultation-header">
          <h3 class="consultation-title">📋 历史咨询回顾</h3>
          <button @click="closeConsultationModal" class="close-btn">
            <svg class="close-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <div class="consultation-stats">
          <div class="stat-item">
            <span class="stat-label">咨询师数量</span>
            <span class="stat-value">{{ consultationStats.totalConsultants }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">总咨询次数</span>
            <span class="stat-value">{{ consultationStats.totalConsultations }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">最近咨询</span>
            <span class="stat-value">{{ consultationStats.lastConsultationTime }}</span>
          </div>
        </div>

        <div class="consultation-list">
          <div 
            v-for="(consultation, index) in consultationReviews" 
            :key="index"
            class="consultation-item"
          >
            <div class="consultation-item-header">
              <div class="consultation-role">
                <div class="role-avatar" :style="{ background: consultation.role.gradient }">
                  <span class="role-emoji">{{ consultation.role.emoji }}</span>
                </div>
                <div class="role-info">
                  <h4 class="role-name">{{ consultation.role.name }}</h4>
                  <p class="role-description">{{ consultation.role.description }}</p>
                </div>
              </div>
              <span class="consultation-time">{{ formatTimestamp(consultation.lastMessageTime) }}</span>
            </div>
            <div class="consultation-summary">
              <h5 class="summary-title">咨询摘要：</h5>
              <p class="summary-content">{{ consultation.summary }}</p>
            </div>
            <div class="consultation-details">
              <div class="detail-item">
                <span class="detail-label">对话次数：</span>
                <span class="detail-value">{{ consultation.messageCount }} 次</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">主要话题：</span>
                <span class="detail-value">{{ consultation.topics.join('、') }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 历史记录弹窗 -->
    <div v-if="showHistoryModal" class="history-modal" @click="closeHistoryModal">
      <div class="history-modal-content" @click.stop>
        <div class="history-header">
          <h3 class="history-title">对话历史记录</h3>
          <button @click="closeHistoryModal" class="close-btn">
            <svg class="close-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <div class="history-stats">
          <div class="stat-item">
            <span class="stat-label">总对话数</span>
            <span class="stat-value">{{ historyStats.totalMessages }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">最近对话</span>
            <span class="stat-value">{{ historyStats.lastMessageTime }}</span>
          </div>
        </div>

        <div class="history-list">
          <div 
            v-for="(record, index) in historyRecords" 
            :key="index"
            class="history-item"
          >
            <div class="history-item-header">
              <span class="history-time">{{ formatTimestamp(record.timestamp) }}</span>
              <span class="history-type">{{ record.is_user ? '您' : selectedRole.name }}</span>
            </div>
            <div class="history-content">
              <p class="history-message">{{ record.message.substring(0, 100) }}{{ record.message.length > 100 ? '...' : '' }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked'

export default {
  name: 'AiRolesFixed',
  data() {
    return {
      selectedRole: null,
      messages: [],
      currentMessage: '',
      isAiTyping: false,
      aiRoles: [],
      showHistoryModal: false,
      historyRecords: [],
      historyStats: {
        totalMessages: 0,
        lastMessageTime: '暂无'
      },
      showConsultationModal: false,
      consultationReviews: [],
      consultationStats: {
        totalConsultants: 0,
        totalConsultations: 0,
        lastConsultationTime: '暂无'
      }
    }
  },
  methods: {
    goBack() {
      this.$router.push('/home')
    },
    async fetchRoles() {
      try {
        const res = await fetch('/api/ai/roles')
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
    renderMarkdown(text) {
      if (!text) return ''
      try {
        // 配置marked选项 - 优化换行处理
        marked.setOptions({
          breaks: false,  // 关闭自动换行，减少不必要的<br>标签
          gfm: true,
          pedantic: false,
          sanitize: false,
          smartLists: true,
          smartypants: false
        })
        
        // 预处理文本，移除多余的空行
        const cleanedText = text
          .replace(/\n\s*\n\s*\n/g, '\n\n')  // 将多个连续空行合并为两个
          .replace(/\n{3,}/g, '\n\n')       // 限制最多两个连续换行
          .trim()
        
        return marked(cleanedText)
      } catch (error) {
        console.error('Markdown渲染错误:', error)
        return text.replace(/\n/g, '<br>')
      }
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
        
        const response = await fetch(`/api/ai/chat`, {
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
    async showHistory() {
      if (!this.selectedRole) return
      
      try {
        const userId = JSON.parse(localStorage.getItem('user')).id
        const response = await fetch(`/api/ai/full-history?user_id=${userId}&role_id=${this.selectedRole.id}`)
        if (!response.ok) throw new Error('Failed to load history')
        
        const data = await response.json()
        this.historyRecords = data.conversations || []
        this.historyStats = {
          totalMessages: data.total_messages || 0,
          lastMessageTime: this.historyRecords.length > 0 ? 
            this.formatTimestamp(this.historyRecords[0].timestamp) : '暂无'
        }
        this.showHistoryModal = true
      } catch (error) {
        console.error('Error loading history:', error)
        alert('加载历史记录失败')
      }
    },
    closeHistoryModal() {
      this.showHistoryModal = false
    },
    async showConsultationReview() {
      if (!this.aiRoles.length) {
        await this.fetchRoles()
      }
      
      try {
        const userStr = localStorage.getItem('user')
        if (!userStr) {
          console.log('No user found in localStorage')
          alert('用户未登录，请先登录')
          return
        }
        const user = JSON.parse(userStr)
        const userId = user.id || user.user_id || 1
        console.log('Loading consultation review for user:', userId)
        const consultationData = []
        let latestConsultation = null
        let latestTime = null
        
        // 获取所有AI角色的对话历史
        for (const role of this.aiRoles) {
          try {
            const response = await fetch(`/api/ai/full-history?user_id=${userId}&role_id=${role.id}`)
            if (response.ok) {
              const data = await response.json()
              if (data.conversations && data.conversations.length > 0) {
                // 分析对话内容，生成摘要
                const summary = this.generateConsultationSummary(data.conversations)
                const topics = this.extractTopics(data.conversations)
                
                const consultation = {
                  role: role,
                  messageCount: data.conversations.length,
                  lastMessageTime: data.conversations[0].timestamp,
                  summary: summary,
                  topics: topics
                }
                
                consultationData.push(consultation)
                
                // 找到最新的咨询记录
                if (!latestTime || new Date(data.conversations[0].timestamp) > new Date(latestTime)) {
                  latestTime = data.conversations[0].timestamp
                  latestConsultation = {
                    role_name: role.name,
                    last_message_time: data.conversations[0].timestamp,
                    summary: summary
                  }
                }
              }
            }
          } catch (error) {
            console.error(`获取角色 ${role.name} 的历史记录失败:`, error)
          }
        }
        
        // 按最后对话时间排序
        consultationData.sort((a, b) => new Date(b.lastMessageTime) - new Date(a.lastMessageTime))
        
        // 更新最后一次咨询信息
        this.lastConsultation = latestConsultation
        
        this.consultationReviews = consultationData
        this.consultationStats = {
          totalConsultants: consultationData.length,
          totalConsultations: consultationData.reduce((sum, item) => sum + item.messageCount, 0),
          lastConsultationTime: consultationData.length > 0 ? 
            this.formatTimestamp(consultationData[0].lastMessageTime) : '暂无'
        }
        this.showConsultationModal = true
      } catch (error) {
        console.error('Error loading consultation review:', error)
        alert('加载历史咨询回顾失败')
      }
    },
    closeConsultationModal() {
      this.showConsultationModal = false
    },
    formatTimestamp(timestamp) {
      if (!timestamp) return '暂无'
      
      try {
        const now = new Date()
        const date = new Date(timestamp)
        
        // 检查日期是否有效
        if (isNaN(date.getTime())) {
          return '时间格式错误'
        }
        
        // 获取用户时区
        const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone
        
        // 计算时间差（毫秒）
        const diff = now - date
        const diffDays = Math.floor(diff / (1000 * 60 * 60 * 24))
        
        // 如果是今天
        if (diffDays === 0) {
          return `今天 ${date.toLocaleTimeString('zh-CN', { 
            hour: '2-digit', 
            minute: '2-digit',
            timeZone: userTimezone
          })}`
        }
        
        // 如果是昨天
        if (diffDays === 1) {
          return `昨天 ${date.toLocaleTimeString('zh-CN', { 
            hour: '2-digit', 
            minute: '2-digit',
            timeZone: userTimezone
          })}`
        }
        
        // 如果是本周内（2-6天前）
        if (diffDays >= 2 && diffDays <= 6) {
          return `${diffDays}天前 ${date.toLocaleTimeString('zh-CN', { 
            hour: '2-digit', 
            minute: '2-digit',
            timeZone: userTimezone
          })}`
        }
        
        // 如果是本周内（显示星期几）
        if (diffDays >= 1 && diffDays <= 7) {
          const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
          const weekday = weekdays[date.getDay()]
          return `${weekday} ${date.toLocaleTimeString('zh-CN', { 
            hour: '2-digit', 
            minute: '2-digit',
            timeZone: userTimezone
          })}`
        }
        
        // 其他情况显示完整日期时间（用户时区）
        return date.toLocaleString('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          timeZone: userTimezone
        })
      } catch (error) {
        console.error('时间格式化错误:', error)
        return '时间格式错误'
      }
    },
    async loadLastConsultation() {
      try {
        const userStr = localStorage.getItem('user')
        if (!userStr) {
          console.log('No user found in localStorage')
          return
        }
        const user = JSON.parse(userStr)
        const userId = user.id || user.user_id || 1
        console.log('Loading last consultation for user:', userId)
        let latestConsultation = null
        let latestTime = null
        
        // 获取所有AI角色的对话历史，找到最新的
        for (const role of this.aiRoles) {
          try {
            const response = await fetch(`/api/ai/full-history?user_id=${userId}&role_id=${role.id}`)
            if (response.ok) {
              const data = await response.json()
              if (data.conversations && data.conversations.length > 0) {
                const lastMessageTime = data.conversations[0].timestamp
                
                // 找到最新的咨询记录
                if (!latestTime || new Date(lastMessageTime) > new Date(latestTime)) {
                  latestTime = lastMessageTime
                  const summary = this.generateConsultationSummary(data.conversations)
                  latestConsultation = {
                    role_name: role.name,
                    last_message_time: lastMessageTime,
                    summary: summary
                  }
                }
              }
            }
          } catch (error) {
            console.error(`获取角色 ${role.name} 的历史记录失败:`, error)
          }
        }
        
        this.lastConsultation = latestConsultation
      } catch (error) {
        console.error('Error loading last consultation:', error)
      }
    },
    generateConsultationSummary(conversations) {
      if (conversations.length === 0) return '暂无对话记录'
      
      // 分析对话内容，生成摘要
      const userMessages = conversations.filter(c => c.is_user).map(c => c.message)
      const aiMessages = conversations.filter(c => !c.is_user).map(c => c.message)
      
      // 简单的摘要生成逻辑
      let summary = ''
      if (userMessages.length > 0) {
        const firstUserMessage = userMessages[userMessages.length - 1] // 最新的用户消息
        const lastUserMessage = userMessages[0] // 最旧的用户消息
        
        if (firstUserMessage.length > 50) {
          summary = `您主要咨询了关于"${firstUserMessage.substring(0, 50)}..."的问题`
        } else {
          summary = `您咨询了关于"${firstUserMessage}"的问题`
        }
        
        if (userMessages.length > 1) {
          summary += `，共进行了${userMessages.length}轮对话`
        }
      }
      
      return summary || '咨询内容摘要生成中...'
    },
    extractTopics(conversations) {
      // 简单的关键词提取
      const topics = []
      const userMessages = conversations.filter(c => c.is_user).map(c => c.message)
      
      // 常见心理话题关键词
      const topicKeywords = {
        '情绪管理': ['情绪', '心情', '焦虑', '抑郁', '压力', '愤怒', '悲伤'],
        '人际关系': ['朋友', '家人', '同事', '恋爱', '分手', '社交', '沟通'],
        '工作学习': ['工作', '学习', '考试', '职业', '未来', '目标', '计划'],
        '自我成长': ['自信', '自我', '成长', '改变', '习惯', '性格', '价值观'],
        '生活困扰': ['睡眠', '饮食', '健康', '时间', '金钱', '选择', '决定']
      }
      
      const allText = userMessages.join(' ')
      for (const [topic, keywords] of Object.entries(topicKeywords)) {
        if (keywords.some(keyword => allText.includes(keyword))) {
          topics.push(topic)
        }
      }
      
      return topics.length > 0 ? topics : ['一般咨询']
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
  async created() {
    await this.fetchRoles()
    await this.loadLastConsultation()
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

/* Markdown内容样式 - 优化版 */
:deep(.message-text) {
  color: #1f2937;
  line-height: 1.6;
  font-size: 0.95rem;
}

/* 重置所有元素的默认边距 */
:deep(.message-text *:first-child) {
  margin-top: 0;
}

:deep(.message-text *:last-child) {
  margin-bottom: 0;
}

/* 标题样式 - 减少间距 */
:deep(.message-text h1),
:deep(.message-text h2),
:deep(.message-text h3),
:deep(.message-text h4),
:deep(.message-text h5),
:deep(.message-text h6) {
  color: #1f2937;
  font-weight: 700;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}

:deep(.message-text h1) {
  font-size: 1.25rem;
  color: #8b5cf6;
  border-bottom: 1px solid #8b5cf6;
  padding-bottom: 0.25rem;
}

:deep(.message-text h2) {
  font-size: 1.125rem;
  color: #374151;
  border-left: 3px solid #8b5cf6;
  padding-left: 0.75rem;
  background: #f8fafc;
  padding: 0.5rem 0.75rem;
  border-radius: 0.25rem;
}

:deep(.message-text h3) {
  font-size: 1rem;
  color: #4b5563;
  font-weight: 600;
}

/* 段落样式 - 紧凑布局 */
:deep(.message-text p) {
  margin-bottom: 0.5rem;
  line-height: 1.6;
  text-align: justify;
}

/* 列表样式 - 紧凑布局 */
:deep(.message-text ul),
:deep(.message-text ol) {
  margin-bottom: 0.5rem;
  padding-left: 1.25rem;
}

:deep(.message-text li) {
  margin-bottom: 0.125rem;
  line-height: 1.5;
}

/* 强调文本 */
:deep(.message-text strong) {
  font-weight: 700;
  color: #8b5cf6;
}

:deep(.message-text em) {
  font-style: italic;
  color: #6b7280;
}

/* 代码样式 */
:deep(.message-text code) {
  background: #f3f4f6;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  color: #dc2626;
}

/* 引用块 */
:deep(.message-text blockquote) {
  border-left: 3px solid #8b5cf6;
  padding-left: 0.75rem;
  margin: 0.5rem 0;
  font-style: italic;
  color: #6b7280;
  background: #f8fafc;
  padding: 0.5rem 0.75rem;
  border-radius: 0.25rem;
}

/* 链接样式 */
:deep(.message-text a) {
  color: #8b5cf6;
  text-decoration: underline;
}

:deep(.message-text a:hover) {
  color: #7c3aed;
}

/* 移除多余的换行和间距 */
:deep(.message-text br) {
  display: none;
}

/* 优化段落间距 */
:deep(.message-text p + p) {
  margin-top: 0.25rem;
}

/* 列表项之间的间距 */
:deep(.message-text li + li) {
  margin-top: 0.125rem;
}

/* 历史记录弹窗样式 */
.history-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.history-modal-content {
  background: white;
  border-radius: 1rem;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow: hidden;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.history-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  background: linear-gradient(135deg, #8b5cf6, #3b82f6);
  color: white;
}

.history-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.close-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 0.5rem;
  padding: 0.5rem;
  cursor: pointer;
  transition: background 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.close-icon {
  width: 1.25rem;
  height: 1.25rem;
  color: white;
}

.history-stats {
  display: flex;
  gap: 2rem;
  padding: 1.5rem;
  background: #f8fafc;
  border-bottom: 1px solid #e5e7eb;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
}

.stat-value {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
}

.history-list {
  max-height: 400px;
  overflow-y: auto;
  padding: 1rem;
}

.history-item {
  padding: 1rem;
  border-bottom: 1px solid #f3f4f6;
  transition: background 0.2s;
}

.history-item:hover {
  background: #f8fafc;
}

.history-item:last-child {
  border-bottom: none;
}

.history-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.history-time {
  font-size: 0.75rem;
  color: #9ca3af;
}

.history-type {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 0.375rem;
  background: #e5e7eb;
  color: #374151;
}

.history-content {
  margin-top: 0.5rem;
}

.history-message {
  font-size: 0.875rem;
  color: #374151;
  line-height: 1.5;
  margin: 0;
}

/* 聊天操作按钮样式 */
.chat-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  flex-wrap: wrap;
  margin-top: 0.5rem;
}



/* 移动设备优化 */
@media (max-width: 768px) {
  .chat-actions {
    flex-direction: column;
    gap: 0.75rem;
    width: 100%;
  }
  
}

.clear-chat-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 0.5rem;
  padding: 0.5rem;
  cursor: pointer;
  transition: background 0.2s;
}

.clear-chat-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.clear-icon {
  width: 1.25rem;
  height: 1.25rem;
  color: white;
}

/* 历史咨询回顾弹窗样式 */
.consultation-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.consultation-modal-content {
  background: white;
  border-radius: 1rem;
  width: 90%;
  max-width: 900px;
  max-height: 80vh;
  overflow: hidden;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.consultation-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  background: linear-gradient(135deg, #8b5cf6, #3b82f6);
  color: white;
}

.consultation-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.consultation-stats {
  display: flex;
  gap: 2rem;
  padding: 1.5rem;
  background: #f8fafc;
  border-bottom: 1px solid #e5e7eb;
}

.consultation-list {
  max-height: 500px;
  overflow-y: auto;
  padding: 1rem;
}

.consultation-item {
  padding: 1.5rem;
  border-bottom: 1px solid #f3f4f6;
  transition: background 0.2s;
}

.consultation-item:hover {
  background: #f8fafc;
}

.consultation-item:last-child {
  border-bottom: none;
}

.consultation-item-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.consultation-role {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.role-avatar {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.role-emoji {
  color: white;
}

.role-info {
  flex: 1;
}

.role-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.25rem 0;
}

.role-description {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
  line-height: 1.4;
}

.consultation-time {
  font-size: 0.75rem;
  color: #9ca3af;
  white-space: nowrap;
}

.consultation-summary {
  margin-bottom: 1rem;
}

.summary-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 0.5rem 0;
}

.summary-content {
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.5;
  margin: 0;
}

.consultation-details {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.detail-label {
  font-size: 0.75rem;
  color: #9ca3af;
}

.detail-value {
  font-size: 0.75rem;
  color: #374151;
  font-weight: 500;
}
</style>
