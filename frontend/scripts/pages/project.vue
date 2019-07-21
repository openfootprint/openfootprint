<template>
  <div class="admin_project_page">

    <nav class="ofp_sidebar">
      <b-link :to="{'name':'index'}" class="logo"><img src="../../images/logo_openfootprint_vertical.svg" alt="Logo OpenFootprint"></b-link>

        <ul>
          <b-nav-item :to='{"name": "project_home"}'><unicon name="home-alt" class="icon"></unicon>Dashboard</b-nav-item>
          <b-nav-item class="has_subcats">
            <unicon name="chart" class="icon"></unicon>Estimate
            <!--<span class="subtotal_item">10t</span>-->
            <ul class="ofp_siedebar_submenu">
              <b-nav-item :to='{"name": "estimate_locations"}'>Locations</b-nav-item>
              <b-nav-item :to='{"name": "estimate_people"}'>
                <span v-if="project.kind=='company'">Employees</span>
                <span v-if="project.kind=='event'">Attendees</span>
              </b-nav-item>
              <b-nav-item :to='{"name": "estimate_transports"}'>Transports</b-nav-item>
              <b-nav-item :to='{"name": "estimate_food"}'>Food</b-nav-item>
              <b-nav-item :to='{"name": "estimate_hotels"}'>Hotels</b-nav-item>
              <b-nav-item :to='{"name": "estimate_extras"}' v-if="project.kind=='event'">Extras</b-nav-item>
            </ul>
          </b-nav-item>
          <b-nav-item :to='{"name": "project_reports"}'><unicon name="chart-line" class="icon"></unicon>Reports</b-nav-item>
          <b-nav-item :to='{"name": "project_reports"}'>Reports</b-nav-item>
          <b-nav-item :to='{"name": "project_settings"}'><unicon name="cog" class="icon"></unicon>Settings</b-nav-item>
      </ul>

      <div class="profile_block">
        <!-- TODO -->
        <a href="#">
          <img src="../../images/logo_openfootprint_icon.svg" />
          <p>Log in to save</p>
        </a>
      </div>
    </nav>

    <div class="ofp_content">
      <div class="right_header">
        <div class="right_header_c">
          <p>
            <b-link :to='{"name": "project_home"}'>{{project.name}}</b-link>
            <span class="icon" v-if="project.kind === 'event'"><unicon name="ticket"></unicon></span>
            <span class="icon" v-if="project.kind === 'company'"><unicon name="briefcase-alt"></unicon></span>
            <span class="icon" v-if="project.kind === 'household'"><unicon name="building"></unicon></span>
          </p>
        </div>
        <div class="compute_block">
            <b-button @click="computeFootprint()" variant="primary" v-if="!total_co2e">Compute footprint <b-spinner v-if="loading_footprint" small type="grow" /></b-button>

            <div v-if="total_co2e" class="computed_footprint">
<<<<<<< HEAD
              <p>{{parseInt(total_co2e/100000,10)/10}} tons of CO2e <span @click="computeFootprint()" v-if="total_co2e"><unicon name="redo"></unicon></span></p>
              <a v-if="report_id" :href="'/report/'+report_id+'/'" target="_blank">View report</a>
=======
              <p>{{parseInt(total_co2e/100000,10)/10}} tons of CO2e <span @click="computeFootprint()" v-if="total_co2e"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M21,11a1,1,0,0,0-1,1,8.05,8.05,0,1,1-2.22-5.5h-2.4a1,1,0,0,0,0,2h4.53a1,1,0,0,0,1-1V3a1,1,0,0,0-2,0V4.77A10,10,0,1,0,22,12,1,1,0,0,0,21,11Z"/></svg></span></p>
              <a v-if="report_id" :href="'/reports/'+report_id+'/'" target="_blank">View report</a>
>>>>>>> 6a91fde67d7819dcfc57f5a11c423119bca7cde5
              |
              <a href="">Offset</a>
            </div>
        </div>
      </div>

      <div class="main_content_right">
        <router-view/>
      </div>
   </div>
  </div>
</template>

<script>
import Vue from 'vue'

