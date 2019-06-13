<template>
  <div class="admin_project_page">

    <nav class="ofp_sidebar">
      <b-link :to="{'name':'index'}" class="logo"><img src="../../images/logo_openfootprint_vertical.svg" alt="Logo OpenFootprint"></b-link>

        <ul>
          <b-nav-item :to='{"name": "project_home"}'><span class="icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M20,8h0L14,2.74a3,3,0,0,0-4,0L4,8a3,3,0,0,0-1,2.26V19a3,3,0,0,0,3,3H18a3,3,0,0,0,3-3V10.25A3,3,0,0,0,20,8ZM14,20H10V15a1,1,0,0,1,1-1h2a1,1,0,0,1,1,1Zm5-1a1,1,0,0,1-1,1H16V15a3,3,0,0,0-3-3H11a3,3,0,0,0-3,3v5H6a1,1,0,0,1-1-1V10.25a1,1,0,0,1,.34-.75l6-5.25a1,1,0,0,1,1.32,0l6,5.25a1,1,0,0,1,.34.75Z"/></svg></span>Dashboard</b-nav-item>
          <b-nav-item class="has_subcats">
            <span class="icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12,6a1,1,0,0,0-1,1V17a1,1,0,0,0,2,0V7A1,1,0,0,0,12,6ZM7,12a1,1,0,0,0-1,1v4a1,1,0,0,0,2,0V13A1,1,0,0,0,7,12Zm10-2a1,1,0,0,0-1,1v6a1,1,0,0,0,2,0V11A1,1,0,0,0,17,10Zm2-8H5A3,3,0,0,0,2,5V19a3,3,0,0,0,3,3H19a3,3,0,0,0,3-3V5A3,3,0,0,0,19,2Zm1,17a1,1,0,0,1-1,1H5a1,1,0,0,1-1-1V5A1,1,0,0,1,5,4H19a1,1,0,0,1,1,1Z"/></svg></span>Estimate
            <!--<span class="subtotal_item">10t</span>-->
            <ul class="ofp_siedebar_submenu">
              <b-nav-item :to='{"name": "estimate_locations"}'>Locations</b-nav-item>
              <b-nav-item :to='{"name": "estimate_people"}'>
                <span v-if="project.kind=='company'">Employees</span>
                <span v-if="project.kind=='event'">Attendees</span>
              </b-nav-item>
              <b-nav-item :to='{"name": "estimate_transports"}'>Transports</b-nav-item>
              <b-nav-item >Food</b-nav-item>
              <b-nav-item >Hotels</b-nav-item>
              <b-nav-item :to='{"name": "estimate_extras"}' v-if="project.kind=='event'">Extras</b-nav-item>

            </ul>
          </b-nav-item>
          <b-nav-item><span class="icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M7,16a1.5,1.5,0,0,0,1.5-1.5.77.77,0,0,0,0-.15l2.79-2.79.23,0,.23,0,1.61,1.61s0,.05,0,.08a1.5,1.5,0,1,0,3,0v-.08L20,9.5h0A1.5,1.5,0,1,0,18.5,8a.77.77,0,0,0,0,.15l-3.61,3.61h-.16L13,10a1.49,1.49,0,0,0-3,0L7,13H7a1.5,1.5,0,0,0,0,3Zm13.5,4H3.5V3a1,1,0,0,0-2,0V21a1,1,0,0,0,1,1h18a1,1,0,0,0,0-2Z"/></svg></span>Reports</b-nav-item>
          <b-nav-item :to='{"name": "project_settings"}'><span class="icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M21.32,9.55l-1.89-.63.89-1.78A1,1,0,0,0,20.13,6L18,3.87a1,1,0,0,0-1.15-.19l-1.78.89-.63-1.89A1,1,0,0,0,13.5,2h-3a1,1,0,0,0-.95.68L8.92,4.57,7.14,3.68A1,1,0,0,0,6,3.87L3.87,6a1,1,0,0,0-.19,1.15l.89,1.78-1.89.63A1,1,0,0,0,2,10.5v3a1,1,0,0,0,.68.95l1.89.63-.89,1.78A1,1,0,0,0,3.87,18L6,20.13a1,1,0,0,0,1.15.19l1.78-.89.63,1.89a1,1,0,0,0,.95.68h3a1,1,0,0,0,.95-.68l.63-1.89,1.78.89A1,1,0,0,0,18,20.13L20.13,18a1,1,0,0,0,.19-1.15l-.89-1.78,1.89-.63A1,1,0,0,0,22,13.5v-3A1,1,0,0,0,21.32,9.55ZM20,12.78l-1.2.4A2,2,0,0,0,17.64,16l.57,1.14-1.1,1.1L16,17.64a2,2,0,0,0-2.79,1.16l-.4,1.2H11.22l-.4-1.2A2,2,0,0,0,8,17.64l-1.14.57-1.1-1.1L6.36,16A2,2,0,0,0,5.2,13.18L4,12.78V11.22l1.2-.4A2,2,0,0,0,6.36,8L5.79,6.89l1.1-1.1L8,6.36A2,2,0,0,0,10.82,5.2l.4-1.2h1.56l.4,1.2A2,2,0,0,0,16,6.36l1.14-.57,1.1,1.1L17.64,8a2,2,0,0,0,1.16,2.79l1.2.4ZM12,8a4,4,0,1,0,4,4A4,4,0,0,0,12,8Zm0,6a2,2,0,1,1,2-2A2,2,0,0,1,12,14Z"/></svg></span>Settings</b-nav-item>
      </ul>

      <div class="profile_block">
        <!-- TODO -->
        <a href="#">
          <img src="../../images/logo_openfootprint_icon.svg" />
          <p>OpenFootprint</p>
        </a>
      </div>
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
        <div class="compute_block">
            <b-button @click="computeFootprint()" variant="primary" v-if="!total_co2e"><b-spinner v-if="loading_footprint" small type="grow" /> Compute footprint</b-button>

            <div v-if="total_co2e" class="computed_footprint">
              <p>{{total_co2e}} gCO2e <span @click="computeFootprint()" v-if="total_co2e"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M21,11a1,1,0,0,0-1,1,8.05,8.05,0,1,1-2.22-5.5h-2.4a1,1,0,0,0,0,2h4.53a1,1,0,0,0,1-1V3a1,1,0,0,0-2,0V4.77A10,10,0,1,0,22,12,1,1,0,0,0,21,11Z"/></svg></span></p>
              <a v-if="footprint_id" :href="'/report/'+footprint_id+'/'" target="_blank">View report</a>
            </div>
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
      total_co2e: true,
      footprint_id:true
    };
  },
  created() {
    this.refreshProject();
  },
  methods: {
    refreshProject(callback) {
      // TODO loading
      this.$http.get("/api/project/"+this.$route.params.id).then((response) => {
        response.data.locations.forEach((loc) => {
          loc.address_source_name = (loc.address||{}).source_name;
        });
        this.project = response.data;
        if (callback) callback();
      });
    },
    computeFootprint() {
      this.loading_footprint = true;
      this.$http.post("/api/project/"+this.project.id+"/footprint").then((response) => {
        this.loading_footprint = false;
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
            
            svg {
              fill:$gray-700;
            }
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
        width:250px;
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