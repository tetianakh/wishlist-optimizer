<template lang="html">
  <table class="table table-hover table-sm" id="cards-table">
    <thead>
      <tr>
        <th>#</th>
        <th>Name</th>
        <th>Quantity</th>
        <th>Languages</th>
        <th>Expansions</th>
        <th></th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <card-row :idx="idx" :card="card"
        v-for="(card, idx) in cards"
        @update-card="updateCard"
        @delete-card="deleteCard"
        :key="card.id"></card-row>
    </tbody>
  </table>
</template>

<script>
import CardRow from './CardRow'
import { UPDATE_CARD, DELETE_CARD } from '../events'

export default {
  props: ['cards'],
  components: { CardRow },
  methods: {
    // propagate events to parent component
    updateCard (args) {
      this.$emit(UPDATE_CARD, args)
    },
    deleteCard (args) {
      this.$emit(DELETE_CARD, args)
    }
  }
}
</script>

<style lang="css">
#cards-table {
  margin-bottom: 150px;
}
</style>
