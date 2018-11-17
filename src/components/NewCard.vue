<template lang="html">
  <b-modal :id="modalId" ok-title="Add" @ok="addCard">
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
      <b-form-select v-model="newCard.languages"
        :options="$store.state.availableLanguages"
        id="cardLanguagesInput" multiple></b-form-select>
    </b-form-group>

    </b-form>

  </b-modal>
</template>

<script>
import _ from 'lodash'
import vSelect from 'vue-select'
import {NEW_CARD} from '../events'
import MtgClient from '../clients/MtgClient'

const searchCardByName = _.debounce((searchTerm, loading, self) => {
  self.mtgClient.getCards(searchTerm).then(res => {
    self.searchedCards = res
    loading(false)
  })
}, 350)

export default {
  components: {vSelect},
  props: ['modalId'],
  data () {
    return {
      modalErrorMessage: null,
      searchedCards: [],
      newCard: {
        name: '',
        quantity: 1,
        languages: []
      },
      mtgClient: new MtgClient()
    }
  },
  computed: {
    searchedCardNames () {
      return Array.from(new Set(this.searchedCards.map(c => c.name)))
    }
  },
  mounted () {
  },
  methods: {
    addCard (event) {
      if (!this.newCard.name || !this.newCard.quantity) {
        event.preventDefault()
        this.modalErrorMessage = 'Please fill in card name'
        return
      }
      this.$eventBus.$emit(NEW_CARD, this.newCard)
      this.newCard = {
        name: '',
        quantity: 1,
        languages: []
      }
      this.searchedCards = []
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
</style>
