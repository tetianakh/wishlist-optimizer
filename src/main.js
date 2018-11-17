import Vue from 'vue'
import App from './App'
import VueAxios from 'vue-axios'
import VueAuthenticate from 'vue-authenticate'
import axios from 'axios'
import router from './router'
import store from './store/store'
import BootstrapVue from 'bootstrap-vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faEdit, faTrash, faCheck, faTimes } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faEdit)
library.add(faTrash)
library.add(faCheck)
library.add(faTimes)

Vue.prototype.$eventBus = new Vue()

Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.use(VueAxios, axios)

const baseApiUrl = process.env.API_URL.replace('/api', '')
const oauthRedirectUri = baseApiUrl + '/oauth'
console.log(oauthRedirectUri)
console.log(baseApiUrl)
Vue.use(VueAuthenticate, {
  baseUrl: baseApiUrl, // Your API domain

  providers: {
    google: {
      clientId: '1000794530745-gnf0qu137rac5kgcskkphuohfqlp8ahu.apps.googleusercontent.com',
      requiredUrlParams: ['scope', 'access_type'],
      accessType: 'offline',
      redirectUri: oauthRedirectUri
    }
  }
})
Vue.use(BootstrapVue)
Vue.config.productionTip = false
/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  render: h => h(App)
})
