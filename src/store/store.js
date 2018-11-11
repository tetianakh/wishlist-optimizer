import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    user: null
  },
  mutations: {
    logIn (state, {user}) {
      state.user = user
    },
    logOut (state) {
      state.user = null
    }
  }
})

export default store
