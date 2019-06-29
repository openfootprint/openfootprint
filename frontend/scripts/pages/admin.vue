<template>
  <div class="admin_project_page">

    <nav class="ofp_sidebar">
      <b-link :to="{'name':'index'}" class="logo"><img src="../../images/logo_openfootprint_vertical.svg" alt="Logo OpenFootprint"></b-link>
        <ul v-if="user_logged">
          <b-nav-item :to='{"name": "admin_home"}'><span class="icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M20,8h0L14,2.74a3,3,0,0,0-4,0L4,8a3,3,0,0,0-1,2.26V19a3,3,0,0,0,3,3H18a3,3,0,0,0,3-3V10.25A3,3,0,0,0,20,8ZM14,20H10V15a1,1,0,0,1,1-1h2a1,1,0,0,1,1,1Zm5-1a1,1,0,0,1-1,1H16V15a3,3,0,0,0-3-3H11a3,3,0,0,0-3,3v5H6a1,1,0,0,1-1-1V10.25a1,1,0,0,1,.34-.75l6-5.25a1,1,0,0,1,1.32,0l6,5.25a1,1,0,0,1,.34.75Z"/></svg></span>Dashboard</b-nav-item>
          <b-nav-item :to='{"name": "project_list"}'><span class="icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M22.47,18.82l-1-3.86h0L18.32,3.37a1,1,0,0,0-1.22-.71l-3.87,1a1,1,0,0,0-.73-.33H2.5a1,1,0,0,0-1,1v16a1,1,0,0,0,1,1h10a1,1,0,0,0,1-1v-8l2.2,8.22a1,1,0,0,0,1,.74,1.15,1.15,0,0,0,.26,0l4.83-1.29a1,1,0,0,0,.61-.47A1.05,1.05,0,0,0,22.47,18.82Zm-16,.55h-3v-2h3Zm0-4h-3v-6h3Zm0-8h-3v-2h3Zm5,12h-3v-2h3Zm0-4h-3v-6h3Zm0-8h-3v-2h3Zm2.25-1.74,2.9-.78.52,1.93-2.9.78Zm2.59,9.66-1.55-5.8,2.9-.78,1.55,5.8Zm1,3.86-.52-1.93,2.9-.78.52,1.93Z"/></svg></span>Projects</b-nav-item>
          <b-nav-item :to='{"name": "admin_settings"}'><span class="icon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M21.32,9.55l-1.89-.63.89-1.78A1,1,0,0,0,20.13,6L18,3.87a1,1,0,0,0-1.15-.19l-1.78.89-.63-1.89A1,1,0,0,0,13.5,2h-3a1,1,0,0,0-.95.68L8.92,4.57,7.14,3.68A1,1,0,0,0,6,3.87L3.87,6a1,1,0,0,0-.19,1.15l.89,1.78-1.89.63A1,1,0,0,0,2,10.5v3a1,1,0,0,0,.68.95l1.89.63-.89,1.78A1,1,0,0,0,3.87,18L6,20.13a1,1,0,0,0,1.15.19l1.78-.89.63,1.89a1,1,0,0,0,.95.68h3a1,1,0,0,0,.95-.68l.63-1.89,1.78.89A1,1,0,0,0,18,20.13L20.13,18a1,1,0,0,0,.19-1.15l-.89-1.78,1.89-.63A1,1,0,0,0,22,13.5v-3A1,1,0,0,0,21.32,9.55ZM20,12.78l-1.2.4A2,2,0,0,0,17.64,16l.57,1.14-1.1,1.1L16,17.64a2,2,0,0,0-2.79,1.16l-.4,1.2H11.22l-.4-1.2A2,2,0,0,0,8,17.64l-1.14.57-1.1-1.1L6.36,16A2,2,0,0,0,5.2,13.18L4,12.78V11.22l1.2-.4A2,2,0,0,0,6.36,8L5.79,6.89l1.1-1.1L8,6.36A2,2,0,0,0,10.82,5.2l.4-1.2h1.56l.4,1.2A2,2,0,0,0,16,6.36l1.14-.57,1.1,1.1L17.64,8a2,2,0,0,0,1.16,2.79l1.2.4ZM12,8a4,4,0,1,0,4,4A4,4,0,0,0,12,8Zm0,6a2,2,0,1,1,2-2A2,2,0,0,1,12,14Z"/></svg></span>Settings</b-nav-item>
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
            <b-link :to='{"name": "admin_home"}'>Company name</b-link>
          </p>
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
      user_logged: true
    };
  },
  mounted() {

  },
  methods: {

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
        margin:0px auto;
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