<template lang="html">
  <div>
    <spinner v-if="loading"></spinner>

    <table class='table table-hover' v-if="pricing.length > 0">
      <thead>
        <th>Seller Username</th>
        <th>Has # cards</th>
        <th>Total price</th>
      </thead>
      <tbody>
        <tr v-for="item in pricing" :key="item.seller_id">
          <td><a :href="item.seller_url" target="_blank">{{ item.seller_username }}</a></td>
          <td>{{ item.total_count }}</td>
          <td>{{ item.total_price.toFixed(2) }}€</td>
        </tr>
      </tbody>
    </table>

    <div class="centered">
      <b-button
        variant="success"
        v-if="hasCards"
        @click="submitPricingJob"
        class="margin">Get Pricing</b-button>
    </div>
    <b-alert variant="danger"
         dismissible
         :show="errorMessage !== null"
         @dismissed="errorMessage=null">
        {{ errorMessage }}
    </b-alert>
    <b-alert variant="info"
         dismissible
         :show="infoMessage !== null"
         @dismissed="infoMessage=null">
        {{ infoMessage }}
    </b-alert>
  </div>
</template>

<script>
import PricingClient from '../clients/PricingClient'
import Spinner from './MtgSpinnerRound'
import hasCards from '../mixins/hasCards'

export default {
  props: ['wishlist'],
  components: {Spinner},
  data () {
    return {
      pricingClient: new PricingClient(),
      errorMessage: null,
      infoMessage: null,
      pricing: [],
      pricingJobId: null,
      loading: false
    }
  },
  mixins: [hasCards],
  methods: {
    submitPricingJob () {
      if (!this.wishlist || !this.wishlist.cards) {
        return
      }
      this.pricing = []
      this.pricingClient.submitPricingCalculationJob(this.wishlist).then(resp => {
        console.log(resp)
        this.pricingJobId = resp.job_id
        this.getPricingResult()
      })
    },
    getPricingResult () {
      console.log('Getting pricing result')
      this.loading = true
      this.pricingClient.getPricingJobResult(this.pricingJobId).then(resp => {
        if (resp.job_result === null && (resp.job_status === 'started' || resp.job_status === 'queued')) {
          setTimeout(this.getPricingResult, 1000)
        } else if (resp.job_status === 'failed' || resp.job_result.error !== null) {
          this.loading = false
          console.error(resp.job_result.error)
          this.errorMessage = 'Failed to fetch pricing data'
        } else {
          this.loading = false
          console.log(resp.job_result)
          this.pricing = resp.job_result.result === null ? [] : resp.job_result.result
          if (this.pricing.length === 0) {
            this.infoMessage = 'No data was found for these cards'
          }
        }
      }).catch(e => {
        console.error(e)
        this.loading = false
        this.errorMessage = 'Failed to fetch pricing data'
      })
    }
  }
}
</script>

<style lang="css">
</style>
