import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    token: localStorage.getItem('user-token')
  },
  getters: {
    isAuthenticated: state => {
      return state.token !== null
    }
  },
  mutations: {
    logIn (state, {token}) {
      state.token = token
      localStorage.setItem('user-token', token)
    },
    logOut (state) {
      state.token = null
      localStorage.removeItem('user-token')
    }
  }
})

export default store
