<template lang="html">
  <div class="sk-fading-circle">
    <div class="sk-circle1 sk-circle"></div>
    <div class="sk-circle2 sk-circle"></div>
    <div class="sk-circle3 sk-circle"></div>
    <div class="sk-circle4 sk-circle"></div>
    <div class="sk-circle5 sk-circle"></div>
  </div>
</template>

<script>
export default {
}
</script>

<style lang="css">
.sk-fading-circle {
  margin: 100px auto;
  width: 120px;
  height: 120px;
  position: relative;
}

.sk-fading-circle .sk-circle {
  width: 100%;
  height: 100%;
  position: absolute;
  left: 0;
  top: 0;
}

.sk-fading-circle .sk-circle:before {
  content: '';
  display: block;
  margin: 0 auto;
  width: 22%;
  height: 22%;
  border-radius: 100%;
  -webkit-animation: sk-circleFadeDelay 1s infinite ease-in-out both;
          animation: sk-circleFadeDelay 1s infinite ease-in-out both;
}

.sk-fading-circle .sk-circle2 {
  -webkit-transform: rotate(72deg);
      -ms-transform: rotate(72deg);
          transform: rotate(72deg);
}
.sk-fading-circle .sk-circle3 {
  -webkit-transform: rotate(144deg);
      -ms-transform: rotate(144deg);
          transform: rotate(144deg);
}
.sk-fading-circle .sk-circle4 {
  -webkit-transform: rotate(216deg);
      -ms-transform: rotate(216deg);
          transform: rotate(216deg);
}
.sk-fading-circle .sk-circle5 {
  -webkit-transform: rotate(288deg);
      -ms-transform: rotate(288deg);
          transform: rotate(288deg);
}


.sk-fading-circle .sk-circle1:before {
  background-color: #CDC9AD;  /* W */
  background: radial-gradient(circle at 50% 50%, #D5D5B9, #A59E83);
}

.sk-fading-circle .sk-circle2:before {
  background-color: #619EB7; /* U */
  background: radial-gradient(circle at 50% 50%, #82C2E7, #326A89);
  -webkit-animation-delay: -0.8s;
          animation-delay: -0.8s;
}
.sk-fading-circle .sk-circle3:before {
  background-color: #524443; /* B */
  background: radial-gradient(farthest-corner, #C4B5B8, #372A30);
  -webkit-animation-delay: -0.6s;
          animation-delay: -0.6s;
}
.sk-fading-circle .sk-circle4:before {
  background-color: #B05D56; /* R */
  background: radial-gradient(farthest-corner, #D0736F, #98413D);
  -webkit-animation-delay: -0.4s;
          animation-delay: -0.4s;
}
.sk-fading-circle .sk-circle5:before {
  background-color: #8FA85D; /* G */
  background: radial-gradient(farthest-corner, #B8D37E, #66883F);
  -webkit-animation-delay: -0.2s;
          animation-delay: -0.2s;
}

@-webkit-keyframes sk-circleFadeDelay {
  0%, 10%, 90%, 100% { opacity: 0; }
  50% { opacity: 1; }
}

@keyframes sk-circleFadeDelay {
  0%, 10%, 90%, 100% { opacity: 0; }
  50% { opacity: 1; }
}
</style>