export default {
  data () {
    return {
      loading_footprint: false,
      total_co2e: null,
      report_id: null
    };
  },
  created() {
    // TODO use vuex mutation
    this.$store.state.project = {
      "id": this.$route.params.project_id
    };
    this.refreshProject();
  },
  methods: {
    computeFootprint() {
      this.loading_footprint = true;
      this.$http.post("/api/project/"+this.project.id+"/footprint").then((response) => {
        this.loading_footprint = false;
        this.total_co2e = response.data.footprint || 0;
        this.report_id = response.data.report_id;
      });
    }
  },
  components: {
  }
}
</script>

<style lang="scss" scoped>
  .ofp_sidebar {
    width: 220px;
    height: 100%;
    position: fixed;
    background: #fff;
    z-index: 2;
    background-color: #F3F7FA;

    .logo {
      width:100%;
      padding:0px;
      margin:0px;
      display: block;

      img {
        width:60%;
        height:auto;
        margin:0px auto 30px;
        display: block;
        padding:30px 0px;
      }
    }

    ul {
      margin:0px;
      padding:0px;

      &:first-of-type {
        overflow-y:auto;
        height: -webkit-calc(100% - 156px);
        height: -moz-calc(100% - 156px);
        height: calc(100% - 156px);
        padding-bottom:75px;
      }

      li {
        list-style: none;

        a {
          color:$gray-700;
          padding:15px 20px 15px 30px;
          position: relative;

          .icon {
            width:20px;
            display: inline-block;
            position: relative;
            top:-2px;
            margin-right:10px;
            fill:$gray-700;
          }

          &.router-link-exact-active {
            color:$blue;
            font-weight: 500;
            background-color:$white;

            svg {
              fill:$blue;
            }

            // .active_bar {
            //   position: absolute;
            //   height:100%;
            //   width:5px;
            //   background-color:$blue;
            //   display: block;
            //   top:0px;
            //   left:0px;
            // }
          }

          &:hover {
            background-color:rgba(255,255,255,0.6);
          }

          .subtotal_item {
            border-radius:4px;
            background-color:rgba(8,174,234,0.14);
            color:$blue;
            font-size:10px;
            padding:4px 12px;
            float: right;
            text-transform: initial;
          }
        }

        .ofp_siedebar_submenu {
          padding-bottom:0px;
          li {
            border:0px;
            &:first-child {
              margin-top:15px;
            }
            a {
              text-transform: initial;
              font-weight: normal;
              font-size:14px;
              padding:10px 0px 10px 10px;
            }
          }
        }

        &.has_subcats {
          ul li a.router-link-exact-active {
            background-color:transparent;

            &:hover {
              background-color:transparent;
            }
          }
        }
      }
    }

    .profile_block {
      position: absolute;
      bottom:0px;
      left:0px;
      width:100%;
      padding:20px 30px;
      background-color: #F3F7FA;
      border-top:1px solid #FFF;

      a {
        color:$gray-700;

        img {
          width:30px;
          height:30px;
          border-radius: 100px;
          margin-right:5px;
          display: inline-block;
        }

        p {
          display: inline-block;
          font-size:14px;
          margin-bottom:0px;
        }

        &:hover {
          text-decoration: none;
        }
      }
    }
  }

  .ofp_content {
    width: 100%;
    padding: 0 0 130px 220px;

    .right_header {
      height: 70px;
      background-color: #fff;
      border-bottom: 1px solid $gray-200;
      display: table;
      width: 100%;
      position: fixed;
      z-index: 10;
      width: -webkit-calc(100% - 2200px);
      width: -moz-calc(100% - 220px);
      width: calc(100% - 220px);

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

      .compute_block {
        position: absolute;
        top:0px;
        width:280px;
        padding:5px 20px;
        background-color:#F3F7FA;
        right:0px;
        height:100%;
        align-items: center;
        display: flex;

        button {
          width:100%;
        }

        .computed_footprint {
          font-size:16px;
          margin: 0 auto;
          width:100%;
          text-align: center;

          p {
            margin-bottom:0px;
            font-weight: bold;
            line-height:16px;
            color:$blue;

            span {
              cursor:pointer;
              margin-left:5px;
              position: relative;
              top:-1px;
              svg {
                width:16px;
              }
            }
          }

          a {
            font-weight: normal;
            color:inherit;
            text-decoration: underline;
            font-size: 12px;
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