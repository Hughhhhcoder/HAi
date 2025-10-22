<template>
  <div style="min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2rem 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); position: relative; overflow: hidden; font-family: 'Inter var', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
    <!-- 背景装饰 -->
    <div style="position: absolute; top: -50%; right: -50%; width: 100%; height: 100%; background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%); animation: float 20s ease-in-out infinite;"></div>
    
    <!-- 登录表单卡片 -->
    <div style="width: 100%; max-width: 28rem; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(20px); border-radius: 1.5rem; padding: 2.5rem; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); position: relative; z-index: 10; animation: slideUp 0.6s ease-out;">
      <!-- Logo -->
      <div style="text-align: center; margin-bottom: 2rem;">
        <div style="width: 4rem; height: 4rem; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 1rem; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; box-shadow: 0 10px 25px -5px rgba(102, 126, 234, 0.4);">
          <svg style="width: 2rem; height: 2rem; color: white;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
          </svg>
        </div>
        <h1 style="font-size: 2rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">欢迎回来</h1>
        <p style="color: #6b7280; font-size: 1rem;">登录 Hai 心理健康平台</p>
      </div>

      <!-- 登录表单 -->
      <form @submit.prevent="handleLogin" style="space-y: 1.5rem;">
        <!-- 用户名输入 -->
        <div style="margin-bottom: 1.5rem;">
          <label style="display: block; font-size: 0.875rem; font-weight: 600; color: #374151; margin-bottom: 0.5rem;">用户名</label>
          <div style="position: relative;">
            <svg style="position: absolute; left: 1rem; top: 50%; transform: translateY(-50%); width: 1.25rem; height: 1.25rem; color: #9ca3af;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
            <input
              v-model="form.username"
              type="text"
              placeholder="请输入用户名"
              style="width: 100%; padding: 0.875rem 1rem 0.875rem 3rem; border: 2px solid #e5e7eb; border-radius: 0.75rem; font-size: 1rem; transition: all 0.2s; background: #f9fafb;"
              @focus="e => { e.target.style.borderColor = '#667eea'; e.target.style.background = 'white'; e.target.style.boxShadow = '0 0 0 3px rgba(102, 126, 234, 0.1)'; }"
              @blur="e => { e.target.style.borderColor = '#e5e7eb'; e.target.style.background = '#f9fafb'; e.target.style.boxShadow = 'none'; }"
              required
            />
          </div>
        </div>

        <!-- 密码输入 -->
        <div style="margin-bottom: 1.5rem;">
          <label style="display: block; font-size: 0.875rem; font-weight: 600; color: #374151; margin-bottom: 0.5rem;">密码</label>
          <div style="position: relative;">
            <svg style="position: absolute; left: 1rem; top: 50%; transform: translateY(-50%); width: 1.25rem; height: 1.25rem; color: #9ca3af;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
            </svg>
            <input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="请输入密码"
              style="width: 100%; padding: 0.875rem 3rem 0.875rem 3rem; border: 2px solid #e5e7eb; border-radius: 0.75rem; font-size: 1rem; transition: all 0.2s; background: #f9fafb;"
              @focus="e => { e.target.style.borderColor = '#667eea'; e.target.style.background = 'white'; e.target.style.boxShadow = '0 0 0 3px rgba(102, 126, 234, 0.1)'; }"
              @blur="e => { e.target.style.borderColor = '#e5e7eb'; e.target.style.background = '#f9fafb'; e.target.style.boxShadow = 'none'; }"
              required
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              style="position: absolute; right: 1rem; top: 50%; transform: translateY(-50%); background: none; border: none; color: #9ca3af; cursor: pointer; padding: 0.25rem;"
            >
              <svg v-if="!showPassword" style="width: 1.25rem; height: 1.25rem;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
              </svg>
              <svg v-else style="width: 1.25rem; height: 1.25rem;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"></path>
              </svg>
            </button>
          </div>
        </div>

        <!-- 记住我和忘记密码 -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
          <label style="display: flex; align-items: center; cursor: pointer;">
            <input
              v-model="rememberMe"
              type="checkbox"
              style="margin-right: 0.5rem; width: 1rem; height: 1rem; accent-color: #667eea;"
            />
            <span style="font-size: 0.875rem; color: #6b7280;">记住我</span>
          </label>
          <a href="#" style="font-size: 0.875rem; color: #667eea; text-decoration: none; hover:underline;">忘记密码？</a>
        </div>

        <!-- 错误消息 -->
        <div v-if="errorMessage" style="background: #fef2f2; border: 1px solid #fecaca; color: #991b1b; padding: 0.75rem; border-radius: 0.5rem; margin-bottom: 1rem; font-size: 0.875rem;">
          {{ errorMessage }}
        </div>

        <!-- 登录按钮 -->
        <button
          type="submit"
          :disabled="isLoading"
          style="width: 100%; padding: 0.875rem 1rem; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; border-radius: 0.75rem; font-size: 1rem; font-weight: 600; cursor: pointer; transition: all 0.2s; position: relative; overflow: hidden;"
          :style="{ opacity: isLoading ? 0.7 : 1, cursor: isLoading ? 'not-allowed' : 'pointer' }"
          @mouseenter="e => { if (!isLoading) e.target.style.transform = 'translateY(-1px)'; e.target.style.boxShadow = '0 10px 25px -5px rgba(102, 126, 234, 0.4)'; }"
          @mouseleave="e => { if (!isLoading) e.target.style.transform = 'translateY(0)'; e.target.style.boxShadow = 'none'; }"
        >
          <span v-if="!isLoading">登录</span>
          <span v-else style="display: flex; align-items: center; justify-content: center;">
            <svg style="width: 1rem; height: 1rem; margin-right: 0.5rem; animation: spin 1s linear infinite;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
            </svg>
            登录中...
          </span>
        </button>

        <!-- 社交登录 -->
        <div style="margin-top: 1.5rem;">
          <div style="text-align: center; margin-bottom: 1rem;">
            <span style="font-size: 0.875rem; color: #9ca3af;">或使用以下方式登录</span>
          </div>
          <div style="display: flex; gap: 0.75rem;">
            <button type="button" style="flex: 1; padding: 0.75rem; background: #24292e; color: white; border: none; border-radius: 0.5rem; font-size: 0.875rem; font-weight: 600; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; justify-content: center;"
              @mouseenter="e => e.target.style.background = '#1a1e22'"
              @mouseleave="e => e.target.style.background = '#24292e'">
              <svg style="width: 1rem; height: 1rem; margin-right: 0.5rem;" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
              GitHub
            </button>
            <button type="button" style="flex: 1; padding: 0.75rem; background: #1da1f2; color: white; border: none; border-radius: 0.5rem; font-size: 0.875rem; font-weight: 600; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; justify-content: center;"
              @mouseenter="e => e.target.style.background = '#0d8bd9'"
              @mouseleave="e => e.target.style.background = '#1da1f2'">
              <svg style="width: 1rem; height: 1rem; margin-right: 0.5rem;" fill="currentColor" viewBox="0 0 24 24">
                <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
              </svg>
              Twitter
            </button>
          </div>
        </div>

        <!-- 注册链接 -->
        <div style="text-align: center; margin-top: 1.5rem;">
          <span style="font-size: 0.875rem; color: #6b7280;">还没有账户？</span>
          <router-link to="/register" style="margin-left: 0.5rem; font-size: 0.875rem; color: #667eea; text-decoration: none; font-weight: 600;"
            @mouseenter="e => e.target.style.textDecoration = 'underline'"
            @mouseleave="e => e.target.style.textDecoration = 'none'">立即注册</router-link>
        </div>
      </form>
    </div>

    <!-- 页脚 -->
    <div style="position: absolute; bottom: 1rem; left: 50%; transform: translateX(-50%); color: rgba(255, 255, 255, 0.8); font-size: 0.75rem;">
      <p>&copy; 2025 Your Company · <a href="#" style="color: rgba(255, 255, 255, 0.8); text-decoration: none;">隐私政策</a> · <a href="#" style="color: rgba(255, 255, 255, 0.8); text-decoration: none;">使用条款</a></p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginFixed',
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      rememberMe: false,
      showPassword: false,
      isLoading: false,
      errorMessage: ''
    }
  },
  methods: {
    async handleLogin() {
      this.isLoading = true
      this.errorMessage = ''

      try {
        const response = await fetch('http://localhost:8000/api/user/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.form)
        })

        const data = await response.json()

        if (response.ok) {
          // 存储登录信息
          localStorage.setItem('isLoggedIn', 'true')
          localStorage.setItem('user', JSON.stringify(data))
          localStorage.setItem('user_id', data.user_id)
          
          // 跳转到主页
          this.$router.push('/home')
        } else {
          this.errorMessage = data.detail || '登录失败，请检查用户名和密码'
        }
      } catch (error) {
        console.error('登录错误:', error)
        this.errorMessage = '网络错误，请稍后重试'
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>

<style>
@keyframes float {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg);
  }
  33% {
    transform: translate(30px, -50px) rotate(120deg);
  }
  66% {
    transform: translate(-20px, 20px) rotate(240deg);
  }
}

@keyframes slideUp {
  0% {
    opacity: 0;
    transform: translateY(30px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>