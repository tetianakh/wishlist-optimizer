<template lang="html">
  <b-navbar toggleable="md" type="light" fixed=top class="header">

    <b-navbar-brand>
      <img src="/static/logo.png" alt="Logo" height="40" width="40" id="imglogo">
    </b-navbar-brand>

    <b-collapse is-nav id="nav_collapse">
      <b-navbar-nav>
        <b-nav-item><router-link to="/" class='link'>Wishlists</router-link></b-nav-item>
        <b-nav-item><router-link to="/draft" class='link'>Unsaved</router-link></b-nav-item>
      </b-navbar-nav>
    </b-collapse>

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

.header {
  background-color: #AA7251;
}

#imglogo {
  -webkit-filter: drop-shadow(1px 1px 1px rgba(0,0,0,0.8));
  filter: drop-shadow(1px 1px 1px  rgba(0,0,0,1));
}

.link:hover {
    text-decoration: underline;
    color: #fff;
}
</style>
