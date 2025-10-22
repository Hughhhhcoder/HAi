<template>
  <div class="register-container">
    <!-- 背景装饰 -->
    <div class="bg-decoration"></div>
    
    <!-- 注册表单卡片 -->
    <div class="register-card">
      <!-- Logo -->
      <div class="logo-section">
        <div class="logo-icon">
          <svg class="heart-svg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
          </svg>
        </div>
        <h1 class="app-title">创建账户</h1>
        <p class="app-subtitle">加入 Hai 心理健康平台</p>
      </div>

      <!-- 注册表单 -->
      <form @submit.prevent="handleRegister" class="register-form">
        <!-- 用户名 -->
        <div class="form-group">
          <label class="form-label">用户名</label>
          <div class="input-wrapper">
            <svg class="input-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
            <input v-model="form.username" type="text" placeholder="请输入用户名" class="form-input" required />
          </div>
        </div>

        <!-- 邮箱 -->
        <div class="form-group">
          <label class="form-label">邮箱</label>
          <div class="input-wrapper">
            <svg class="input-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
            </svg>
            <input v-model="form.email" type="email" placeholder="请输入邮箱" class="form-input" required />
          </div>
        </div>

        <!-- 密码 -->
        <div class="form-group">
          <label class="form-label">密码</label>
          <div class="input-wrapper">
            <svg class="input-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
            </svg>
            <input v-model="form.password" :type="showPassword ? 'text' : 'password'" placeholder="请输入密码" class="form-input" required />
            <button type="button" @click="showPassword = !showPassword" class="password-toggle">
              <svg v-if="!showPassword" class="eye-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
              </svg>
              <svg v-else class="eye-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"></path>
              </svg>
            </button>
          </div>
        </div>

        <!-- 确认密码 -->
        <div class="form-group">
          <label class="form-label">确认密码</label>
          <div class="input-wrapper">
            <svg class="input-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <input v-model="form.confirmPassword" :type="showConfirmPassword ? 'text' : 'password'" placeholder="请再次输入密码" class="form-input" required />
            <button type="button" @click="showConfirmPassword = !showConfirmPassword" class="password-toggle">
              <svg v-if="!showConfirmPassword" class="eye-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
              </svg>
              <svg v-else class="eye-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"></path>
              </svg>
            </button>
          </div>
        </div>

        <!-- 错误提示 -->
        <div v-if="errorMessage" class="error-message">
          <svg class="error-icon" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
          </svg>
          {{ errorMessage }}
        </div>

        <!-- 注册按钮 -->
        <button type="submit" class="register-button" :disabled="isLoading">
          <span v-if="!isLoading">注册</span>
          <span v-else class="loading-spinner">
            <svg class="spinner" viewBox="0 0 24 24">
              <circle class="spinner-circle" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
            </svg>
            注册中...
          </span>
        </button>

        <!-- 登录链接 -->
        <div class="login-section">
          <span class="login-text">已有账户？</span>
          <router-link to="/login" class="login-link">立即登录</router-link>
        </div>
      </form>
    </div>

    <!-- 页脚 -->
    <div class="footer">
      <p>&copy; 2025 Your Company · <a href="#">隐私政策</a> · <a href="#">使用条款</a></p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RegisterFixed',
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      },
      showPassword: false,
      showConfirmPassword: false,
      isLoading: false,
      errorMessage: ''
    }
  },
  methods: {
    async handleRegister() {
      this.errorMessage = ''

      // 验证密码
      if (this.form.password !== this.form.confirmPassword) {
        this.errorMessage = '两次输入的密码不一致'
        return
      }

      if (this.form.password.length < 6) {
        this.errorMessage = '密码长度至少6个字符'
        return
      }

      this.isLoading = true

      try {
        const response = await fetch('http://localhost:8000/api/user/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: this.form.username,
            email: this.form.email,
            password: this.form.password
          })
        })

        const data = await response.json()

        if (response.ok) {
          alert('注册成功！请登录')
          this.$router.push('/login')
        } else {
          this.errorMessage = data.detail || '注册失败，请重试'
        }
      } catch (error) {
        console.error('注册错误:', error)
        this.errorMessage = '网络错误，请稍后重试'
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>

<style scoped>
/* 复用登录页面的样式 */
.register-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
  font-family: 'Inter var', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.bg-decoration {
  position: absolute;
  top: -50%;
  right: -50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  animation: float 20s ease-in-out infinite;
}

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

.register-card {
  width: 100%;
  max-width: 28rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 1.5rem;
  padding: 2.5rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  position: relative;
  z-index: 10;
  animation: slideUp 0.6s ease-out;
  max-height: 90vh;
  overflow-y: auto;
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

.logo-section {
  text-align: center;
  margin-bottom: 2rem;
}

.logo-icon {
  width: 4rem;
  height: 4rem;
  margin: 0 auto 1rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.5);
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.heart-svg {
  width: 2rem;
  height: 2rem;
  color: white;
}

.app-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
}

.app-subtitle {
  font-size: 1rem;
  color: #6b7280;
  margin: 0;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1rem;
  width: 1.25rem;
  height: 1.25rem;
  color: #9ca3af;
  pointer-events: none;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  font-size: 1rem;
  color: #1f2937;
  background: white;
  transition: all 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input::placeholder {
  color: #9ca3af;
}

.password-toggle {
  position: absolute;
  right: 1rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  color: #6b7280;
  transition: color 0.2s ease;
}

.password-toggle:hover {
  color: #374151;
}

.eye-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 0.5rem;
  color: #dc2626;
  font-size: 0.875rem;
}

.error-icon {
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
}

.register-button {
  width: 100%;
  padding: 0.875rem 1.5rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 14px rgba(102, 126, 234, 0.4);
}

.register-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.register-button:active:not(:disabled) {
  transform: translateY(0);
}

.register-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.spinner {
  width: 1rem;
  height: 1rem;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.spinner-circle {
  stroke-dasharray: 60;
  stroke-dashoffset: 45;
}

.login-section {
  text-align: center;
  font-size: 0.875rem;
}

.login-text {
  color: #6b7280;
}

.login-link {
  color: #667eea;
  font-weight: 600;
  text-decoration: none;
  margin-left: 0.25rem;
  transition: color 0.2s ease;
}

.login-link:hover {
  color: #764ba2;
}

.footer {
  margin-top: 2rem;
  text-align: center;
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.8);
  position: relative;
  z-index: 10;
}

.footer a {
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer a:hover {
  color: white;
}

/* 响应式 */
@media (max-width: 640px) {
  .register-card {
    padding: 2rem 1.5rem;
  }
}
</style>
