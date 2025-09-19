import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'

const app = createApp(App)
app.use(router)
app.mount('#app')

// ---- 全局暗黑模式检测与切换 ----
const DARK_KEY = 'theme-mode' // 可选值: 'light' | 'dark' | 'system'

function setDarkClass(isDark) {
  document.documentElement.classList.toggle('dark', isDark)
}

function getSystemDark() {
  return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
}

function applyTheme() {
  const mode = localStorage.getItem(DARK_KEY) || 'system'
  if (mode === 'dark') setDarkClass(true)
  else if (mode === 'light') setDarkClass(false)
  else setDarkClass(getSystemDark())
}

// 监听系统主题变化
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
  if ((localStorage.getItem(DARK_KEY) || 'system') === 'system') {
    setDarkClass(getSystemDark())
  }
})

// 初始应用主题
applyTheme()

// 暴露切换方法供全局调用
window.$setThemeMode = (mode) => {
  localStorage.setItem(DARK_KEY, mode)
  applyTheme()
}
window.$getThemeMode = () => localStorage.getItem(DARK_KEY) || 'system'
