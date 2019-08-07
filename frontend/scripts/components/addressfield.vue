<template>
  <b-input :class='{"geocoding":!(value||{latitude:1}).latitude}' :value="(value||{}).source_name||''" @input="onInput" />
</template>

<script>
export default {
  props: ['value'],
  methods: {
    onInput(value) {
      this.$emit("input", {"source_name": value});
    }
  }
}
</script>

<style lang="scss" scoped>
 input {
   padding-left:30px;
   // TODO add location icon
 }
 input.geocoding {
   border:1px solid red !important;
 }
</style>