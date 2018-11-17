import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    availableLanguages: []
  },
  getters: {
  },
  mutations: {
    setLanguages (state, languages) {
      state.availableLanguages = languages
    }
  },
  actions: {
  }
})

export default store
