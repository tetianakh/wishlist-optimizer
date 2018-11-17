<template lang="html">
  <page>
    <h1>Unsaved wishlist</h1>
    <h4>Log in to save the wishlist draft</h4>
    <pricing :wishlist="wishlist"></pricing>

    <div class="row centered">
      <pricing-button :hasCards="hasCards"></pricing-button>
      <new-card-button></new-card-button>
      <b-button
        v-b-modal="'saveWishlistModal'"
        variant="success"
        v-if="authenticated && hasCards"
        class="margin">Save wishlist</b-button>
    </div>

    <b-modal id="saveWishlistModal" ok-title="Save" @ok="saveWishlist">
      <template slot="modal-title">
        Enter wishlist name:
      </template>

      <b-alert variant="danger"
           dismissible
           :show="!!modalErrorMessage"
           @dismissed="modalErrorMessage=null">
          {{ modalErrorMessage }}
      </b-alert>

      <b-form>
        <b-form-input v-model="wishlist.name"></b-form-input>
      </b-form>

    </b-modal>

    <new-card modalId="newCardModal"></new-card>
    <cards-table v-if="hasCards" :cards="wishlist.cards"></cards-table>
  </page>
</template>

<script>
import WishlistClient from '../clients/WishlistClient'
import NewCardButton from './NewCardButton'
import CardsTable from './CardsTable'
import Pricing from './Pricing'
import Page from './Page'
import NewCard from './NewCard'
import hasCards from '../mixins/hasCards'
import PricingButton from './PricingButton'
import languagesLoader from '../mixins/languagesLoader'
import {NEW_CARD, UPDATE_CARD, DELETE_CARD} from '../events'
import tokenStore from '../store/token'
import draftStore from '../store/draft'

export default {
  components: {Pricing, Page, NewCard, NewCardButton, CardsTable, PricingButton},
  data () {
    return {
      nextCardId: 0,
      wishlist: {
        name: '',
        cards: []
      },
      modalErrorMessage: '',
      wishlistClient: new WishlistClient()
    }
  },
  mounted () {
    if (draftStore.hasDraft()) {
      this.wishlist = draftStore.getDraft()
    }
    this.$eventBus.$on(NEW_CARD, this.addCard)
    this.$eventBus.$on(UPDATE_CARD, this.updateCard)
    this.$eventBus.$on(DELETE_CARD, this.deleteCard)
  },
  mixins: [hasCards, languagesLoader],
  computed: {
    authenticated () {
      return tokenStore.isAuthenticated()
    }
  },
  methods: {
    addCard (card) {
      card.id = this.nextCardId++
      this.wishlist.cards.push(card)
      draftStore.setDraft(this.wishlist)
    },
    deleteCard ({idx, cardId}) {
      this.wishlist.cards.splice(idx, 1)
      draftStore.setDraft(this.wishlist)
    },
    updateCard ({idx, card}) {
      this.wishlist.cards[idx] = card
      draftStore.setDraft(this.wishlist)
    },
    saveWishlist (event) {
      if (!this.wishlist.name) {
        event.preventDefault()
        this.modalErrorMessage = 'Please enter modal name'
        return
      }
      this.wishlistClient.saveWishlist(this.wishlist).then(wishlist => {
        draftStore.setDraft(null)
        this.$router.push({
          name: 'Wishlist',
          params: {
            id: wishlist.id
          }
        })
      })
    }
  }
}
</script>

<style lang="css">

</style>
