<template>
  <div>

    <div class="test">
      <h2>Transports</h2>
      
      <UploadSheet ref="uploaded_transports" :columns='{"from_address": "Address from", "to_address": "Address to", "country": "Country", "name": "Name"}' />
    </div>

    <b-table ref="table_transports" :fields="transports_fields" striped primary-key="id" v-if="$parent.project.transports" :items="$parent.project.transports">

      <template slot="roundtrip" slot-scope="row">
        <input type="checkbox" v-model="row.roundtrip" />
      </template>

      <template slot="from_location" slot-scope="row">
        {{row.value.source_name}}
      </template>

      <template slot="to_location" slot-scope="row">
        {{row.value.source_name}}
      </template>

    </b-table>

    <b-button @click="deleteAllTransports()">Delete all transports</b-button>

  </div>
</template>


<script>

import UploadSheet from "../components/uploadsheet"
import Vue from 'vue'

export default {
  data () {
    return {

      transports_fields: [
        {
          "key": "name",
          "label": "Name"
        },
        {
          "key": "from_location",
          "label": "From"
        },
        {
          "key": "to_location",
          "label": "To"
        },
        {
          "key": "roundtrip",
          "label": "Roundtrip?"
        }
      ]
    };
  },
  mounted() {
    this.$refs.uploaded_transports.$on("data", (data) => {
      // TODO loading (https://bootstrap-vue.js.org/docs/components/table#table-busy-state)
      this.$http.post("/api/project/"+this.$parent.project.id+"/set_transports", data).then((response) => {
        this.$parent.refreshProject();
      });
    });
  },
  methods: {
    deleteAllTransports() {
      // TODO loading
      this.$http.post("/api/project/"+this.$parent.project.id+"/delete_transports").then((response) => {
        this.$parent.refreshProject();
      });
    }
  },
  components: {
    UploadSheet
  }
}
</script>

<style lang="scss" scoped>

  h2 {
    float: left;
  }
  
</style>