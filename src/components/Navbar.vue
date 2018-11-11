<template lang="html">
  <b-navbar toggleable="md" type="dark" variant="info" fixed=top>
    <b-navbar-brand>
      <router-link to="/" class='link'>Wishlists</router-link>
    </b-navbar-brand>
    <b-navbar-nav class="ml-auto">
      <!-- <div id="google-signin-button" v-if="!authenticated"></div> -->
      <!-- <div class="g-signin2" :data-onsuccess="onLogIn"></div> -->
      <button @click="onLogIn('google')" class='btn'>Google Sign In</button>
      <a href="#" @click="onLogOut" class="link">Log out</a>
    </b-navbar-nav>
  </b-navbar>
</template>

<script>
export default {
  computed: {
    authenticated () {
      return this.$store.state.user !== null
    }
  },
  mounted () {
    // gapi.load('auth2', () => {
    //   gapi.auth2.init()
    // })
    // this.renderSignInButton()
  },
  methods: {
    renderSignInButton () {
      // gapi.signin2.render('google-signin-button', {onsuccess: this.onSignIn})
    },
    onLogIn (provider) {
      // const profile = user.getBasicProfile()
      this.$auth.authenticate(provider).then(function (authResponse) {
        console.log(authResponse)
        this.$store.commit('logIn', {user: authResponse})
        // Execute application logic after successful social authentication
      })
    },
    onLogOut () {
      // const auth2 = gapi.auth2.getAuthInstance()
      // auth2.signOut().then(() => {
      //   this.$store.commit('logOut')
      //   console.log(this.$store.state.user)
      //   console.log(this.authenticated)
      //   this.renderSignInButton()
      //   console.log('User signed out.')
      // })
      this.$auth.logout().then(() => this.$store.commit('logOut'))
    }
  }
}
</script>

<style lang="css">
.link {
  color: #fff;
}
</style>
