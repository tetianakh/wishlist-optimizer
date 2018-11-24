import axios from '../axios'

export default class ExpansionsClient {
  constructor () {
    this.http = axios
  }

  getCardExpansions (cardName) {
    const params = { 'card_name': cardName }
    return this.http.get(`expansions`, { params }).then(resp => {
      return resp.data.expansions
    })
  }
}
