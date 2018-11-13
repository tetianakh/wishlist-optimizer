import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    token: localStorage.getItem('user-token')
  },
  getters: {
    isAuthenticated: state => {
      return Boolean(state.token)
    }
  },
  mutations: {
    logIn (state, token) {
      state.token = token
    },
    logOut (state) {
      state.token = null
    }
  },
  actions: {
    logIn ({commit}, {token}) {
      localStorage.setItem('user-token', token)
      commit('logIn', token)
    },
    logOut (context) {
      localStorage.removeItem('user-token')
      context.commit('logOut')
    }
  }
})

export default store
