<template>
  <div class="admin_project_page">

    <nav class="ofp_sidebar">
      <b-link :to="{'name':'index'}" class="logo"><img src="../../images/logo_openfootprint_vertical.svg" alt="Logo OpenFootprint"></b-link>

        <ul>
          <b-nav-item :to='{"name": "project_home"}' active>Dashboard<span class="active_bar"></span></b-nav-item>
          <b-nav-item :to='{"name": "estimate_people"}' v-if="project.kind=='company'">Employees<span class="active_bar"></span></b-nav-item>
          <b-nav-item :to='{"name": "estimate_people"}' v-if="project.kind=='event'">Attendees<span class="active_bar"></span></b-nav-item>
          <b-nav-item :to='{"name": "estimate_transports"}' v-if="project.kind=='event'">Transports<span class="active_bar"></span></b-nav-item>
          <b-nav-item :to='{"name": "estimate_extras"}' v-if="project.kind=='event'">Extras<span class="active_bar"></span></b-nav-item>
          <b-nav-item :to='{"name": "estimate_locations"}'>Locations<span class="active_bar"></span></b-nav-item>

          <b-nav-item v-if="project.kind=='company'">Offices<span class="active_bar"></span></b-nav-item>
          <b-nav-item>Reports<span class="active_bar"></span></b-nav-item>
          <b-nav-item :to='{"name": "project_settings"}'>Settings<span class="active_bar"></span></b-nav-item>

          <div>
            <b-button @click="computeFootprint()" class="compute_footprint"><b-spinner v-if="loading_footprint" small type="grow" /> Compute footprint</b-button>

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
            <span class="icon" v-if="project.kind === 'event'"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M9,10a1,1,0,0,0-1,1v2a1,1,0,0,0,2,0V11A1,1,0,0,0,9,10Zm12,1a1,1,0,0,0,1-1V6a1,1,0,0,0-1-1H3A1,1,0,0,0,2,6v4a1,1,0,0,0,1,1,1,1,0,0,1,0,2,1,1,0,0,0-1,1v4a1,1,0,0,0,1,1H21a1,1,0,0,0,1-1V14a1,1,0,0,0-1-1,1,1,0,0,1,0-2ZM20,9.18a3,3,0,0,0,0,5.64V17H10a1,1,0,0,0-2,0H4V14.82A3,3,0,0,0,4,9.18V7H8a1,1,0,0,0,2,0H20Z"/></svg></span>
            <span class="icon" v-if="project.kind === 'company'"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19,6.5H16v-1a3,3,0,0,0-3-3H11a3,3,0,0,0-3,3v1H5a3,3,0,0,0-3,3v9a3,3,0,0,0,3,3H19a3,3,0,0,0,3-3v-9A3,3,0,0,0,19,6.5Zm-9-1a1,1,0,0,1,1-1h2a1,1,0,0,1,1,1v1H10Zm10,13a1,1,0,0,1-1,1H5a1,1,0,0,1-1-1V13a21.27,21.27,0,0,0,3,.94v.59a1,1,0,0,0,2,0v-.21a23,23,0,0,0,3,.21,23,23,0,0,0,3-.21v.21a1,1,0,0,0,2,0v-.59A21.27,21.27,0,0,0,20,13Zm0-7.69a20.39,20.39,0,0,1-3,1V11.5a1,1,0,0,0-2,0v.74a20.11,20.11,0,0,1-6,0V11.5a1,1,0,0,0-2,0v.33a20.39,20.39,0,0,1-3-1V9.5a1,1,0,0,1,1-1H19a1,1,0,0,1,1,1Z"/></svg></span>
            <span class="icon" v-if="project.kind === 'household'"><svg xmlns="http://www.w3.org/2000/svg" data-name="Layer 1" viewBox="0 0 24 24"><path d="M14,8h1a1,1,0,0,0,0-2H14a1,1,0,0,0,0,2Zm0,4h1a1,1,0,0,0,0-2H14a1,1,0,0,0,0,2ZM9,8h1a1,1,0,0,0,0-2H9A1,1,0,0,0,9,8Zm0,4h1a1,1,0,0,0,0-2H9a1,1,0,0,0,0,2Zm12,8H20V3a1,1,0,0,0-1-1H5A1,1,0,0,0,4,3V20H3a1,1,0,0,0,0,2H21a1,1,0,0,0,0-2Zm-8,0H11V16h2Zm5,0H15V15a1,1,0,0,0-1-1H10a1,1,0,0,0-1,1v5H6V4H18Z"/></svg></span>
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
        response.data.locations.forEach((loc) => {
          loc.address_source_name = (loc.address||{}).source_name;
        });
        this.project = response.data;
        console.log(this.project);
      });
    },
    computeFootprint() {
      this.loading_footprint = true;
      this.$http.post("/api/project/"+this.project.id+"/footprint").then((response) => {
        this.loading_footprint = false;
        console.log(response);
        this.total_co2e = response.data.footprint || 0;
        this.footprint_id = response.data.footprint_id;
      });
    }
  },
  components: {
  }
}
</script>

<style lang="scss" scoped>
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

    .compute_footprint {
      margin-left: 25px;
      margin-top: 20px;
      width: calc(100% - 50px);
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

          .icon {
            display:inline-block;
            height:20px;
            width:30px;
            svg {
              max-height:20px;
              width:auto;
              fill:$gray-500;
            }
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