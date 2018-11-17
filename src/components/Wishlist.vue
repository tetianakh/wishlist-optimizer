<template lang="html">
  <page>
    <h1>{{ wishlist.name }}</h1>
    <pricing :wishlist="wishlist"></pricing>

    <div class="row centered">
      <new-card-button></new-card-button>
      <b-button
        @click="deleteWishlist"
        variant="danger"
        class="margin">Delete wishlist</b-button>
    </div>

    <new-card modalId="newCardModal" :availableLanguages="availableLanguages"></new-card>
    <cards-table v-if="hasCards" :cards="wishlist.cards"></cards-table>
  </page>
</template>

<script>
import WishlistClient from '../clients/WishlistClient'
import LanguagesClient from '../clients/LanguagesClient'
import NewCardButton from './NewCardButton'
import CardsTable from './CardsTable'
import Pricing from './Pricing'
import Page from './Page'
import NewCard from './NewCard'
import hasCards from '../mixins/hasCards'
import {NEW_CARD, UPDATE_CARD, DELETE_CARD, CALCULATE_PRICING} from '../events'

export default {
  components: {Pricing, Page, NewCard, NewCardButton, CardsTable},
  data () {
    return {
      wishlist: {},
      wishlistClient: new WishlistClient(),
      languagesClient: new LanguagesClient(),
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
  mixins: [hasCards],
  created () {
    this.wishlistClient.getWishlist(this.$route.params.id).then(resp => {
      this.wishlist = resp.wishlist
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
      this.$eventBus.$emit(CALCULATE_PRICING, this.wishlist)
    }
  }
}
</script>

<style lang="css">

</style>
