<template lang="html">
  <page>
    <h1>New wishlist</h1>
    <p></p>
    <pricing :wishlist="wishlist"></pricing>

    <div class="row centered">
      <new-card-button></new-card-button>
      <file-upload-button></file-upload-button>
      <div v-b-tooltip.hover :title="tooltipTitle">
        <b-button
          v-b-modal="'saveWishlistModal'"
          variant="info"
          :disabled="!authenticated"
          v-if="hasCards"
          class="margin">Save wishlist</b-button>
      </div>
    </div>

    <file-upload-modal v-on:new-cards="addCards"></file-upload-modal>

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

    <new-card modalId="newCardModal" v-on:new-card="addCard"></new-card>
    <cards-table v-if="hasCards"
      v-on:update-card="updateCard"
      v-on:delete-card="deleteCard"
      :cards="wishlist.cards"></cards-table>
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
import languagesLoader from '../mixins/languagesLoader'
import FileUploadButton from './FileUploadButton'
import FileUploadModal from './FileUploadModal'
import tokenStore from '../store/token'
import draftStore from '../store/draft'

export default {
  components: {
    Pricing,
    Page,
    NewCard,
    NewCardButton,
    CardsTable,
    FileUploadModal,
    FileUploadButton
  },
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
    if (this.wishlist.cards.length > 0) {
      this.nextCardId = this.wishlist.cards[this.wishlist.cards.length - 1].id + 1
    }
  },
  mixins: [hasCards, languagesLoader],
  computed: {
    authenticated () {
      return tokenStore.isAuthenticated()
    },
    tooltipTitle () {
      return this.authenticated ? null : 'Log In To Save'
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
    },
    addCards (cards) {
      for (let card of cards) {
        card.id = this.nextCardId++
        this.wishlist.cards.push(card)
      }
      draftStore.setDraft(this.wishlist)
    }
  }
}
</script>

<style lang="css">

</style>
