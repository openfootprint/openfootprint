<template>
  <div class="admin_project_page">

    <b-nav class="ofp-sidebar">
      <a href="#" class="logo"><img src="../../images/logo_openfootprint_vertical.svg" alt="Logo OpenFootprint"></a>

      <b-nav-item active>Dashboard</b-nav-item>
      <b-nav-item>Estimate</b-nav-item>
      <b-nav-item>Employees</b-nav-item>
      <b-nav-item>Offices</b-nav-item>
      <b-nav-item>Reports</b-nav-item>
      <b-nav-item>Settings</b-nav-item>
    </b-nav>

    <div class="ofp-content">
      <h1>{{project.kind}}: {{project.name}}</h1>

      <button @click="computeFootprint()"><b-spinner v-if="loading_footprint" small type="grow" /> Compute footprint</button>

      <div v-if="total_co2e">
        Total footprint: {{total_co2e}} gCO2e
        <a v-if="footprint_id" :href="'/report/'+footprint_id+'/'" target="_blank">Report</a>
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

  </div>
</template>

<script>

import UploadSheet from "../components/uploadsheet"

export default {
  data () {
    return {
      loading_footprint: false,
      project: {},
      total_co2e: false,
      footprint_id:false,

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
    computeFootprint() {
      this.loading_footprint = true;
      this.$http.post("/api/project/"+this.$route.params.id+"/footprint").then((response) => {
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

<style lang="scss" scoped>
  .nav-link[data-toggle].collapsed:after {
      content: "▾";
  }
  .nav-link[data-toggle]:not(.collapsed):after {
      content: "▴";
  }

  .ofp-sidebar {
    width: 300px;
    height: 100%;
    position: fixed;
    background: #fff;
    z-index: 2;
    background-color: #F3F7FA;

    .logo {
      width:100%;
      padding:0px;
      margin:0px;
      border-bottom:1px solid $white;
    }
  }

  .ofp-content {
    width: 100%;
    padding: 0 0 130px 300px;
  }
</style>