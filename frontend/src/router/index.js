import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Dashboard from '../views/Dashboard.vue'
import Checkin from '../views/Checkin.vue'
import Calendar from '../views/Calendar.vue'
import Stats from '../views/Stats.vue'
import Shop from '../views/Shop.vue'
import Inventory from '../views/Inventory.vue'
import Badges from '../views/Badges.vue'
import Profile from '../views/Profile.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/checkin',
    name: 'Checkin',
    component: Checkin,
    meta: { requiresAuth: true }
  },
  {
    path: '/calendar',
    name: 'Calendar',
    component: Calendar,
    meta: { requiresAuth: true }
  },
  {
    path: '/stats',
    name: 'Stats',
    component: Stats,
    meta: { requiresAuth: true }
  },
  {
    path: '/store',
    name: 'Shop',
    component: Shop,
    meta: { requiresAuth: true }
  },
  {
    path: '/inventory',
    name: 'Inventory',
    component: Inventory,
    meta: { requiresAuth: true }
  },
  {
    path: '/badges',
    name: 'Badges',
    component: Badges,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：检查登录状态
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('user_id')

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
