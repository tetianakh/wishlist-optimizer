<template lang="html">
  <page>
    <div class="wrapper">
      <div class="google-btn" v-if="!authenticated" @click="onLogIn('google')">
        <div class="google-icon-wrapper">
          <img class="google-icon" src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg"/>
        </div>
        <p class="btn-text"><b>Sign in with google</b></p>
      </div>
    </div>
  </page>
</template>

<script>
import Page from './Page'

export default {
  components: {
    Page
  },
  computed: {
    authenticated () {
      return this.$store.state.token !== null
    }
  },
  methods: {
    onLogIn (provider) {
      this.$auth.authenticate(provider).then((authResponse) => {
        const token = authResponse.data.token
        this.$store.dispatch('logIn', {token}).then(() => {
          this.$router.push({name: 'Home'})
        })
      }).catch(e => {
        console.error(e)
        this.$store.dispatch('logOut')
      })
    }
  }
}
</script>

<style lang="scss">

$white: #fff;
$google-blue: #4285f4;
$button-active-blue: #1669F2;

.wrapper {
  text-align: center;
}

.google-btn {
  width: 184px;
  height: 42px;
  background-color: $white;
  border-radius: 2px;
  box-shadow: 0 3px 4px 0 rgba(0,0,0,.25);
  text-align: center;
  cursor: pointer;
  margin-top: 100px;
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
