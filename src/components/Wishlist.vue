<template lang="html">
  <div class="">
    <h1>{{ wishlist.name }}</h1>
    <spinner v-if="loadingPricing"></spinner>

    <pricing :pricing="pricing" v-if="pricing.length > 0"></pricing>

    <b-button
      variant="success"
      @click="submitPricingJob"
      :disabled="loadingPricing"
      class="margin">Get Pricing</b-button>

    <div class="row">
        <div class="col-lg-5 col-centered">
      <b-form inline>
      <b-input class="mb-2 mr-sm-2 mb-sm-0" placeholder="Card Name" v-model="newCard.name"/>
      <b-input-group left="@" class="mb-2 mr-sm-2 mb-sm-0">
        <b-form-input v-model="newCard.quantity" type="number" placeholder="Card Quantity"></b-form-input>
      </b-input-group>
      <b-button variant="primary" @click="addCard">Add card</b-button>
      </b-form>
    </div>
  </div>

    <table class="table table-hover" v-if="wishlist.cards && wishlist.cards.length > 0">
      <thead>
        <tr>
          <th>#</th>
          <th>Card name</th>
          <th>Card quantity</th>
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
  </div>
</template>

<script>
import WishlistClient from '../clients/WishlistClient'
import PricingClient from '../clients/PricingClient'
import Spinner from './Spinner'
import Pricing from './Pricing'

export default {
  components: {Spinner, Pricing},
  data () {
    return {
      wishlist: {},
      wishlistClient: new WishlistClient(),
      pricingClient: new PricingClient(),
      newCard: {
        name: null,
        quantity: null
      },
      updatedCard: {
        id: null,
        name: null,
        quantity: null
      },
      loadingPricing: false,
      pricingJobId: null,
      pricing: []
    }
  },
  mounted () {
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
    addCard () {
      if (!this.newCard.name || !this.newCard.quantity) {
        return
      }
      this.wishlistClient.addCard(this.$route.params.id, this.newCard).then(resp => {
        this.wishlist.cards.push(resp.card)
        this.newCard = {
          name: '',
          quantity: null
        }
      })
    },
    deleteCard (cardId, idx) {
      this.wishlistClient.removeCard(this.$route.params.id, cardId).then(() => {
        this.wishlist.cards.splice(idx, 1)
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
        if (resp.job_result === null && resp.job_status === 'started') {
          setTimeout(this.getPricingResult, 1000)
        } else {
          this.loadingPricing = false
          this.pricing = resp.job_result
          console.log(this.pricing)
        }
      })
    }
  }
}
</script>

<style lang="css">
.margin {
  margin: 10px;
}
.hoverable {
  cursor: pointer;
}
.col-centered{
    margin: 10px auto;
    float: none;
}

</style>
