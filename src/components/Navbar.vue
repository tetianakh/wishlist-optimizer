<template lang="html">
  <b-navbar toggleable="md" type="dark" variant="info" fixed=top>

    <b-navbar-brand>
      <router-link to="/" class='link'>Wishlists</router-link>
    </b-navbar-brand>

    <b-navbar-nav class="ml-auto">
      <a href='#' v-if="!authenticated && $router.history.current.name !== 'Login'" @click="onLogIn" class="link">Log in</a>
      <a href='#' v-if="authenticated" @click="onLogOut" class="link">Log out</a>
    </b-navbar-nav>

  </b-navbar>
</template>

<script>
import tokenStore from '../store/token'

export default {
  computed: {
    authenticated () {
      return tokenStore.isAuthenticated()
    }
  },
  methods: {
    onLogIn () {
      this.$router.push({'name': 'Login'})
    },
    onLogOut () {
      tokenStore.logOut()
      this.$auth.logout()
      location.reload()
    }
  }
}
</script>

<style lang="css">
.link {
  color: #fff;
}

</style>
