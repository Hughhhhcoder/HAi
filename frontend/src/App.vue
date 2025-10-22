<template>
  <div>
    <!-- 登录/注册页面不需要布局 -->
    <MainLayoutNoSidebar v-if="!isAuthPage">
      <router-view />
    </MainLayoutNoSidebar>
    
    <!-- 登录/注册页面直接渲染 -->
    <router-view v-else />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import MainLayoutNoSidebar from './components/MainLayoutNoSidebar.vue'

const route = useRoute()

// 判断是否是认证页面（登录/注册）
const isAuthPage = computed(() => {
  return route.path === '/login' || route.path === '/register'
})
</script>