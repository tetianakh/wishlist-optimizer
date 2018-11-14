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
      <b-button
        v-b-modal="'newCardModal'"
        variant="info"
        class="margin">Add new card</b-button>
      <b-button
        @click="deleteWishlist"
        variant="danger"
        class="margin">Delete wishlist</b-button>
    </div>

    <b-modal id="newCardModal" ok-title="Add" @ok="addCard">
      <template slot="modal-title">
        Add new card
      </template>

      <b-alert variant="danger"
           dismissible
           :show="modalErrorMessage !== null"
           @dismissed="modalErrorMessage=null">
          {{ modalErrorMessage }}
      </b-alert>

      <b-form>
        <b-form-group
          label="Card Name:"
          label-for="cardNameInput">
          <!-- <b-form-input v-model="newCard.name" id="cardNameInput"></b-form-input> -->
          <v-select
            :filterable="false"
            :options="searchedCardNames"
            v-model="newCard.name"
            label="name"
            @search="onCardSearch">
          </v-select>
        </b-form-group>

        <b-form-group
          label="Card quantity:"
          label-for="cardQuantityInput">
        <b-form-input v-model="newCard.quantity" id="cardQuantityInput" type="number"></b-form-input>
      </b-form-group>

      <b-form-group
        label="Card languages:"
        label-for="cardLanguagesInput">
        <b-form-select v-model="newCard.languages" :options="availableLanguages" id="cardLanguagesInput" multiple></b-form-select>
      </b-form-group>

      </b-form>

    </b-modal>

    <table class="table table-hover" v-if="hasCards">
      <thead>
        <tr>
          <th>#</th>
          <th>Card Name</th>
          <th>Card Quantity</th>
          <th>Card Languages</th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(card, idx) in wishlist.cards" :key="card.id">
          <td>{{ idx + 1 }}</td>
          <td>
            <p v-if="updatedCard.id !== card.id" @click="activateUpdate(idx)" class='hoverable'>{{ card.name }}</p>
            <b-form-input v-else v-model="updatedCard.name" type="text" @keydown.enter.native="updateCard(idx)"></b-form-input>
          </td>
          <td>
            <p v-if="updatedCard.id !== card.id" @click="activateUpdate(idx)" class='hoverable'>{{ card.quantity }}</p>
            <b-form-input v-else v-model="updatedCard.quantity" type="number" @keydown.enter.native="updateCard(idx)"></b-form-input>
          </td>
          <td>
            <p v-if="updatedCard.id !== card.id" @click="activateUpdate(idx)" class='hoverable'>{{ card.languages | join }}</p>
            <b-form-select v-else  v-model="updatedCard.languages" :options="availableLanguages" multiple ></b-form-select>
          </td>
          <td>
            <font-awesome-icon v-if="updatedCard.id !== card.id" icon="edit" @click="activateUpdate(idx)" class="hoverable"/>
            <font-awesome-icon v-else icon="check" @click="updateCard(idx)" class="hoverable"/>
          </td>
          <td>
            <font-awesome-icon v-if="updatedCard.id !== card.id" icon="trash" @click="deleteCard(card.id, idx)" class="hoverable"/>
            <font-awesome-icon v-else icon="times" @click="closeUpdate()" class="hoverable"/>
          </td>
        </tr>
      </tbody>
    </table>
  </page>
</template>

<script>
import _ from 'lodash'
import vSelect from 'vue-select'
import WishlistClient from '../clients/WishlistClient'
import PricingClient from '../clients/PricingClient'
import LanguagesClient from '../clients/LanguagesClient'
import MtgClient from '../clients/MtgClient'
import Spinner from './MtgSpinnerRound'
import Pricing from './Pricing'
import Page from './Page'

const searchCardByName = _.debounce((searchTerm, loading, self) => {
  self.mtgClient.getCards(searchTerm).then(res => {
    self.searchedCards = res
    loading(false)
  })
}, 350)

export default {
  components: {Spinner, Pricing, Page, vSelect},
  data () {
    return {
      wishlist: {},
      wishlistClient: new WishlistClient(),
      pricingClient: new PricingClient(),
      languagesClient: new LanguagesClient(),
      mtgClient: new MtgClient(),
      newCard: {
        name: '',
        quantity: 1,
        languages: []
      },
      updatedCard: {
        id: null,
        name: null,
        quantity: null
      },
      loadingPricing: false,
      pricingJobId: null,
      pricing: [],
      errorMessage: null,
      infoMessage: null,
      modalErrorMessage: null,
      availableLanguages: [],
      searchedCards: []
    }
  },
  computed: {
    searchedCardNames () {
      return Array.from(new Set(this.searchedCards.map(c => c.name)))
    },
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
    this.languagesClient.getAvailableLanguages().then(resp => {
      this.availableLanguages = resp
    })
  },
  filters: {
    join: function (values) {
      return values.join(', ')
    }
  },
  methods: {
    addCard (event) {
      if (!this.newCard.name || !this.newCard.quantity) {
        event.preventDefault()
        this.modalErrorMessage = 'Please fill in card name'
        return
      }
      this.wishlistClient.addCard(this.$route.params.id, this.newCard).then(resp => {
        this.wishlist.cards.push(resp.card)
        this.newCard = {
          name: '',
          quantity: 1,
          languages: []
        }
        this.searchedCards = []
      })
    },
    deleteCard (cardId, idx) {
      this.wishlistClient.removeCard(this.$route.params.id, cardId).then(() => {
        this.wishlist.cards.splice(idx, 1)
      })
    },
    deleteWishlist () {
      this.wishlistClient.removeWishlist(this.$route.params.id).then(() => {
        this.$router.push({'name': 'Home'})
      })
    },
    activateUpdate (cardIdx) {
      this.updatedCard = this.wishlist.cards[cardIdx]
    },
    updateCard (cardIdx) {
      this.wishlistClient.updateCard(this.$route.params.id, this.updatedCard).then(resp => {
        this.wishlist.cards[cardIdx] = resp.card
        this.closeUpdate()
      })
    },
    closeUpdate () {
      this.updatedCard = {
        id: null,
        name: null,
        quantity: null
      }
    },
    submitPricingJob () {
      this.pricing = []
      this.pricingClient.submitPricingCalculationJob(this.wishlist.id).then(resp => {
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
        } else if (resp.job_status === 'failed' || resp.result.error !== null) {
          this.loadingPricing = false
          this.errorMessage = resp.result.error || 'Failed to fetch pricing data'
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
    },
    onCardSearch (searchTerm, loading) {
      if (searchTerm.length < 2) {
        return
      }
      loading(true)
      searchCardByName(searchTerm, loading, this)
    }
  }
}
</script>

<style lang="css">
.margin {
  margin: 10px;
}

</style>
