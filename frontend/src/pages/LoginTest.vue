<template>
  <div style="padding: 2rem; max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif;">
    <h1 style="color: #333; margin-bottom: 2rem;">登录状态测试</h1>
    
    <div style="background: #f5f5f5; padding: 1rem; border-radius: 8px; margin-bottom: 2rem;">
      <h2 style="color: #666; margin-bottom: 1rem;">当前状态：</h2>
      <p><strong>isLoggedIn:</strong> {{ isLoggedIn }}</p>
      <p><strong>user_id:</strong> {{ userId }}</p>
      <p><strong>user:</strong> {{ userInfo }}</p>
    </div>

    <div style="background: #e8f4fd; padding: 1rem; border-radius: 8px; margin-bottom: 2rem;">
      <h2 style="color: #0066cc; margin-bottom: 1rem;">测试登录：</h2>
      <div style="margin-bottom: 1rem;">
        <input v-model="testUsername" placeholder="用户名" style="padding: 0.5rem; margin-right: 0.5rem; border: 1px solid #ccc; border-radius: 4px;">
        <input v-model="testPassword" type="password" placeholder="密码" style="padding: 0.5rem; margin-right: 0.5rem; border: 1px solid #ccc; border-radius: 4px;">
        <button @click="testLogin" :disabled="isLoading" style="padding: 0.5rem 1rem; background: #0066cc; color: white; border: none; border-radius: 4px; cursor: pointer;">
          {{ isLoading ? '登录中...' : '测试登录' }}
        </button>
      </div>
      <div v-if="loginResult" style="background: white; padding: 0.5rem; border-radius: 4px; font-family: monospace; font-size: 0.9rem;">
        {{ loginResult }}
      </div>
    </div>

    <div style="background: #fff3cd; padding: 1rem; border-radius: 8px; margin-bottom: 2rem;">
      <h2 style="color: #856404; margin-bottom: 1rem;">快速操作：</h2>
      <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
        <button @click="setLoggedIn" style="padding: 0.5rem 1rem; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer;">
          设置为已登录
        </button>
        <button @click="clearLogin" style="padding: 0.5rem 1rem; background: #dc3545; color: white; border: none; border-radius: 4px; cursor: pointer;">
          清除登录状态
        </button>
        <button @click="goToPsych" style="padding: 0.5rem 1rem; background: #6f42c1; color: white; border: none; border-radius: 4px; cursor: pointer;">
          测试心理测评页面
        </button>
        <button @click="refresh" style="padding: 0.5rem 1rem; background: #17a2b8; color: white; border: none; border-radius: 4px; cursor: pointer;">
          刷新状态
        </button>
      </div>
    </div>

    <div style="background: #d1ecf1; padding: 1rem; border-radius: 8px;">
      <h2 style="color: #0c5460; margin-bottom: 1rem;">说明：</h2>
      <ul style="color: #0c5460; line-height: 1.6;">
        <li>如果 isLoggedIn 为 null 或 false，说明用户未登录</li>
        <li>点击"设置为已登录"可以模拟登录状态</li>
        <li>点击"测试心理测评页面"可以测试路由守卫</li>
        <li>使用"测试登录"可以真实登录并保存状态</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginTest',
  data() {
    return {
      testUsername: 'testuser',
      testPassword: 'testpass',
      isLoading: false,
      loginResult: ''
    }
  },
  computed: {
    isLoggedIn() {
      return localStorage.getItem('isLoggedIn')
    },
    userId() {
      return localStorage.getItem('user_id')
    },
    userInfo() {
      const user = localStorage.getItem('user')
      return user ? JSON.parse(user) : null
    }
  },
  methods: {
    async testLogin() {
      this.isLoading = true
      this.loginResult = ''
      
      try {
        const response = await fetch('/api/user/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: this.testUsername,
            password: this.testPassword
          })
        })

        const data = await response.json()
        this.loginResult = JSON.stringify(data, null, 2)

        if (response.ok) {
          localStorage.setItem('isLoggedIn', 'true')
          localStorage.setItem('user', JSON.stringify(data))
          localStorage.setItem('user_id', data.user_id)
          this.$forceUpdate() // 强制更新组件
        }
      } catch (error) {
        this.loginResult = '错误: ' + error.message
      } finally {
        this.isLoading = false
      }
    },
    setLoggedIn() {
      localStorage.setItem('isLoggedIn', 'true')
      localStorage.setItem('user_id', '1')
      localStorage.setItem('user', JSON.stringify({ user_id: 1, msg: '登录成功' }))
      this.$forceUpdate()
    },
    clearLogin() {
      localStorage.removeItem('isLoggedIn')
      localStorage.removeItem('user_id')
      localStorage.removeItem('user')
      this.$forceUpdate()
    },
    goToPsych() {
      this.$router.push('/psych/choose')
    },
    refresh() {
      this.$forceUpdate()
    }
  }
}
</script>
