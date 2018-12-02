<template lang="html">
  <page>

  <img src="../assets/logo.png" alt="Logo" width="70px">

  <h3>Sign in to VampiricTutor</h3>
  <p>Signing in allows you to save your wishlists.</p>
    <div class="wrapper">
      <div>
        <b-alert variant="danger"
             dismissible
             :show="errorMessage !== null"
             @dismissed="errorMessage=null">
            {{ errorMessage }}
        </b-alert>
      </div>

      <div class="google-btn" v-if="!authenticated" @click="onLogIn('google')">
        <div class="google-icon-wrapper">
          <img class="google-icon" src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg"/>
        </div>
        <p class="btn-text"><b>Sign in with Google</b></p>
      </div>
    </div>

  </page>
</template>

<script>
import Page from './Page'
import tokenStore from '../store/token'
import draftStore from '../store/draft'

export default {
  components: {
    Page
  },
  data () {
    return {
      errorMessage: null
    }
  },
  computed: {
    authenticated () {
      return tokenStore.isAuthenticated()
    }
  },
  methods: {
    onLogIn (provider) {
      this.errorMessage = null
      this.$auth.authenticate(provider).then((authResponse) => {
        tokenStore.logIn(authResponse.data.token)
        if (draftStore.hasDraft()) {
          this.$router.push({ name: 'Draft' })
        } else {
          this.$router.push({ name: 'Home' })
        }
      }).catch(e => {
        console.error(e)
        this.errorMessage = 'Authentication failed'
        tokenStore.logOut()
      })
    }
  }
}
</script>

<style lang="scss">

$white: #fff;
$google-blue: #4285f4;
$button-active-blue: #1669F2;
$light-grey: #f9f9f9;
$dark-grey: #d8dee2;


h3 {
  margin-top: 40px;
}

.wrapper {
  width: 300px;
  text-align: center;
  background-color: $light-grey;
  border: 1px solid $dark-grey;
  margin: 0px auto 40px auto;
  border-radius: 5px;
  padding: 20px;
  margin-top: 20px;
}

.google-btn {
  // width: 184px;
  width: 203px;
  height: 42px;
  background-color: $white;
  border-radius: 2px;
  box-shadow: 0 3px 4px 0 rgba(0,0,0,.25);
  text-align: center;
  cursor: pointer;
  display: inline-block;
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
    font-weight: 400;
  }
  &:hover {
    box-shadow: 0 0 6px $google-blue;
  }
  &:active {
    background: $button-active-blue;
  }
}
</style>
