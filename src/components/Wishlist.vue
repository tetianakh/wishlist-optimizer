<template lang="html">
  <page>
    <h1>{{ wishlist.name }}</h1>
    <spinner v-if="loadingPricing"></spinner>

    <pricing :pricing="pricing" v-if="pricing.length > 0"></pricing>

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

    <div class="row centered">
      <b-button
        variant="success"
        v-if="hasCards"
        @click="submitPricingJob"
        :disabled="loadingPricing"
        class="margin">Get Pricing</b-button>
      <new-card-button></new-card-button>
      <b-button
        @click="deleteWishlist"
        variant="danger"
        class="margin">Delete wishlist</b-button>
    </div>

    <new-card modalId="newCardModal" :availableLanguages="availableLanguages"></new-card>

    <cards-table  v-if="hasCards" :cards="wishlist.cards"></cards-table>
  </page>
</template>

<script>
import WishlistClient from '../clients/WishlistClient'
import PricingClient from '../clients/PricingClient'
import LanguagesClient from '../clients/LanguagesClient'
import NewCardButton from './NewCardButton'
import CardsTable from './CardsTable'
import Spinner from './MtgSpinnerRound'
import Pricing from './Pricing'
import Page from './Page'
import NewCard from './NewCard'
import {NEW_CARD, UPDATE_CARD, DELETE_CARD} from '../events'

export default {
  components: {Spinner, Pricing, Page, NewCard, NewCardButton, CardsTable},
  data () {
    return {
      wishlist: {},
      wishlistClient: new WishlistClient(),
      pricingClient: new PricingClient(),
      languagesClient: new LanguagesClient(),
      loadingPricing: false,
      pricingJobId: null,
      pricing: [],
      errorMessage: null,
      infoMessage: null,
      searchedCards: [],
      availableLanguages: []
    }
  },
  mounted () {
    this.languagesClient.getAvailableLanguages().then(languages => {
      this.$store.commit('setLanguages', languages)
    })
    this.$eventBus.$on(NEW_CARD, this.addCard)
    this.$eventBus.$on(UPDATE_CARD, this.updateCard)
    this.$eventBus.$on(DELETE_CARD, this.deleteCard)
  },
  computed: {
    hasCards () {
      return this.wishlist && this.wishlist.cards && this.wishlist.cards.length > 0
    }
  },
  created () {
    this.wishlistClient.getWishlist(this.$route.params.id).then(resp => {
      this.wishlist = {
        id: resp.wishlist.id,
        name: resp.wishlist.name,
        created_at: resp.wishlist.created_at,
        cards: resp.wishlist.cards
      }
    })
  },
  methods: {
    addCard (card) {
      this.wishlistClient.addCard(this.$route.params.id, card).then(resp => {
        this.wishlist.cards.push(resp.card)
      })
    },
    deleteCard ({idx, cardId}) {
      this.wishlistClient.removeCard(this.$route.params.id, cardId).then(() => {
        this.wishlist.cards.splice(idx, 1)
      })
    },
    deleteWishlist () {
      this.wishlistClient.removeWishlist(this.$route.params.id).then(() => {
        this.$router.push({'name': 'Home'})
      })
    },
    updateCard ({idx, card}) {
      this.wishlistClient.updateCard(this.$route.params.id, card).then(resp => {
        this.wishlist.cards[idx] = resp.card
      })
    },
    submitPricingJob () {
      this.pricing = []
      this.pricingClient.submitPricingCalculationJob(this.wishlist).then(resp => {
        console.log(resp)
        this.pricingJobId = resp.job_id
        this.getPricingResult()
      })
    },
    getPricingResult () {
      console.log('Getting pricing result')
      this.loadingPricing = true
      this.pricingClient.getPricingJobResult(this.pricingJobId).then(resp => {
        if (resp.job_result === null && (resp.job_status === 'started' || resp.job_status === 'queued')) {
          setTimeout(this.getPricingResult, 1000)
        } else if (resp.job_status === 'failed' || resp.job_result.error !== null) {
          this.loadingPricing = false
          console.error(resp.job_result.error)
          this.errorMessage = 'Failed to fetch pricing data'
        } else {
          this.loadingPricing = false
          console.log(resp.job_result)
          this.pricing = resp.job_result.result === null ? [] : resp.job_result.result
          if (this.pricing.length === 0) {
            this.infoMessage = 'No data was found for these cards'
          }
        }
      }).catch(e => {
        console.error(e)
        this.loadingPricing = false
        this.errorMessage = 'Failed to fetch pricing data'
      })
    }
  }
}
</script>

<style lang="css">
.margin {
  margin: 10px;
}

</style>
