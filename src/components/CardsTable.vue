<template lang="html">
  <table class="table table-hover">
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
      <card-row :idx="idx" :card="card"
        v-for="(card, idx) in cards" :key="card.id"></card-row>
    </tbody>
  </table>
</template>

<script>
import CardRow from './CardRow'

export default {
  props: ['cards'],
  components: {CardRow}
}
</script>

<style lang="css">
</style>
