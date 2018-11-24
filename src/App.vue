<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
@import '~vue-multiselect/dist/vue-multiselect.min.css';
@import 'https://fonts.googleapis.com/css?family=Lato';
@import 'https://fonts.googleapis.com/css?family=Roboto:400';

#app {
  font-family: 'Lato', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  text-align: center;
  margin-top: 100px;
}
</style>
