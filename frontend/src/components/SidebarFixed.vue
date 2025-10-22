<template>
  <aside style="height: 100%; width: 16rem; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border-right: 1px solid #f3f4f6; display: none; flex-direction: column;" class="sidebar">
    <!-- Logo区域 -->
    <div style="padding: 1rem; border-bottom: 1px solid #f3f4f6; display: flex; align-items: center; gap: 0.75rem;">
      <div style="width: 2.5rem; height: 2.5rem; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 0.75rem; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);">
        <svg style="width: 1.5rem; height: 1.5rem; color: white;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
        </svg>
      </div>
      <div>
        <div style="font-weight: 700; color: #1f2937; font-size: 1.125rem;">Hai</div>
        <div style="font-size: 0.75rem; color: #9ca3af;">心理健康平台</div>
      </div>
    </div>
    
    <!-- 导航菜单 -->
    <nav style="flex: 1; padding: 0.75rem 0; overflow-y: auto;">
      <router-link 
        v-for="item in menu" 
        :key="item.to" 
        :to="item.to"
        :style="getLinkStyle(item.to)"
        @mouseenter="e => handleHover(e, true)"
        @mouseleave="e => handleHover(e, false)"
      >
        <span :style="getIconStyle(item.to)">{{ item.emoji }}</span>
        <span style="margin-left: 0.75rem;">{{ item.label }}</span>
      </router-link>
    </nav>
    
    <!-- 页脚 -->
    <div style="padding: 1rem; border-top: 1px solid #f3f4f6; font-size: 0.75rem; color: #9ca3af;">
      © 2025 Hai
    </div>
  </aside>
</template>

<script>
import { useRoute } from 'vue-router'
import { computed } from 'vue'

export default {
  name: 'SidebarFixed',
  setup() {
    const route = useRoute()
    
    const menu = [
      { to: '/home', label: '首页', emoji: '🏠' },
      { to: '/ai/roles', label: 'AI 对话', emoji: '🤖' },
      { to: '/psych/choose', label: '心理测评', emoji: '🧠' },
      { to: '/checkin/daily', label: '每日打卡', emoji: '✅' },
      { to: '/plan/profile', label: '生活计划', emoji: '📅' },
      { to: '/rewards/points', label: '积分', emoji: '🏅' },
    ]
    
    const isActive = (path) => {
      return route.path.startsWith(path)
    }
    
    const getLinkStyle = (path) => {
      const active = isActive(path)
      return {
        display: 'flex',
        alignItems: 'center',
        padding: '0.625rem 1rem',
        fontSize: '0.875rem',
        fontWeight: '500',
        borderRadius: '0.5rem',
        margin: '0 0.5rem',
        textDecoration: 'none',
        color: active ? '#667eea' : '#374151',
        background: active ? 'linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1))' : 'transparent',
        transition: 'all 0.2s',
        cursor: 'pointer'
      }
    }
    
    const getIconStyle = (path) => {
      const active = isActive(path)
      return {
        width: '1.1rem',
        textAlign: 'center',
        opacity: active ? '1' : '0.6',
        transition: 'opacity 0.2s'
      }
    }
    
    const handleHover = (e, isEnter) => {
      if (!e.target.classList.contains('router-link-active')) {
        if (isEnter) {
          e.target.style.background = '#f9fafb'
          e.target.style.color = '#667eea'
        } else {
          e.target.style.background = 'transparent'
          e.target.style.color = '#374151'
        }
      }
    }
    
    return {
      menu,
      isActive,
      getLinkStyle,
      getIconStyle,
      handleHover
    }
  }
}
</script>

<style scoped>
/* 桌面端显示侧边栏 */
@media (min-width: 768px) {
  .sidebar {
    display: flex !important;
  }
}

/* 滚动条样式 */
nav::-webkit-scrollbar {
  width: 6px;
}

nav::-webkit-scrollbar-track {
  background: transparent;
}

nav::-webkit-scrollbar-thumb {
  background: #e5e7eb;
  border-radius: 3px;
}

nav::-webkit-scrollbar-thumb:hover {
  background: #d1d5db;
}
</style>

