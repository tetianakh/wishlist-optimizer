<template lang="html">
  <div class="">

    <navbar>
    </navbar>

    <div class="container">
      <slot></slot>
    </div>

    <wo-footer>
    </wo-footer>
  </div>

</template>

<script>
import Navbar from './Navbar'
import WoFooter from './Footer'

export default {
  components: { Navbar, WoFooter }
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
