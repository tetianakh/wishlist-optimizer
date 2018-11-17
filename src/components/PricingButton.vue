<template lang="html">
  <div class="margin">
    <b-button
      variant="success"
      v-if="hasCards"
      @click="submitPricingJob">Get Pricing</b-button>
  </div>

</template>

<script>
import {CALCULATE_PRICING} from '../events'

export default {
  props: ['hasCards'],
  methods: {
    submitPricingJob () {
      this.$eventBus.$emit(CALCULATE_PRICING)
    }
  }
}
</script>

<style lang="css">
</style>
