<template>
  <aside class="h-full w-64 bg-white/95 backdrop-blur border-r border-gray-100 hidden md:flex md:flex-col">
    <div class="px-4 py-4 border-b border-gray-100 flex items-center space-x-3">
      <img src="/logo.svg" alt="logo" class="h-7" />
      <span class="font-semibold text-gray-900">Hai</span>
    </div>
    <nav class="flex-1 py-3 overflow-y-auto">
      <RouterLink v-for="item in menu" :key="item.to" :to="item.to" class="group flex items-center px-4 py-2.5 text-sm font-medium rounded-lg mx-2"
        :class="isActive(item.to) ? 'text-indigo-600 bg-indigo-50' : 'text-gray-700 hover:text-indigo-600 hover:bg-gray-50'">
        <span class="i" :class="isActive(item.to) ? 'opacity-100' : 'opacity-60 group-hover:opacity-100'">{{ item.emoji }}</span>
        <span class="ml-3">{{ item.label }}</span>
      </RouterLink>
    </nav>
    <div class="px-4 py-4 border-t border-gray-100 text-xs text-gray-500">© 2025 Hai</div>
  </aside>
</template>

<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()
const menu = [
  { to: '/home', label: '首页', emoji: '🏠' },
  { to: '/ai/roles', label: 'AI 对话', emoji: '🤖' },
  { to: '/psych/choose', label: '心理测评', emoji: '🧠' },
  { to: '/checkin/daily', label: '每日打卡', emoji: '✅' },
  { to: '/plan/profile', label: '生活计划', emoji: '📅' },
  { to: '/rewards/points', label: '积分', emoji: '🏅' },
]
function isActive(path) {
  return route.path.startsWith(path)
}
</script>

<style scoped>
.i { width: 1.1rem; text-align: center; }
</style>


