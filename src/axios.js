import axios from 'axios'

import {logOut, tokenIsExpired} from './auth'
import tokenStore from './store/token'

const instance = axios.create({
  baseURL: process.env.API_URL,
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json'
  }
})

instance.interceptors.request.use(
  config => {
    if (tokenStore.isAuthenticated()) {
      config.headers.Authorization = 'Bearer ' + tokenStore.getToken()
    }
    return config
  },
  error => Promise.reject(error)
)

const BASE_AUTH_URL = process.env.API_URL.replace('/api', '/auth')

const updateToken = () => {
  const headers = {'Authorization': tokenStore.getToken()}
  return axios.post(`${BASE_AUTH_URL}/refresh`, {}, {headers})
    .then(resp => resp.data.token)
}

instance.interceptors.request.use((config) => {
  const originalRequest = config

  if (tokenStore.isAuthenticated()) {
    let tokenExpired
    try {
      tokenExpired = tokenIsExpired()
    } catch (e) {
      // token is invalid and couldn't be decoded, clear it
      logOut()
      return Promise.reject(e)
    }
    if (tokenExpired) {
      return updateToken().then((token) => {
        return tokenStore.logIn(token)
      }).then(() => {
        originalRequest['Authorization'] = 'Bearer ' + tokenStore.getToken()
        return Promise.resolve(originalRequest)
      }).catch(e => {
        logOut()
        return Promise.reject(e)
      })
    }
  }
  return config
}, err => Promise.reject(err)
)
//
// instance.interceptors.response.use(null, (error) => {
//  if (error.config && error.response && error.response.status === 401 && error.response.data.error === INVALID_TOKEN && tokenStore.getters.isAuthenticated) {
//    return updateToken().then((token) => {
//      tokenStore.dispatch('logIn', {token}).then(() => {
//        error.config.headers.Authorization = 'Bearer ' + token
//        return instance.request(error.config)
//      })
//    })
//  } else if (error.response && error.response.status === 401) {
//    logOut()
//  }
//  return Promise.reject(error)
// })

export default instance
