const TOKEN = 'user-token'

class TokenStore {
  getToken () {
    return localStorage.getItem(TOKEN)
  }
  isAuthenticated () {
    return !!this.getToken()
  }
  logIn (token) {
    localStorage.setItem(TOKEN, token)
  }
  logOut () {
    localStorage.removeItem('user-token')
  }
}

export default new TokenStore()
