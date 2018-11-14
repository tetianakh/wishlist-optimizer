import axios from 'axios'
import {logOut} from './auth'
import store from './store/store'

const instance = axios.create({
  baseURL: process.env.API_URL,
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json'
  }
})

instance.interceptors.request.use(
  config => {
    if (store.getters.isAuthenticated) {
      config.headers.Authorization = 'Bearer ' + store.state.token
    }
    return config
  },
  error => Promise.reject(error)
)

const BASE_AUTH_URL = process.env.API_URL.replace('/api', '/auth')
const INVALID_TOKEN = 'Invalid auth token'

const updateToken = () => {
  const headers = {'Authorization': store.state.token}
  return axios.post(`${BASE_AUTH_URL}/refresh`, {}, {headers})
    .then(resp => resp.data.token).catch(e => {
      logOut()
      throw e
    })
}

instance.interceptors.response.use(null, (error) => {
  if (error.config && error.response && error.response.status === 401 && error.response.data.error === INVALID_TOKEN && store.getters.isAuthenticated) {
    return updateToken().then((token) => {
      store.dispatch('logIn', {token}).then(() => {
        error.config.headers.Authorization = 'Bearer ' + token
        return instance.request(error.config)
      })
    })
  } else if (error.response && error.response.status === 401) {
    logOut()
  }
  return Promise.reject(error)
})

export default instance
