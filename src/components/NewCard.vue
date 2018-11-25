<template lang="html">
  <b-modal :id="modalId" button-size="sm" ok-title="Add" @ok="addCard" @cancel="clear">
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
          @select="onCardSelect"
          v-model="newCard.name"
          :multiple="false"
          :searchable="true"
          :close-on-select="true"
          placeholder="Search card by name"
          :clear-on-select="true"
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
      label="Foil?"
      label-for="foilSelect">
      <b-form-select v-model="newCard.foil"
        :options="foilOptions"
        id="foilSelect"></b-form-select>
    </b-form-group>

    <b-form-group
      label="Card languages:"
      label-for="cardLanguagesInput">
      <b-form-select v-model="newCard.languages"
        :options="$store.state.availableLanguages"
        id="cardLanguagesInput" multiple></b-form-select>
    </b-form-group>

    <b-form-group
      label="Card Expansions:"
      label-for="cardExpansionsInput">
      <b-form-select
        v-if="!isLoadingExpansions"
        v-model="newCard.expansions"
        :options="availableExpansions"
        id="cardExpansionsInput"
        multiple></b-form-select>
      <p v-else>Loading...</p>
    </b-form-group>

    </b-form>

  </b-modal>
</template>

<script>
import Multiselect from 'vue-multiselect'
import { NEW_CARD } from '../events'
import MtgClient from '../clients/MtgClient'
import ExpansionsClient from '../clients/ExpansionsClient'
import foilOptions from '../mixins/foilOptions'

export default {
  components: { Multiselect },
  props: ['modalId'],
  data () {
    return {
      modalErrorMessage: null,
      searchedCards: [],
      newCard: {
        name: '',
        quantity: 1,
        languages: [],
        expansions: [],
        foil: null
      },
      isLoading: false,
      isLoadingExpansions: false,
      mtgClient: new MtgClient(),
      expansionsClient: new ExpansionsClient(),
      availableExpansions: []
    }
  },
  mixins: [foilOptions],
  computed: {
    searchedCardNames () {
      return Array.from(new Set(this.searchedCards.map(c => c.name)))
    }
  },
  methods: {
    limitText (count) {
      return `and ${count} other cards`
    },
    clear () {
      console.log('clearing')
      this.newCard = {
        name: '',
        quantity: 1,
        languages: [],
        expansions: [],
        foil: null
      }
      this.availableExpansions = []
      this.searchedCards = []
    },
    addCard (event) {
      if (!this.newCard.name || !this.newCard.quantity) {
        event.preventDefault()
        this.modalErrorMessage = 'Please fill in card name'
        return
      }
      console.log(this.newCard)
      this.$emit(NEW_CARD, this.newCard)
      this.clear()
    },
    onCardSelect (cardName) {
      console.log(cardName)
      this.isLoadingExpansions = true
      this.expansionsClient.getCardExpansions(cardName).then(response => {
        console.log(response)
        this.availableExpansions = response || []
        this.isLoadingExpansions = false
      })
    },
    onCardSearch (query) {
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
