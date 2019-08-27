<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import router from "./router";
import store from "./store";

export default {
  el: "#app",
  name: "App",
  router,
  store
};
</script>

<style></style>
