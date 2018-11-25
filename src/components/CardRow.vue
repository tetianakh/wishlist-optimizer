<template lang="html">
  <tr>
    <td>{{ idx + 1 }}</td>
    <td>
      <p v-if="!editing" @click="activateUpdate()" class='hoverable'>{{ card.name }}</p>
      <b-form-input v-else v-model="card.name" type="text" @keydown.enter.native="updateCard()"></b-form-input>
    </td>
    <td>
      <p v-if="!editing" @click="activateUpdate()" class='hoverable'>{{ card.quantity }}</p>
      <b-form-input v-else v-model="card.quantity" type="number" @keydown.enter.native="updateCard()"></b-form-input>
    </td>
    <td>
      <p v-if="!editing" @click="activateUpdate()" class='hoverable'>{{ card.languages | join }}</p>
      <b-form-select v-else  v-model="card.languages"
        :options="$store.state.availableLanguages" multiple ></b-form-select>
    </td>
    <td>
      <p v-if="!editing" @click="activateUpdate()" class='hoverable'>{{ card.expansions | join }}</p>
      <b-form-select v-else  v-model="card.expansions"
        :options="availableExpansions" multiple ></b-form-select>
    </td>
    <td>
      <p v-if="!editing" @click="activateUpdate()" class='hoverable'>{{ card.foil | humanize }}</p>
      <b-form-select v-else  v-model="card.foil"
        :options="foilOptions" ></b-form-select>
    </td>
    <td>
      <font-awesome-icon v-if="!editing" icon="edit" @click="activateUpdate" class="hoverable"/>
      <font-awesome-icon v-else icon="check" @click="updateCard" class="hoverable"/>
    </td>
    <td>
      <font-awesome-icon v-if="!editing" icon="trash" @click="deleteCard" class="hoverable"/>
      <font-awesome-icon v-else icon="times" @click="closeUpdate" class="hoverable"/>
    </td>
  </tr>

</template>

<script>
import { DELETE_CARD, UPDATE_CARD } from '../events'
import ExpansionsClient from '../clients/ExpansionsClient'
import foilOptions from '../mixins/foilOptions'

export default {
  props: ['idx', 'card'],
  data () {
    return {
      editing: false,
      expansionsClient: new ExpansionsClient(),
      availableExpansions: []
    }
  },
  filters: {
    join (values) {
      return values ? values.join(', ') : ''
    }
  },
  mixins: [foilOptions],
  methods: {
    updateCard () {
      this.$emit(UPDATE_CARD, { idx: this.idx, card: this.card })
      this.closeUpdate()
    },
    deleteCard (cardId, idx) {
      this.$emit(DELETE_CARD, { idx: this.idx, cardId: this.card.id })
    },
    activateUpdate () {
      this.editing = true
      if (this.availableExpansions.length === 0) {
        this.expansionsClient.getCardExpansions(this.card.name).then(result => {
          this.availableExpansions = result || []
        })
      }
    },
    closeUpdate () {
      this.editing = false
    }
  }
}
</script>

<style lang="css">
td > p {
  margin-bottom: auto;
}
</style>
