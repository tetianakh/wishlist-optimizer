import axios from '../axios'

export default class PricingClient {
  constructor () {
    this.http = axios
  }

  getAvailableLanguages () {
    return this.http.get('languages').then(resp => {
      return resp.data
    })
  }
}
