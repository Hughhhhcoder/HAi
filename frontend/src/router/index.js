import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/Login.vue'
import LoginV2 from '../pages/LoginV2.vue'
import Register from '../pages/Register.vue'
import Home from '../pages/Home.vue'
import HomeV2 from '../pages/HomeV2.vue'
import AiRoles from '../pages/AiRoles.vue'
import PsychChoose from '../pages/PsychChoose.vue'
import PlanProfile from '../pages/PlanProfile.vue'
import CheckinDaily from '../pages/CheckinDaily.vue'
import RewardsPoints from '../pages/RewardsPoints.vue'
import ApiTest from '../pages/ApiTest.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginV2 }, // 使用新的高级登录页面
  { path: '/login-old', component: Login }, // 保留旧版本作为对比
  { path: '/register', component: Register },
  { path: '/home', component: HomeV2 }, // 使用新的Dashboard风格主页
  { path: '/home-old', component: Home }, // 保留旧版本
  { path: '/ai/roles', component: AiRoles },
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