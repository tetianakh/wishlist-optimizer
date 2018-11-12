import axios from 'axios'
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
    config.headers.authorization = store.state.token
    return config
  },
  error => Promise.reject(error)
)

export default instance
