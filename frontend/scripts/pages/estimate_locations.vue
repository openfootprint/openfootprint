<template>
  <div>
    <div class="btns_actions">
      <h2>Locations</h2>
      <div class="btns">
        <b-button @click="saveAll()" variant="save">Save <b-spinner v-if="loading_save" small type="grow" /></b-button>
      </div>
      <div class="clearfix"></div>
    </div>

    <DataTable ref="table_main" :fields="locations_fields" collection="locations" :newitemtemplate='{}' />

 </div>
</template>


<script>

import DataTable from "../components/datatable"
import Vue from 'vue'

export default {
  data () {
    return {
      loading_save: false,
      locations_fields: [
        {
          "key": "name",
          "label": "Name"
        },
        {
          "key": "address_source_name",
          "label": "Address"
        },
        {
          "key": "is_default",
          "label": "Default",
          "class": "th_checkbox"
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