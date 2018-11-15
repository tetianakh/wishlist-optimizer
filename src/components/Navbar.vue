<template lang="html">
  <b-navbar toggleable="md" type="dark" variant="info" fixed=top>

    <b-navbar-brand>
      <router-link to="/" class='link'>Wishlists</router-link>
    </b-navbar-brand>

    <b-navbar-nav class="ml-auto">
      <a href='#' v-if="!authenticated" @click="onLogIn" class="link">Log in</a>
      <a href='#' v-else @click="onLogOut" class="link">Log out</a>
    </b-navbar-nav>

  </b-navbar>
</template>

<script>
import eventBus from '../EventBus'
import tokenStore from '../store/token'

export default {
  mounted () {
    this.eventBus = eventBus
  },
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
