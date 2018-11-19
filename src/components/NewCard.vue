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
        <div>
          <multiselect
          :options="searchedCardNames"
          @search-change="onCardSearch"
          v-model="newCard.name"
          :multiple="false"
          :searchable="true"
          :close-on-select="true"
          placeholder="Search card by name"
          :clear-on-select="false"
          :allow-empty="false"
          :loading="isLoading"></multiselect>

        </div>
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
import Multiselect from 'vue-multiselect'
import {NEW_CARD} from '../events'
import MtgClient from '../clients/MtgClient'

export default {
  components: {Multiselect},
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
      isLoading: false,
      mtgClient: new MtgClient()
    }
  },
  computed: {
    searchedCardNames () {
      return Array.from(new Set(this.searchedCards.map(c => c.name)))
    }
  },
  methods: {
    limitText (count) {
      return `and ${count} other cards`
    },
    addCard (event) {
      if (!this.newCard.name || !this.newCard.quantity) {
        event.preventDefault()
        this.modalErrorMessage = 'Please fill in card name'
        return
      }
      this.$emit(NEW_CARD, this.newCard)
      this.newCard = {
        name: '',
        quantity: 1,
        languages: []
      }
      this.searchedCards = []
    },
    onCardSearch (query) {
      console.log(query)
      if (query.length < 3) {
        return
      }
      this.isLoading = true
      this.mtgClient.getCards(query).then(response => {
        this.searchedCards = response
        this.isLoading = false
      })
    }
  }
}
</script>
