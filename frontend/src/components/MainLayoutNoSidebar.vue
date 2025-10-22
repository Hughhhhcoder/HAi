<template>
  <div style="min-height: 100vh; background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf3 100%); display: flex; flex-direction: column;">
    <!-- 顶部导航栏 -->
    <HeaderWithNav />
    
    <!-- 主内容区域 -->
    <main style="flex: 1; width: 100%; max-width: 90rem; margin: 0 auto; padding: 2rem 1rem;">
      <slot />
    </main>
    
    <!-- 页脚 -->
    <Footer />
  </div>
</template>

<script setup>
import HeaderWithNav from './HeaderWithNav.vue'
import Footer from './Footer.vue'
</script>

