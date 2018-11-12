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
    },
    logOut (state) {
      state.token = null
    }
  },
  actions: {
    logIn (context, {token}) {
      localStorage.setItem('user-token', token)
      context.commit('logIn', token)
    },
    logOut (context) {
      localStorage.removeItem('user-token')
      context.commit('logOut')
    }
  }
})

export default store
