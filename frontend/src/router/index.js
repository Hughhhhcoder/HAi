import { createRouter, createWebHistory } from 'vue-router'
import LoginNew from '../pages/LoginNew.vue'
import Register from '../pages/Register.vue'
import HomeNew from '../pages/HomeNew.vue'
import AiRolesNew from '../pages/AiRolesNew.vue'
import PsychChoose from '../pages/PsychChoose.vue'
import PlanProfile from '../pages/PlanProfile.vue'
import CheckinDaily from '../pages/CheckinDaily.vue'
import RewardsPoints from '../pages/RewardsPoints.vue'
import ApiTest from '../pages/ApiTest.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginNew }, // 全新的高级登录页面（3D效果+流体背景）
  { path: '/register', component: Register },
  { path: '/home', component: HomeNew }, // 全新的Dashboard主页（数据可视化+微交互）
  { path: '/ai/roles', component: AiRolesNew }, // 全新的AI对话页面（现代聊天UI+打字效果）
  { path: '/psych/choose', component: PsychChoose },
  { path: '/plan/profile', component: PlanProfile },
  { path: '/checkin/daily', component: CheckinDaily },
  { path: '/rewards/points', component: RewardsPoints },
  { path: '/api-test', component: ApiTest },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 简单登录守卫：未登录跳转到 /login
const publicPaths = ['/login', '/register']
router.beforeEach((to, from, next) => {
  const isPublic = publicPaths.includes(to.path)
  const loggedIn = localStorage.getItem('isLoggedIn') === 'true'
  if (!isPublic && !loggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router 