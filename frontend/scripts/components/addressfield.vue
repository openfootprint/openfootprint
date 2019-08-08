<template>
  <div :class='"status-"+((value||{}).status||"empty")'>
    <!-- {{(value||{}).country}} -->
    <b-input :value="(value||{}).source_name||''" @input="onInput" />
  </div>
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
 .status-new input {
   border:1px solid red !important;
 }
 .status-empty input {
   border:1px solid blue !important;
 }
 .status-geocoded {
 }
</style>