import Vue from 'vue'
import Router from 'vue-router'
import tokenStore from '../store/token'

const routerOptions = [
  { path: '/', name: 'Home', component: 'Home' },
  { path: '/wishlist/:id', name: 'Wishlist', component: 'Wishlist' },
  { path: '/login', name: 'Login', component: 'Login' },
  { path: '*', component: 'NotFound' }
]
const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  }
})

Vue.use(Router)

const router = new Router({
  routes,
  mode: 'history'
})

const publicPages = ['/login']

router.beforeEach((to, from, next) => {
  // redirect to home page if logged in and trying to access login page
  if (to.path === '/login' && tokenStore.isAuthenticated()) {
    return next('/')
  }
  // redirect to login page if not logged in and trying to access a restricted page
  const authRequired = !publicPages.includes(to.path)
  if (authRequired && !tokenStore.isAuthenticated()) {
    return next('/login')
  }
  return next()
})

export default router
