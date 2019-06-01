<template>
  <div>
    <h1>{{project.kind}}: {{project.name}}</h1>

    <button @click="computeFootprint()"><b-spinner v-if="loading_footprint" small type="grow" /> Compute footprint</button>

    <div v-if="total_co2e">
      Total footprint: {{total_co2e}} gCO2e
      <a v-if="footprint_id" :href="'/report/'+footprint_id+'/'" target="_blank">Report</a>
    </div>

    <h2>Transports</h2>
    <UploadSheet ref="uploaded_transports" :columns='{"from_address": "Address from", "to_address": "Address to", "country": "Country", "name": "Name"}' />

    <b-table ref="table_transports" :fields="transports_fields" striped primary-key="id" v-if="project.transports" :items="project.transports">

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

    <button @click="deleteAllTransports()">Delete all transports</button>

    <h2>Extras</h2>
    <b-table ref="table_extras" class="project_extras" :fields="extras_fields" striped primary-key="id" v-if="project.extras" :items="project.extras">

      <template slot="name" slot-scope="row">
        <b-input v-model="row.item.name" class="project_extras_name" />
      </template>

      <template slot="kind" slot-scope="row">
        <b-form-select v-model="row.item.kind" :options="extras_kinds"></b-form-select>
      </template>

      <template slot="params" slot-scope="row">
        <b-input v-model="row.item.param_f1" />
      </template>

      <template slot="actions" slot-scope="row">
        <b-button @click="deleteExtra(row)" ><v-icon name="trash" /></b-button>
      </template>
    </b-table>

    <button @click="addExtra()">Add extra</button>
    <button @click="saveExtras()">Save extras</button>

  </div>
</template>

<script>

import UploadSheet from "../components/uploadsheet"
import Vue from 'vue'

export default {
  data () {
    return {
      loading_footprint: false,
      project: {},
      total_co2e: false,
      footprint_id:false,

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
      ],
      extras_fields: [
        {
          "key": "name",
          "label": "Name"
        },
        {
          "key": "kind",
          "label": "Type"
        },
        {
          "key": "params",
          "label": "Parameters"
        },
        {
          "key": "actions",
          "label": "Actions"
        }
      ],

      // TODO get these values directly from the Django model?
      extras_kinds: [
        {
          "value": "co2e",
          "text":"Raw CO2e in grams"
        },
        {
          "value": "wh",
          "text":"Watt hours"
        }
      ]
    };
  },
  created() {
    this.refreshProject();
  },

  mounted() {
    this.$refs.uploaded_transports.$on("data", (data) => {
      // TODO loading (https://bootstrap-vue.js.org/docs/components/table#table-busy-state)
      this.$http.post("/api/project/"+this.project.id+"/set_transports", data).then((response) => {
        this.refreshProject();
      });
    })
  },
  methods: {
    addExtra() {
      this.project.extras.push({"kind": "co2e", "id": "new_"+Math.random()});
      Vue.nextTick(() => {
        var newInput = document.querySelector("table.project_extras tr:last-child input.project_extras_name");
        if (newInput) newInput.focus();
      });
    },
    deleteExtra(row) {
      this.project.extras.splice(row.index,1);
    },
    saveExtras() {
      this.$http.post("/api/project/"+this.project.id+"/set_extras", this.project.extras).then((response) => {
        this.refreshProject();
      });
    },
    refreshProject() {
      // TODO loading
      this.$http.get("/api/project/"+this.$route.params.id).then((response) => {
        this.project = response.data;
        console.log(this.project);
      });
    },
    deleteAllTransports() {
      // TODO loading
      this.$http.post("/api/project/"+this.project.id+"/delete_transports").then((response) => {
        this.refreshProject();
      });
    },
    computeFootprint() {
      this.loading_footprint = true;
      this.$http.post("/api/project/"+this.project.id+"/footprint").then((response) => {
        this.loading_footprint = false;
        console.log(response);
        this.total_co2e = response.data.result.f.co2e;
        this.footprint_id = response.data.footprint_id;
      });
    }
  },
  components: {
    UploadSheet
  }
}
</script>

<style scoped>

</style>