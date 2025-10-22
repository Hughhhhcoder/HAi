<template>
  <div class="home-container">
    <!-- 主内容区 -->
    <main class="main-content">
      <div class="content-container">
        <!-- 欢迎区域 -->
        <section class="welcome-section">
          <div class="welcome-card">
            <h1 class="welcome-title">欢迎回来，{{ username }}！</h1>
            <p class="welcome-subtitle">今天是美好的一天，让我们一起关注心理健康</p>
          </div>
        </section>

        <!-- 数据统计卡片 -->
        <section class="stats-section">
          <div class="stats-grid">
            <!-- 积分卡片 -->
            <div class="stat-card points-card">
              <div class="stat-icon points-icon">
                <svg class="stat-svg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
                </svg>
              </div>
              <div class="stat-content">
                <h3 class="stat-number">{{ userPoints }}</h3>
                <p class="stat-label">总积分</p>
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: '75%' }"></div>
                </div>
              </div>
            </div>

            <!-- 打卡卡片 -->
            <div class="stat-card checkin-card">
              <div class="stat-icon checkin-icon">
                <svg class="stat-svg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"></path>
                </svg>
              </div>
              <div class="stat-content">
                <h3 class="stat-number">{{ checkinStreak }} 天</h3>
                <p class="stat-label">连续打卡</p>
                <div class="flame-icon">🔥</div>
              </div>
            </div>

            <!-- 测评卡片 -->
            <div class="stat-card test-card">
              <div class="stat-icon test-icon">
                <svg class="stat-svg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                </svg>
              </div>
              <div class="stat-content">
                <h3 class="stat-number">3 次</h3>
                <p class="stat-label">心理测评</p>
                <div class="mini-chart"></div>
              </div>
            </div>

            <!-- AI对话卡片 -->
            <div class="stat-card chat-card">
              <div class="stat-icon chat-icon">
                <svg class="stat-svg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                </svg>
              </div>
              <div class="stat-content">
                <h3 class="stat-number">28 次</h3>
                <p class="stat-label">AI对话</p>
                <div class="pulse-dot"></div>
              </div>
            </div>
          </div>
        </section>

        <!-- 今日任务 -->
        <section class="tasks-section">
          <div class="tasks-card">
            <div class="tasks-header">
              <h2 class="tasks-title">今日任务</h2>
              <span class="completion-rate">{{ taskCompletionRate }}% 完成</span>
            </div>

            <div class="tasks-list">
              <!-- 每日打卡任务 -->
              <div class="task-item">
                <div class="task-icon success-icon">
                  <svg class="task-svg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
                <div class="task-content">
                  <h3 class="task-title">每日打卡</h3>
                  <p class="task-description">记录今天的心情和睡眠质量</p>
                </div>
                <div class="task-status completed">
                  <svg class="check-icon" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                  </svg>
                  <span>已完成</span>
                </div>
              </div>

              <!-- 心理测评任务 -->
              <div class="task-item">
                <div class="task-icon primary-icon">
                  <svg class="task-svg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                  </svg>
                </div>
                <div class="task-content">
                  <h3 class="task-title">心理测评</h3>
                  <p class="task-description">完成一次专业心理评估</p>
                </div>
                <div class="task-action">
                  <button class="primary-btn">开始测评</button>
                </div>
              </div>

              <!-- AI咨询任务 -->
              <div class="task-item">
                <div class="task-icon secondary-icon">
                  <svg class="task-svg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                  </svg>
                </div>
                <div class="task-content">
                  <h3 class="task-title">AI心理咨询</h3>
                  <p class="task-description">与专业AI心理师交流</p>
                </div>
                <div class="task-action">
                  <button class="secondary-btn">开始对话</button>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'HomeFixed',
  data() {
    return {
      username: '用户',
      userPoints: 1250,
      checkinStreak: 7,
      taskCompletionRate: 67
    }
  },
  mounted() {
    // 获取用户信息
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      const user = JSON.parse(storedUser)
      this.username = user.username || '用户'
    }
  }
}
</script>

