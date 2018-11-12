<template lang="html">
  <b-navbar toggleable="md" type="dark" variant="info" fixed=top>

    <b-navbar-brand>
      <router-link to="/" class='link'>Wishlists</router-link>
    </b-navbar-brand>

    <b-navbar-nav class="ml-auto">
      <div class="google-btn" v-if="!authenticated" @click="onLogIn('google')">
        <div class="google-icon-wrapper">
          <img class="google-icon" src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg"/>
        </div>
        <p class="btn-text"><b>Sign in with google</b></p>
      </div>
      <a href='#' v-else @click="onLogOut" class="link">Log out</a>
    </b-navbar-nav>

  </b-navbar>
</template>

<script>
export default {
  computed: {
    authenticated () {
      return this.$store.state.token !== null
    }
  },
  methods: {
    onLogIn (provider) {
      this.$auth.authenticate(provider).then((authResponse) => {
        const token = authResponse.data.token
        this.$store.dispatch('logIn', {token: token})
      }).catch(e => console.error(e))
    },
    onLogOut () {
      this.$auth.logout().then(() => {
        this.$store.dispatch('logOut')
      }).catch(e => console.error(e.message))
    }
  }
}
</script>

<style lang="scss">
.link {
  color: #fff;
}

$white: #fff;
$google-blue: #4285f4;
$button-active-blue: #1669F2;

.google-btn {
  width: 184px;
  height: 42px;
  background-color: $white;
  border-radius: 2px;
  box-shadow: 0 3px 4px 0 rgba(0,0,0,.25);
  text-align: center;
  cursor: pointer;
  .google-icon-wrapper {
    position: absolute;
    margin-top: 1px;
    margin-left: 0px;
    width: 40px;
    height: 40px;
    border-radius: 2px;
    background-color: $white;
  }
  .google-icon {
    position: absolute;
    margin-top: 11px;
    margin-left: 0px;
    width: 18px;
    height: 18px;
  }
  .btn-text {
    float: right;
    margin: 11px 20px 0 0;
    color: $google-blue;
    font-size: 14px;
    letter-spacing: 0.2px;
    font-family: "Roboto";
  }
  &:hover {
    box-shadow: 0 0 6px $google-blue;
  }
  &:active {
    background: $button-active-blue;
  }
}

@import url(https://fonts.googleapis.com/css?family=Roboto:400);

</style>
