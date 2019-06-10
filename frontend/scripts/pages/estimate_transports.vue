<template>
  <div>

    <div class="test">
      <h2>Transports</h2>

      <UploadSheet ref="uploaded_transports" :columns='{"from_address": "Address from", "to_address": "Address to", "name": "Name"}' />
    </div>

    <b-table ref="table_main" :fields="transports_fields" striped primary-key="id" v-if="$parent.project.transports" :items="$parent.project.transports">

      <template slot="roundtrip" slot-scope="row">
        <input type="checkbox" v-model="row.item.roundtrip" />
      </template>

      <template slot="from_address" slot-scope="row">
        <AddressField v-model="row.item.from_address" />
      </template>

      <template slot="to_address" slot-scope="row">
        <AddressField v-model="row.item.to_address" />
      </template>

      <template slot="name" slot-scope="row">
        <b-input v-model="row.item.name" class="project_transport_name" />
      </template>

      <template slot="mode" slot-scope="row">
        <b-form-select v-model="row.item.mode" :options="$OPENFOOTPRINT_GLOBAL.transport_modes" />
      </template>

      <template slot="actions" slot-scope="row">
        <b-button @click="deleteRow(row)" ><v-icon name="trash" /></b-button>
      </template>

    </b-table>

    <b-button @click="deleteAllTransports()">Delete all transports</b-button>
    <b-button @click="addTransportsFromPeople()">Add transports from people</b-button>
    <b-button @click="addRow()">Add transport</b-button>
    <b-button @click="saveAll()">Save all</b-button>

  </div>
</template>


<script>

import UploadSheet from "../components/uploadsheet"
import AddressField from "../components/addressfield"
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
          "key": "from_address",
          "label": "From"
        },
        {
          "key": "to_address",
          "label": "To"
        },
        {
          "key": "mode",
          "label": "Mode"
        },
        {
          "key": "roundtrip",
          "label": "Roundtrip?"
        },
        {
          "key": "actions",
          "label": "Actions"
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
    addRow() {
      this.$parent.project.transports.push({"id": "new_"+Math.random(), "from_address": {}, "to_address": {}});
      Vue.nextTick(() => {
        var newInput = this.$refs.table_main.$el.querySelector("tr:last-child input[type=text]");
        if (newInput) newInput.focus();
      });
    },
    deleteRow(row) {
      this.$refs.table_main.items.splice(row.index,1);
    },
    deleteAllTransports() {
      // TODO loading
      this.$http.post("/api/project/"+this.$parent.project.id+"/delete_transports").then((response) => {
        this.$parent.refreshProject();
      });
    },
    saveAll() {
      this.$http.post("/api/project/"+this.$parent.project.id+"/set_transports", this.$refs.table_main.items).then((response) => {
        this.$parent.refreshProject();
      });
    },
    addTransportsFromPeople() {
      this.$http.post("/api/project/"+this.$parent.project.id+"/add_transports_from_people").then((response) => {
        this.$parent.refreshProject();
      });
    }
  },
  components: {
    UploadSheet,
    AddressField
  }
}
</script>

<style lang="scss" scoped>

  h2 {
    float: left;
  }

</style>