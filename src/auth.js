import store from './store/store'
import router from './router'

const logOut = () => {
  store.dispatch('logOut').then(() => router.push({name: 'Login'}))
}

export {logOut}