<style scoped>
/* 基础样式 */
.home-container {
  min-height: 100vh;
  background: linear-gradient(to bottom right, #f9fafb, #ffffff, #f3f4f6);
  font-family: 'Inter var', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* 主内容区 */
.main-content {
  padding: 2rem 0;
}

.content-container {
  max-width: 80rem;
  margin: 0 auto;
  padding: 0 1rem;
}

@media (min-width: 640px) {
  .content-container {
    padding: 0 1.5rem;
  }
}

@media (min-width: 1024px) {
  .content-container {
    padding: 0 2rem;
  }
}

/* 欢迎区域 */
.welcome-section {
  margin-bottom: 2rem;
}

.welcome-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1.5rem;
  padding: 2rem;
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}

.welcome-title {
  font-size: 2.25rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.5rem 0;
}

.welcome-subtitle {
  font-size: 1.125rem;
  color: #6b7280;
  margin: 0;
}

/* 统计卡片区域 */
.stats-section {
  margin-bottom: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1.5rem;
  padding: 1.5rem;
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.points-icon {
  background: linear-gradient(to bottom right, #f59e0b, #d97706);
}

.checkin-icon {
  background: linear-gradient(to bottom right, #ef4444, #dc2626);
}

.test-icon {
  background: linear-gradient(to bottom right, #8b5cf6, #7c3aed);
}

.chat-icon {
  background: linear-gradient(to bottom right, #06b6d4, #0891b2);
}

.stat-svg {
  width: 1.5rem;
  height: 1.5rem;
  color: white;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.25rem 0;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0 0 1rem 0;
}

/* 进度条 */
.progress-bar {
  position: relative;
  height: 0.5rem;
  background: #e5e7eb;
  border-radius: 9999px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(to right, #8b5cf6, #7c3aed);
  border-radius: 9999px;
  transition: width 0.5s ease-out;
}

/* 特殊效果 */
.flame-icon {
  font-size: 1.5rem;
  animation: bounce 2s infinite;
}

.pulse-dot {
  width: 0.75rem;
  height: 0.75rem;
  background: #06b6d4;
  border-radius: 50%;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.mini-chart {
  width: 100%;
  height: 0.5rem;
  background: linear-gradient(to right, #8b5cf6, #a78bfa, #c4b5fd);
  border-radius: 0.25rem;
  animation: shimmer 2s linear infinite;
}

/* 任务区域 */
.tasks-section {
  margin-bottom: 2rem;
}

.tasks-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1.5rem;
  padding: 1.5rem;
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}

.tasks-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.tasks-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.completion-rate {
  font-size: 0.875rem;
  color: #6b7280;
}

.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.task-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 0.75rem;
  transition: all 0.3s ease;
}

.task-item:hover {
  background: rgba(255, 255, 255, 0.8);
  transform: scale(1.02);
}

.task-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease;
}

.task-item:hover .task-icon {
  transform: scale(1.1) rotate(6deg);
}

.success-icon {
  background: linear-gradient(to bottom right, #22c55e, #16a34a);
}

.primary-icon {
  background: linear-gradient(to bottom right, #8b5cf6, #7c3aed);
}

.secondary-icon {
  background: linear-gradient(to bottom right, #8b5cf6, #06b6d4, #7c3aed);
}

.task-svg {
  width: 1.5rem;
  height: 1.5rem;
  color: white;
}

.task-content {
  flex: 1;
}

.task-title {
  font-weight: 600;
  color: #111827;
  margin: 0 0 0.25rem 0;
}

.task-description {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
}

.task-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #16a34a;
  font-size: 0.875rem;
  font-weight: 500;
}

.check-icon {
  width: 1rem;
  height: 1rem;
}

.task-action {
  display: flex;
  align-items: center;
}

.primary-btn, .secondary-btn {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 0.875rem;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.primary-btn {
  background: linear-gradient(to right, #8b5cf6, #7c3aed);
  color: white;
}

.primary-btn:hover {
  background: linear-gradient(to right, #7c3aed, #6d28d9);
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.secondary-btn {
  background: linear-gradient(to right, #06b6d4, #0891b2);
  color: white;
}

.secondary-btn:hover {
  background: linear-gradient(to right, #0891b2, #0e7490);
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* 动画 */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

@keyframes shimmer {
  0% {
    background-position: 0% 50%;
  }
  100% {
    background-position: 200% 50%;
  }
}
</style>
