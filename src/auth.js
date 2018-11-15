import jwtDecode from 'jwt-decode'

import tokenStore from './store/token'

const EXP_TIME_WINDOW = 10 // seconds

const logOut = () => {
  tokenStore.logOut()
  location.reload()
}

const tokenIsExpired = () => {
  const now = Date.now().valueOf() / 1000
  const decoded = jwtDecode(tokenStore.getToken())
  return decoded.exp < (now - EXP_TIME_WINDOW)
}

export {logOut, tokenIsExpired}
