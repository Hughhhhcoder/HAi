import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/Login.vue'
import Register from '../pages/Register.vue'
import Home from '../pages/Home.vue'
import AiRoles from '../pages/AiRoles.vue'
import PsychChoose from '../pages/PsychChoose.vue'
import PlanProfile from '../pages/PlanProfile.vue'
import CheckinDaily from '../pages/CheckinDaily.vue'
import RewardsPoints from '../pages/RewardsPoints.vue'
import ApiTest from '../pages/ApiTest.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/home', component: Home },
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