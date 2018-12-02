import Vue from 'vue'
import Router from 'vue-router'
import tokenStore from '../store/token'

const routerOptions = [
  { path: '/', name: 'Home', component: 'Home' },
  { path: '/draft', name: 'Draft', component: 'Draft' },
  { path: '/wishlist/:id', name: 'Wishlist', component: 'Wishlist' },
  { path: '/login', name: 'Login', component: 'Login' },
  { path: '/oauth', name: 'Blank', component: 'Blank' },
  { path: '*', component: 'NotFound', name: 'NotFound' }
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

const publicPages = ['Login', 'NotFound', 'Draft', 'Blank', 'Home']

router.beforeEach((to, from, next) => {
  // redirect to home page if logged in and trying to access login page
  if (to.name === 'Login' && tokenStore.isAuthenticated()) {
    return next('/')
  }
  // redirect to login page if not logged in and trying to access a restricted page
  const authRequired = !publicPages.includes(to.name)
  if (authRequired && !tokenStore.isAuthenticated()) {
    return next({ name: 'Login' })
  }
  return next()
})

export default router
