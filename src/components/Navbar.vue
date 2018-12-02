<template lang="html">
  <b-navbar toggleable="md" type="light" fixed=top class="header">

    <b-navbar-brand>
      <router-link to="/" >
        <img src="../assets/logo.png" alt="Logo" height="40" width="40" id="imglogo">
      </router-link>
    </b-navbar-brand>

    <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

    <b-collapse is-nav id="nav_collapse">
      <b-navbar-nav>
        <b-nav-item><router-link to="/" :class="getClasses('Home')" >Home</router-link></b-nav-item>
        <b-nav-item><router-link to="/draft" :class="getClasses('Draft')">
        {{ newWishlistLinkName }}</router-link></b-nav-item>
      </b-navbar-nav>

      <b-navbar-nav class="ml-auto">
        <a href='#' v-if="!authenticated" @click="onLogIn" :class="getClasses('Login')">Log in</a>
        <a href='#' v-if="authenticated" @click="onLogOut" :class="getClasses()">Log out</a>
      </b-navbar-nav>

    </b-collapse>

  </b-navbar>
</template>

<script>
import tokenStore from '../store/token'
import draftStore from '../store/draft'

export default {
  computed: {
    authenticated () {
      return tokenStore.isAuthenticated()
    },
    newWishlistLinkName () {
      if (draftStore.hasDraft()) {
        return "Unsaved Wishlist"
      }
      return "New Wishlist"
    }
  },
  methods: {
    onLogIn () {
      this.$router.push({ 'name': 'Login' })
    },
    onLogOut () {
      tokenStore.logOut()
      this.$auth.logout()
      location.reload()
    },
    getClasses (name) {
      const classes = { link: true }
      if (name === this.$router.history.current.name) {
        classes.active = true
      }
      return classes
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
    font-weight: bold;
    text-decoration: none;
    color: #fff;
}
.active {
  text-decoration: underline;
}
</style>
