<template lang="html">
  <div class="footer">
    <p>© Foki {{ currentYear }}&nbsp;&nbsp;|&nbsp;&nbsp;<font-awesome-icon :icon="['fab', 'github']"/>
      Find us on <a href="https://github.com/tetianakh/wishlist-optimizer" target="_blank">github</a></p>
  </div>
</template>

<script>
export default {
  computed: {
    currentYear () {
      return (new Date()).getFullYear()
    }
  }
}
</script>

<style lang="css">
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    font-size: 0.8em;
    background-color: #F5F5F5;
    text-shadow: 1px 1px #ffffff;
    padding-top: 10px;
}
</style>
