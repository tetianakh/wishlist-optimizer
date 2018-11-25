<template lang="html">
  <page>
    <h1 v-if="!editingName" @click="activateEditName" class="hoverable">{{ wishlist.name }} </h1>
    <input v-else id="nameInput" ref="nameInput" v-model="newName" type="text" @keydown.enter="updateName" @blur="closeEditName"></input>

    <pricing :wishlist="wishlist"></pricing>

    <div class="row centered">
      <new-card-button></new-card-button>
      <file-upload-button></file-upload-button>
      <b-button
        size="sm"
        @click="deleteWishlist"
        variant="danger"
        class="margin">Delete wishlist</b-button>
    </div>

    <file-upload-modal v-on:new-cards="addCards"></file-upload-modal>

    <new-card modalId="newCardModal" v-on:new-card="addCard"></new-card>

    <cards-table v-if="hasCards"
      @update-card="updateCard"
      @delete-card="deleteCard"
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
      wishlist: {},
      wishlistClient: new WishlistClient(),
      editingName: false,
      newName: ''
    }
  },
  mixins: [hasCards, languagesLoader],
  created () {
    this.wishlistClient.getWishlist(this.$route.params.id).then(resp => {
      this.wishlist = resp.wishlist
      this.newName = resp.wishlist.name
    })
  },
  methods: {
    addCard (card) {
      this.wishlistClient.addCard(this.$route.params.id, card).then(resp => {
        this.wishlist.cards.push(resp.card)
      })
    },
    deleteCard ({ idx, cardId }) {
      this.wishlistClient.removeCard(this.$route.params.id, cardId).then(() => {
        this.wishlist.cards.splice(idx, 1)
      })
    },
    deleteWishlist () {
      this.wishlistClient.removeWishlist(this.$route.params.id).then(() => {
        this.$router.push({ 'name': 'Home' })
      })
    },
    updateCard ({ idx, card }) {
      this.wishlistClient.updateCard(this.$route.params.id, card).then(resp => {
        this.wishlist.cards[idx] = resp.card
      })
    },
    addCards (cards) {
      this.wishlistClient.addCards(this.$route.params.id, { cards }).then(resp => {
        this.wishlist = resp.wishlist
      })
    },
    closeEditName () {
      this.editingName = false
      this.newName = this.wishlist.name
    },
    activateEditName () {
      this.editingName = true
      this.$nextTick(() => this.$refs.nameInput.focus())
    },
    updateName (event) {
      if (!this.newName) {
        event.preventDefault()
        return
      }
      if (this.newName == this.wishlist.name){
        return
      }
      this.editingName = false
      this.wishlistClient.renameWishlist(this.wishlist.id, this.newName).then(resp => {
        this.wishlist.name = resp.name
      })
    }
  }
}
</script>

<style lang="css">
#nameInput:focus {
  margin: auto;
  width: 300px;
  height: 3.5rem;
  border-top: none;
  border-right: none;
  border-left: none;
  border-radius: 0;
  border-bottom: 2px solid grey;
  padding: 0px 0px 15px 0px;
  font-size: 2.5rem;
  text-align: center;
  outline: 0;
}
</style>
