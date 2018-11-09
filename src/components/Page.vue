<template lang="html">
  <div class="">

    <b-navbar toggleable="md" type="dark" variant="info" fixed=top>
      <b-navbar-brand>
        <router-link to="/" class='brand'>Wishlists</router-link>
      </b-navbar-brand>
    </b-navbar>

    <div class="container">
      <slot></slot>
    </div>

  </div>
</template>

<script>
export default {}
</script>

<style lang="css" scoped>
  .hoverable {
    cursor: pointer;
  }

  .brand {
    color: #fff;
  }

  .centered {
    display: flex;
    justify-content: center;
  }

</style>
