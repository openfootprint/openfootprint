<template>
  <div class="admin_project_page">

    <nav class="ofp_sidebar">
      <a href="/" class="logo"><img src="../../images/logo_openfootprint_vertical.svg" alt="Logo OpenFootprint"></a>

        <ul>
          <b-nav-item :to='{"name": "project_home"}' active>Dashboard<span class="active_bar"></span></b-nav-item>
          <b-nav-item>Estimate<span class="active_bar"></span></b-nav-item>
          <b-nav-item>Employees<span class="active_bar"></span></b-nav-item>
          <b-nav-item>Offices<span class="active_bar"></span></b-nav-item>
          <b-nav-item>Reports<span class="active_bar"></span></b-nav-item>
          <b-nav-item :to='{"name": "project_settings"}'>Settings<span class="active_bar"></span></b-nav-item>

          <div>
            <b-button @click="computeFootprint()"><b-spinner v-if="loading_footprint" small type="grow" /> Compute footprint</b-button>

            <div v-if="total_co2e">
              Total footprint: {{total_co2e}} gCO2e
              <a v-if="footprint_id" :href="'/report/'+footprint_id+'/'" target="_blank">Report</a>
            </div>
        </div>
      </ul>
    </nav>

    <div class="ofp_content">
      <div class="right_header">
        <div class="right_header_c">
          <p>
            <b-link :to='{"name": "project_home"}'>{{project.name}}</b-link>
            <span class="icon" v-if="project.kind === 'event'">E</span>
            <span class="icon" v-if="project.kind === 'company'">C</span>
            <span class="icon" v-if="project.kind === 'household'">H</span>
            </p>
        </div>
      </div>

      <div class="main_content_right">
        <router-view v-if="!loading_footprint" />
      </div>
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
  // .nav-link[data-toggle].collapsed:after {
  //     content: "▾";
  // }
  // .nav-link[data-toggle]:not(.collapsed):after {
  //     content: "▴";
  // }

  .ofp_sidebar {
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
      display: block;

      img {
        width:60%;
        height:auto;
        margin:0px auto;
        display: block;
        padding:30px 0px;
      }
    }

    ul {
      margin:0px;
      padding:0px;

      li {
        list-style: none;
        border-bottom:2px solid #FFF;

        a {
          color:$gray-700;
          padding:20px 20px 20px 25px;
          text-transform: uppercase;
          font-weight: bold;
          position: relative;

          &.active {
            color:$blue;

            .active_bar {
              position: absolute;
              height:100%;
              width:5px;
              background-color:$blue;
              display: block;
              top:0px;
              left:0px;
            }
          }

          &:hover {
            color:$blue;
          }
        }
      }
    }
  }

  .ofp_content {
    width: 100%;
    padding: 0 0 130px 300px;

    .right_header {
      height: 70px;
      background-color: #fff;
      border-bottom: 1px solid $gray-200;
      display: table;
      width: 100%;
      position: fixed;
      z-index: 10;
      width: -webkit-calc(100% - 300px);
      width: -moz-calc(100% - 300px);
      width: calc(100% - 300px);

      .right_header_c {
        width:90%;
        margin:0 auto;
        display: flex;
        align-items: center;
        height:100%;

        p {
          margin:0px;
          font-size:1.5rem;
          font-weight: bold;

          a {
            color:$black;
          }
        }
      }
    }

    .main_content_right {
      width: 90%;
      margin: 0 auto;
      padding-top: 120px;
    }

  }
</style>