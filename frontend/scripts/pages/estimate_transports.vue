<template>
  <div>
    <div class="btns_actions">
      <h2>Transports</h2>
      <div class="btns">
        <b-button @click="saveAll()" variant="save">Save<b-spinner v-if="loading_save" small type="grow" /></b-button>
      </div>
      <div class="clearfix"></div>
    </div>

    <b-tabs>

      <b-tab active>
        <template slot="title">
          <div class="icon-tab"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M5,18H9.24a1,1,0,0,0,.71-.29l6.92-6.93h0L19.71,8a1,1,0,0,0,0-1.42L15.47,2.29a1,1,0,0,0-1.42,0L11.23,5.12h0L4.29,12.05a1,1,0,0,0-.29.71V17A1,1,0,0,0,5,18ZM14.76,4.41l2.83,2.83L16.17,8.66,13.34,5.83ZM6,13.17l5.93-5.93,2.83,2.83L8.83,16H6ZM21,20H3a1,1,0,0,0,0,2H21a1,1,0,0,0,0-2Z"/></svg></div>
          <p>Data</p>
        </template>

        <DataTable ref="table_main" :fields="transports_fields" :root="$parent" :items="$parent.project.transports" collection="transports" :newitemtemplate='{"from_address": {}, "to_address": {}}' />

      </b-tab>

      <b-tab ref="tab_map" v-show="$parent.project.transports && $parent.project.transports.length>0">
        <template slot="title">
          <div class="icon-tab"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M21.32,5.05l-6-2h-.07a.7.7,0,0,0-.14,0h-.23l-.13,0h-.07L9,5,3.32,3.05a1,1,0,0,0-.9.14A1,1,0,0,0,2,4V18a1,1,0,0,0,.68.95l6,2h0a1,1,0,0,0,.62,0h0L15,19.05,20.68,21A1.19,1.19,0,0,0,21,21a.94.94,0,0,0,.58-.19A1,1,0,0,0,22,20V6A1,1,0,0,0,21.32,5.05ZM8,18.61,4,17.28V5.39L8,6.72Zm6-1.33-4,1.33V6.72l4-1.33Zm6,1.33-4-1.33V5.39l4,1.33Z"/></svg></div>
          <p>Map</p>
        </template>

        <div class="map_container"></div>
      </b-tab>

      <b-tab :active="($parent.project.people||[]).length>0 && ($parent.project.transports||[]).length==0">
        <template slot="title">
          <div class="icon-tab"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M8.29,13.29a1,1,0,0,0,0,1.42l3,3a1,1,0,0,0,1.42,0l3-3a1,1,0,0,0-1.42-1.42L13,14.59V3a1,1,0,0,0-2,0V14.59l-1.29-1.3A1,1,0,0,0,8.29,13.29ZM18,9H16a1,1,0,0,0,0,2h2a1,1,0,0,1,1,1v7a1,1,0,0,1-1,1H6a1,1,0,0,1-1-1V12a1,1,0,0,1,1-1H8A1,1,0,0,0,8,9H6a3,3,0,0,0-3,3v7a3,3,0,0,0,3,3H18a3,3,0,0,0,3-3V12A3,3,0,0,0,18,9Z"/></svg></div>
          <p>Import from attendees</p>
        </template>

        <div class="full_width_upload_import import_field">
          <div class="icon_empty"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M8.29,13.29a1,1,0,0,0,0,1.42l3,3a1,1,0,0,0,1.42,0l3-3a1,1,0,0,0-1.42-1.42L13,14.59V3a1,1,0,0,0-2,0V14.59l-1.29-1.3A1,1,0,0,0,8.29,13.29ZM18,9H16a1,1,0,0,0,0,2h2a1,1,0,0,1,1,1v7a1,1,0,0,1-1,1H6a1,1,0,0,1-1-1V12a1,1,0,0,1,1-1H8A1,1,0,0,0,8,9H6a3,3,0,0,0-3,3v7a3,3,0,0,0,3,3H18a3,3,0,0,0,3-3V12A3,3,0,0,0,18,9Z"/></svg></div>
          <p>Click here to import transports from your attendees</p>
          <b-button @click="addTransportsFromPeople()" variant="primary">Add transports from people <b-spinner v-if="loading_add_from_people" small type="grow" /></b-button>
        </div>

        <br/>

        <b-form-group
          label="Add waypoint for everyone:"
          label-for="transport_from_people_waypoint"
        >
          <AddressField
            id="transport_from_people_waypoint"
            v-model="transport_from_people_waypoint"
          />
        </b-form-group>


      </b-tab>

      <b-tab :active="($parent.project.people||[]).length==0 && ($parent.project.transports||[]).length==0">
        <template slot="title">
          <div class="icon-tab"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18.42,8.22A7,7,0,0,0,5.06,10.11,4,4,0,0,0,6,18a1,1,0,0,0,0-2,2,2,0,0,1,0-4,1,1,0,0,0,1-1,5,5,0,0,1,9.73-1.61,1,1,0,0,0,.78.67,3,3,0,0,1,.24,5.84,1,1,0,0,0,.5,1.94,5,5,0,0,0,.17-9.62Zm-5.71,2.07a1,1,0,0,0-.33-.21,1,1,0,0,0-.76,0,1,1,0,0,0-.33.21l-3,3a1,1,0,0,0,1.42,1.42L11,13.41V19a1,1,0,0,0,2,0V13.41l1.29,1.3a1,1,0,0,0,1.42,0,1,1,0,0,0,0-1.42Z"/></svg></div>
          <p>Upload a file</p>
        </template>

        <UploadSheet ref="uploaded_transports" :columns='transports_uploaded_columns' layout="full_width_upload"/>

      </b-tab>

    </b-tabs>

  </div>
