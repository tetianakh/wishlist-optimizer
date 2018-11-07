import axios from '../axios'

export default class PricingClient {
  constructor () {
    this.http = axios
  }

  submitPricingCalculationJob (wishlistId) {
    const payload = {'wishlist_id': wishlistId}
    return this.http.post('pricing', payload).then(resp => {
      console.log(resp.data.job_status)
      return resp.data
    })
  }

  getPricingJobResult (jobId) {
    return this.http.get(`pricing/${jobId}`).then(resp => {
      console.log(resp.data.job_status)
      return resp.data
    })
  }
}
