<template lang="html">
  <div class="">

    <navbar>
    </navbar>

    <div class="container">
      <slot></slot>
    </div>

  </div>
</template>

<script>
import Navbar from './Navbar'

export default {
  components: {Navbar}
}
</script>

<style lang="css">
  .hoverable {
    cursor: pointer;
  }

  .centered {
    display: flex;
    justify-content: center;
  }

  .margin {
    margin: 10px;
  }
</style>