</template>


<script>

import DataTable from "../components/datatable"
import UploadSheet from "../components/uploadsheet"
import AddressField from "../components/addressfield"
import Plotly from 'plotly.js-dist'
import Vue from 'vue'

export default {
  data () {
    return {

      loading_save: false,
      loading_add_from_people:false,

      transport_from_people_waypoint:null,

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
          "label": "Mode",
          "class": "th_dropdown"
        },
        {
          "key": "roundtrip",
          "label": "Roundtrip?",
          "class": "th_checkbox"
        },
        {
          "key": "actions",
          "label": "",
          "class": "th_actions"
        }
      ],
      transports_uploaded_columns: {
        "from_address": "Address from",
        "to_address": "Address to",
        "mode": "Mode",
        "roundtrip": "Roundtrip",
        "name": "Name"
      }
    };
  },
  mounted() {
    this.$refs.uploaded_transports.$on("data", (data) => {
      // TODO loading (https://bootstrap-vue.js.org/docs/components/table#table-busy-state)
      this.$http.post("/api/project/"+this.$parent.project.id+"/set_transports", data).then((response) => {
        this.$parent.refreshProject();
      });
    });
    this.$refs.tab_map.$on("click", () => {
      // TODO proper event on tab show, with width set already
      setTimeout(() => {
        this.renderMap();
      }, 200);
    });
  },
  methods: {
    addTransportsFromPeople() {
      this.loading_add_from_people = true;
      var options = {
        "waypoints": this.transport_from_people_waypoint?[
          this.transport_from_people_waypoint.source_name
        ]:[]
      }
      this.$http.post("/api/project/"+this.$parent.project.id+"/add_transports_from_people", options).then((response) => {
        this.$parent.refreshProject(() => {
          this.loading_add_from_people = false;
        });
      });
    },
    renderMap() {

      var data = [];

      this.$parent.project.transports.forEach((transport) => {
        data.push({
          type: 'scattergeo',
          locationmode: 'USA-states',
          lon: [ transport.from_address.longitude, transport.to_address.longitude ],
          lat: [ transport.from_address.latitude, transport.to_address.latitude ],
          mode: 'lines',
          line: {
              width: 1,
              color: 'red'
          },
          opacity: 1
        });
      });

      var layout = {
          showlegend: false,
          geo:{
              scope: 'world',
              projection: {
                  type: 'equirectangular'
              },
              showland: true,
              landcolor: 'rgb(243,243,243)',
              countrycolor: 'rgb(204,204,204)',
              showframe: false,
              showcountries: true
          },
          margin: {
            l: 0,
            r: 0,
            b: 0,
            t: 0,
            pad: 0
        },
        autosize: true
        //width:900,
        //height: 400
      };

      var config = {
        displayModeBar: false,
        showLink: false,
        responsive: true
      };
      Plotly.plot(this.$refs.tab_map.$el.querySelector(".map_container"), data, layout, config);

    }
  },
  components: {
    UploadSheet,
    AddressField,
    DataTable
  }
}
</script>

<style lang="scss" scoped>

  h2 {
    float: left;
  }

</style>