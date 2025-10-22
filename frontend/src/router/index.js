import { createRouter, createWebHistory } from 'vue-router'
import LoginNew from '../pages/LoginNew.vue'
import LoginFixed from '../pages/LoginFixed.vue'
import Register from '../pages/Register.vue'
import RegisterFixed from '../pages/RegisterFixed.vue'
import HomeNew from '../pages/HomeNew.vue'
import HomeFixed from '../pages/HomeFixed.vue'
import AiRolesNew from '../pages/AiRolesNew.vue'
import AiRolesFixed from '../pages/AiRolesFixed.vue'
import PsychChooseNew from '../pages/PsychChooseNew.vue'
import PsychChooseFixed from '../pages/PsychChooseFixed.vue'
import PlanProfile from '../pages/PlanProfile.vue'
import PlanProfileFixed from '../pages/PlanProfileFixed.vue'
import CheckinDaily from '../pages/CheckinDaily.vue'
import CheckinDailyFixed from '../pages/CheckinDailyFixed.vue'
import RewardsPoints from '../pages/RewardsPoints.vue'
import RewardsPointsFixed from '../pages/RewardsPointsFixed.vue'
import ApiTest from '../pages/ApiTest.vue'
import TestPage from '../pages/TestPage.vue'
import LoginTest from '../pages/LoginTest.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginFixed }, // 修复的登录页面（使用内联样式）
  { path: '/register', component: RegisterFixed }, // 修复的注册页面（使用内联样式）
  { path: '/home', component: HomeFixed }, // 修复的主页（使用内联样式）
  { path: '/ai/roles', component: AiRolesFixed }, // 修复的AI对话页面（使用内联样式）
  { path: '/psych/choose', component: PsychChooseFixed }, // 修复的心理测评页面（使用内联样式）
  { path: '/plan/profile', component: PlanProfileFixed }, // 修复的生活计划页面（使用内联样式）
  { path: '/checkin/daily', component: CheckinDailyFixed }, // 修复的每日打卡页面（使用内联样式）
  { path: '/rewards/points', component: RewardsPointsFixed }, // 修复的积分页面（使用内联样式）
  { path: '/api-test', component: ApiTest },
  { path: '/test', component: TestPage }, // 测试页面
  { path: '/login-test', component: LoginTest }, // 登录测试页面
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