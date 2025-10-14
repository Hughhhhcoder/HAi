<template>
  <div class="min-h-screen bg-gradient-to-br from-yellow-50 to-amber-100 p-6">
    <div class="max-w-3xl mx-auto">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">积分总览</h1>
        <p class="text-gray-600">查看当前积分与获得记录</p>
      </div>

      <div class="bg-white rounded-2xl shadow-lg p-6 mb-6">
        <div class="flex items-center justify-between">
          <div>
            <div class="text-sm text-gray-500">当前积分</div>
            <div class="text-4xl font-bold text-yellow-600">{{ points }}</div>
          </div>
          <button @click="load" class="px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors">刷新</button>
        </div>
      </div>

      <div class="bg-white rounded-2xl shadow-lg p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold text-gray-800">积分记录</h2>
        </div>
        <div v-if="history.length === 0" class="text-gray-500 text-sm">暂无记录</div>
        <ul class="space-y-3">
          <li v-for="(h, idx) in history" :key="idx" class="p-4 bg-gray-50 rounded-lg text-gray-800 flex items-center justify-between">
            <div>{{ h }}</div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { rewardsApi } from '../api/index.js'

const userId = localStorage.getItem('user_id')
const points = ref(0)
const history = ref([])

async function load() {
  if (!userId) return
  try {
    const p = await rewardsApi.getPoints(userId)
    points.value = p.points || 0
    history.value = await rewardsApi.getHistory(userId)
  } catch (e) {
    // 忽略错误
  }
}

onMounted(load)
</script>