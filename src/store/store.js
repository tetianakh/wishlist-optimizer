import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    token: null
  },
  mutations: {
    logIn (state, {token}) {
      state.token = token
    },
    logOut (state) {
      state.token = null
    }
  }
})

export default store
