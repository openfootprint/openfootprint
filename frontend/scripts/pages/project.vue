<template>
  <div class="admin_project_page">

    <b-nav class="ofp-sidebar">
      <a href="/" class="logo"><img src="../../images/logo_openfootprint_vertical.svg" alt="Logo OpenFootprint"></a>

      <b-nav-item :to='{"name": "project_home"}' active>Dashboard</b-nav-item>
      <b-nav-item>Estimate</b-nav-item>
      <b-nav-item>Employees</b-nav-item>
      <b-nav-item>Offices</b-nav-item>
      <b-nav-item>Reports</b-nav-item>
      <b-nav-item :to='{"name": "project_settings"}'>Settings</b-nav-item>

      <div>
        <b-button @click="computeFootprint()"><b-spinner v-if="loading_footprint" small type="grow" /> Compute footprint</b-button>

        <div v-if="total_co2e">
          Total footprint: {{total_co2e}} gCO2e
          <a v-if="footprint_id" :href="'/report/'+footprint_id+'/'" target="_blank">Report</a>
        </div>
     </div>

    </b-nav>

    <div class="ofp-content">
      <h1>{{project.kind}}: <b-link :to='{"name": "project_home"}'>{{project.name}}</b-link></h1>

      <router-view v-if="!loading_footprint" />

   </div>
  </div>
</template>

<script>

export default {
  data () {
    return {
      loading_footprint: false,
      project: {},
      total_co2e: false,
      footprint_id:false
    };
  },
  created() {
    this.refreshProject();
  },
  methods: {
    refreshProject() {
      // TODO loading
      this.$http.get("/api/project/"+this.$route.params.id).then((response) => {
        this.project = response.data;
        console.log(this.project);
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