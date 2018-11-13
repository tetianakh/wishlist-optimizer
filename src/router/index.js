import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
  { path: '/', name: 'Home', component: 'Home' },
  { path: '/wishlist/:id', name: 'wishlist', component: 'Wishlist' },
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
export default new Router({
  routes,
  mode: 'history'
})
