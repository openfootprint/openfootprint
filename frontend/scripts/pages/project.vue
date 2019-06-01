<template>
  <div>
    <h1>{{project.kind}}: {{project.name}}</h1>

    <button @click="estimate()"><b-spinner v-if="loading_estimate" small type="grow" /> Estimate</button>

    <div v-if="total_co2e">
      Total footprint: {{total_co2e}} gCO2e
      <a v-if="estimate_id" :href="'/report/'+estimate_id+'/'" target="_blank">Report</a>
    </div>

    <h2>Transports</h2>
    <UploadSheet ref="uploaded_transports" :columns='{"from_address": "Address from", "to_address": "Address to", "country": "Country", "name": "Name"}' />

    <b-table :fields="transport_fields" striped primary-key="id" v-if="project.transports" :items="project.transports">

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
    <ul v-for="extra in project.extras">
      <li>{{extra.name}}</li>
    </ul>

  </div>
</template>

<script>

import UploadSheet from "../components/uploadsheet"

export default {
  data () {
    return {
      loading_estimate: false,
      project: {},
      total_co2e: false,
      estimate_id:false,

      transport_fields: [
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
    }
  },
  created() {
    this.refreshProject();
  },

  mounted() {
    this.$refs.uploaded_transports.$on("data", (data) => {
      this.$http.post("/api/project/"+this.$route.params.id+"/set_transports", data).then((response) => {
        this.refreshProject();
      });
    })
  },
  methods: {
    refreshProject() {
      // TODO loading
      this.$http.get("/api/project/"+this.$route.params.id).then((response) => {
        this.project = response.data;
      });
    },
    deleteAllTransports() {
      // TODO loading
      this.$http.post("/api/project/"+this.$route.params.id+"/delete_transports").then((response) => {
        this.refreshProject();
      });
    },
    estimate() {
      this.loading_estimate = true;
      this.$http.post("/api/project/"+this.$route.params.id+"/estimate").then((response) => {
        this.loading_estimate = false;
        console.log(response);
        this.total_co2e = response.data.result.f.co2e;
        this.estimate_id = response.data.estimate_id;
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