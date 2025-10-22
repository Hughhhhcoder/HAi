<template>
  <header style="width: 100%; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(20px); box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); position: sticky; top: 0; z-index: 100;">
    <div style="max-width: 90rem; margin: 0 auto; padding: 0 1rem;">
      <!-- 主导航栏 -->
      <div style="display: flex; align-items: center; justify-content: space-between; height: 4rem;">
        <!-- 左侧：Logo + 品牌 -->
        <router-link to="/home" style="display: flex; align-items: center; gap: 0.75rem; text-decoration: none;">
          <div style="width: 2.5rem; height: 2.5rem; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 0.75rem; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);">
            <svg style="width: 1.5rem; height: 1.5rem; color: white;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
            </svg>
          </div>
          <div>
            <div style="font-weight: 700; color: #1f2937; font-size: 1.25rem; line-height: 1.2;">Hai</div>
            <div style="font-size: 0.75rem; color: #9ca3af;">心理健康平台</div>
          </div>
        </router-link>
        
        <!-- 中间：导航菜单 -->
        <nav class="desktop-nav" style="display: flex; align-items: center; gap: 0.5rem;">
          <router-link 
            v-for="item in menu" 
            :key="item.to"
            :to="item.to"
            :style="getLinkStyle(item.to)"
            @mouseenter="e => handleHover(e, item.to, true)"
            @mouseleave="e => handleHover(e, item.to, false)"
          >
            <span style="font-size: 1.1rem; margin-right: 0.5rem;">{{ item.emoji }}</span>
            <span>{{ item.label }}</span>
          </router-link>
        </nav>
        
        <!-- 移动端：菜单按钮 -->
        <button 
          @click="toggleMobileMenu"
          class="mobile-menu-btn"
          style="display: none; padding: 0.5rem; border-radius: 0.5rem; background: none; border: none; cursor: pointer; transition: background-color 0.2s;"
          @mouseenter="e => e.target.style.background = '#f3f4f6'"
          @mouseleave="e => e.target.style.background = 'none'"
        >
          <svg style="width: 1.5rem; height: 1.5rem; color: #374151;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
          </svg>
        </button>
        
        <!-- 右侧：通知 + 用户 -->
        <div style="display: flex; align-items: center; gap: 1rem;">
          <!-- 通知图标 -->
          <button 
            style="position: relative; padding: 0.5rem; border-radius: 0.5rem; background: none; border: none; cursor: pointer; transition: background-color 0.2s;"
            @mouseenter="e => e.target.style.background = '#f3f4f6'"
            @mouseleave="e => e.target.style.background = 'transparent'"
          >
            <svg style="width: 1.5rem; height: 1.5rem; color: #6b7280;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
            </svg>
            <span style="position: absolute; top: 0.4rem; right: 0.4rem; width: 0.5rem; height: 0.5rem; background: #ef4444; border-radius: 50%; border: 2px solid white;"></span>
          </button>
          
          <!-- 用户头像 -->
          <div style="width: 2.5rem; height: 2.5rem; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 1rem; cursor: pointer; box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3); transition: transform 0.2s;"
            @mouseenter="e => e.target.style.transform = 'scale(1.05)'"
            @mouseleave="e => e.target.style.transform = 'scale(1)'"
          >
            U
          </div>
        </div>
      </div>
      
      <!-- 移动端下拉菜单 -->
      <transition name="slide-down">
        <div v-if="mobileMenuOpen" class="mobile-menu" style="border-top: 1px solid #f3f4f6; padding: 1rem 0;">
          <router-link 
            v-for="item in menu" 
            :key="item.to"
            :to="item.to"
            @click="mobileMenuOpen = false"
            style="display: flex; align-items: center; padding: 0.75rem 1rem; border-radius: 0.5rem; text-decoration: none; color: #374151; transition: all 0.2s; margin: 0.25rem 0;"
            :style="getMobileLinkStyle(item.to)"
          >
            <span style="font-size: 1.2rem; margin-right: 0.75rem; width: 1.5rem; text-align: center;">{{ item.emoji }}</span>
            <span style="font-weight: 500;">{{ item.label }}</span>
          </router-link>
        </div>
      </transition>
    </div>
  </header>
</template>

<script>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

export default {
  name: 'HeaderWithNav',
  setup() {
    const route = useRoute()
    const mobileMenuOpen = ref(false)
    
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
        fontSize: '0.9375rem',
        fontWeight: '500',
        borderRadius: '0.5rem',
        textDecoration: 'none',
        color: active ? '#667eea' : '#4b5563',
        background: active ? 'linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15))' : 'transparent',
        transition: 'all 0.2s',
        cursor: 'pointer',
        border: active ? '1px solid rgba(102, 126, 234, 0.3)' : '1px solid transparent'
      }
    }
    
    const getMobileLinkStyle = (path) => {
      const active = isActive(path)
      return {
        background: active ? 'linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1))' : 'transparent',
        color: active ? '#667eea' : '#374151'
      }
    }
    
    const handleHover = (e, path, isEnter) => {
      if (!isActive(path)) {
        if (isEnter) {
          e.target.style.background = '#f9fafb'
          e.target.style.transform = 'translateY(-1px)'
        } else {
          e.target.style.background = 'transparent'
          e.target.style.transform = 'translateY(0)'
        }
      }
    }
    
    const toggleMobileMenu = () => {
      mobileMenuOpen.value = !mobileMenuOpen.value
    }
    
    return {
      menu,
      mobileMenuOpen,
      isActive,
      getLinkStyle,
      getMobileLinkStyle,
      handleHover,
      toggleMobileMenu
    }
  }
}
</script>

<style scoped>
/* 响应式：桌面端显示导航，移动端显示菜单按钮 */
@media (min-width: 768px) {
  .desktop-nav {
    display: flex !important;
  }
  .mobile-menu-btn {
    display: none !important;
  }
  .mobile-menu {
    display: none !important;
  }
}

@media (max-width: 767px) {
  .desktop-nav {
    display: none !important;
  }
  .mobile-menu-btn {
    display: block !important;
  }
}

/* 下拉动画 */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>

