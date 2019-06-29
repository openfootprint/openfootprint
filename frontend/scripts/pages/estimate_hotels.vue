<template>
  <div>
    <h2>Hotel nights</h2>

    <DataTable ref="table_main" :fields="hotels_fields" collection="hotels" :newitemtemplate='{}' />

  </div>
</template>


<script>

import DataTable from "../components/datatable"
import Vue from 'vue'

export default {
  data () {
    return {

      hotels_fields: [
        {
          "key": "name",
          "label": "Name"
        },
        {
          "key": "address",
          "label": "Address"
        },
        {
          "key": "starts_at",
          "label": "Check-in"
        },
        {
          "key": "ends_at",
          "label": "Check-out"
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