import { createApp } from 'vue'
import { MotionPlugin } from '@vueuse/motion'
import App from './App.vue'
import router from './router'

// 导入全新的全局样式
import './styles/global.css'

// 创建 Vue 应用
const app = createApp(App)

// 使用插件
app.use(router)
app.use(MotionPlugin) // 高级动画插件

// 全局配置
app.config.productionTip = false
app.config.performance = true

// 挂载应用
app.mount('#app')

// 添加页面加载完成的淡入效果
window.addEventListener('load', () => {
  document.body.classList.add('loaded')
})

// 添加平滑滚动
document.documentElement.style.scrollBehavior = 'smooth'

// 性能监控（开发环境）
if (import.meta.env.DEV) {
  console.log('🚀 Hai 心理健康平台 - 全新前端架构')
  console.log('📦 使用技术栈：')
  console.log('  - Vue 3 + Composition API')
  console.log('  - Tailwind CSS v3 (高级定制)')
  console.log('  - GSAP + VueUse Motion (动画引擎)')
  console.log('  - Particles.js (粒子效果)')
  console.log('  - Chart.js (数据可视化)')
}
