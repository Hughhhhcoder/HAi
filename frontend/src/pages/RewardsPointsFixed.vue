<template>
  <div style="min-height: calc(100vh - 4rem); background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 2rem 1rem;">
    <div style="max-width: 48rem; margin: 0 auto;">
      <!-- 标题 -->
      <div style="text-center; margin-bottom: 2rem;">
        <h1 style="font-size: 2rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">积分总览</h1>
        <p style="color: #6b7280;">查看当前积分与获得记录</p>
      </div>

      <!-- 积分卡片 -->
      <div style="background: white; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); padding: 2rem; margin-bottom: 1.5rem;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
          <div>
            <div style="font-size: 0.875rem; color: #9ca3af; margin-bottom: 0.5rem;">当前积分</div>
            <div style="font-size: 2.5rem; font-weight: 700; color: #d97706;">{{ points }}</div>
          </div>
          <button 
            @click="load" 
            style="padding: 0.75rem 1.5rem; background: #d97706; color: white; border-radius: 0.75rem; border: none; font-weight: 600; cursor: pointer; transition: all 0.2s;"
            @mouseenter="e => e.target.style.background = '#b45309'"
            @mouseleave="e => e.target.style.background = '#d97706'"
          >
            刷新
          </button>
        </div>
      </div>

      <!-- 积分记录 -->
      <div style="background: white; border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); padding: 2rem;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem;">
          <h2 style="font-size: 1.25rem; font-weight: 600; color: #1f2937;">积分记录</h2>
          <span style="font-size: 0.875rem; color: #9ca3af;">共 {{ history.length }} 条</span>
        </div>
        
        <div v-if="history.length === 0" style="padding: 3rem; text-align: center;">
          <svg style="width: 4rem; height: 4rem; color: #d1d5db; margin: 0 auto 1rem;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path>
          </svg>
          <p style="color: #9ca3af; font-size: 0.875rem;">暂无积分记录</p>
        </div>
        
        <ul v-else style="display: flex; flex-direction: column; gap: 0.75rem;">
          <li 
            v-for="(h, idx) in history" 
            :key="idx" 
            style="padding: 1rem; background: #fef3c7; border-radius: 0.75rem; color: #1f2937; display: flex; align-items: center; justify-content: space-between; border: 1px solid #fde68a;"
          >
            <div style="display: flex; align-items: center; gap: 0.75rem;">
              <div style="width: 2.5rem; height: 2.5rem; background: linear-gradient(135deg, #fbbf24, #f59e0b); border-radius: 0.5rem; display: flex; align-items: center; justify-content: center; font-size: 1.25rem;">
                🏅
              </div>
              <div>{{ h }}</div>
            </div>
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
    console.error('加载积分失败:', e)
  }
}

onMounted(() => {
  load()
})
</script>

