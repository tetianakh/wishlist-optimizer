<template lang="html">
  <div class="spinner">
    <div class="bounce1"></div>
    <div class="bounce2"></div>
    <div class="bounce3"></div>
    <div class="bounce4"></div>
    <div class="bounce5"></div>
  </div>
</template>

<script>
export default {
}
</script>

<style lang="css">
.spinner {
  margin: 20px auto 0;
  width: 120px;
  text-align: center;
}

.spinner > div {
  width: 18px;
  height: 18px;
  /* background-color: #333; */

  border-radius: 100%;
  display: inline-block;
  -webkit-animation: sk-bouncedelay 1.4s infinite ease-in-out both;
  animation: sk-bouncedelay 1.4s infinite ease-in-out both;
}

.spinner .bounce1 {
  background-color: #CDC9AD;  /* W */
  -webkit-animation-delay: -0.32s;
  animation-delay: -0.32s;
}

.spinner .bounce2 {
  background-color: #619EB7; /* U */
  -webkit-animation-delay: -0.16s;
  animation-delay: -0.16s;
}

.spinner .bounce3 {
  background-color: #524443; /* B */
}

.spinner .bounce5 {
  background-color: #8FA85D; /* G */
  -webkit-animation-delay: 0.32s;
  animation-delay: 0.32s;
}

.spinner .bounce4 {
  background-color: #B05D56; /* R */
  -webkit-animation-delay: 0.16s;
  animation-delay: 0.16s;
}

@-webkit-keyframes sk-bouncedelay {
  0%, 80%, 100% { -webkit-transform: scale(0) }
  40% { -webkit-transform: scale(1.0) }
}

@keyframes sk-bouncedelay {
  0%, 80%, 100% {
    -webkit-transform: scale(0);
    transform: scale(0);
  } 40% {
    -webkit-transform: scale(1.0);
    transform: scale(1.0);
  }
}
</style>
