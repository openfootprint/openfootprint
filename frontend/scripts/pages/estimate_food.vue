<template>
  <div>
    <h2>Food</h2>

    <DataTable ref="table_main" :fields="food_fields" collection="meals" :newitemtemplate='{}' />

  </div>
</template>


<script>

import DataTable from "../components/datatable"
import Vue from 'vue'

export default {
  data () {
    return {

      food_fields: [
        {
          "key": "name",
          "label": "Name"
        },
        {
          "key": "mass",
          "label": "Mass (in grams)"
        },
        {
          "key": "actions",
          "label": "",
          "class": "th_actions"
        }
      ]
    };
  },
  methods: {
  },
  components: {
    DataTable
  }
}
</script>

<style lang="scss" scoped>

</style>