<template>
  <b-input :value="(value||{}).source_name||''" @input="onInput" />
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
 }
</style>