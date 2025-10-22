<template>
  <header style="width: 100%; background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); box-shadow: 0 1px 3px rgba(102, 126, 234, 0.1); position: sticky; top: 0; z-index: 30;">
    <div style="max-width: 80rem; margin: 0 auto; padding: 0.75rem 1rem; display: flex; align-items: center; justify-content: space-between;">
      <!-- 左侧 -->
      <div style="display: flex; align-items: center; gap: 0.75rem;">
        <button 
          @click="$emit('toggle')" 
          aria-label="Open Menu"
          style="display: none; padding: 0.5rem; border-radius: 0.5rem; background: none; border: none; cursor: pointer; transition: background-color 0.2s;"
          class="mobile-menu-btn"
          @mouseenter="e => e.target.style.background = '#f3f4f6'"
          @mouseleave="e => e.target.style.background = 'none'"
        >
          <svg style="width: 1.25rem; height: 1.25rem; color: #374151;" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
        </button>
        <img src="/logo.svg" alt="logo" style="height: 1.75rem;" />
        <span style="font-weight: 600; color: #1f2937; font-size: 1.125rem;">Hai</span>
      </div>
      
      <!-- 右侧 -->
      <div style="display: flex; align-items: center; gap: 0.75rem;">
        <!-- 导航链接（桌面端） -->
        <div class="desktop-nav" style="display: flex; align-items: center; gap: 0.25rem; font-size: 0.875rem; color: #4b5563;">
          <router-link 
            to="/home" 
            style="padding: 0.375rem 0.75rem; border-radius: 0.5rem; text-decoration: none; color: inherit; transition: all 0.2s;"
            @mouseenter="e => e.target.style.background = '#f3f4f6'"
            @mouseleave="e => e.target.style.background = 'transparent'"
          >首页</router-link>
          <router-link 
            to="/ai/roles" 
            style="padding: 0.375rem 0.75rem; border-radius: 0.5rem; text-decoration: none; color: inherit; transition: all 0.2s;"
            @mouseenter="e => e.target.style.background = '#f3f4f6'"
            @mouseleave="e => e.target.style.background = 'transparent'"
          >AI</router-link>
          <router-link 
            to="/psych/choose" 
            style="padding: 0.375rem 0.75rem; border-radius: 0.5rem; text-decoration: none; color: inherit; transition: all 0.2s;"
            @mouseenter="e => e.target.style.background = '#f3f4f6'"
            @mouseleave="e => e.target.style.background = 'transparent'"
          >测评</router-link>
        </div>
        
        <!-- 通知图标 -->
        <button 
          style="position: relative; padding: 0.5rem; border-radius: 0.5rem; background: none; border: none; cursor: pointer; transition: background-color 0.2s;"
          @mouseenter="e => e.target.style.background = '#f3f4f6'"
          @mouseleave="e => e.target.style.background = 'transparent'"
        >
          <svg style="width: 1.25rem; height: 1.25rem; color: #6b7280;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
          </svg>
          <span style="position: absolute; top: 0.375rem; right: 0.375rem; width: 0.5rem; height: 0.5rem; background: #ef4444; border-radius: 50%; border: 2px solid white;"></span>
        </button>
        
        <!-- 用户头像 -->
        <div style="width: 2rem; height: 2rem; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 0.875rem; cursor: pointer; box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);">
          U
        </div>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'HeaderFixed'
}
</script>

<style scoped>
/* 响应式：移动端显示菜单按钮 */
@media (max-width: 768px) {
  .mobile-menu-btn {
    display: block !important;
  }
  .desktop-nav {
    display: none !important;
  }
}
</style>

