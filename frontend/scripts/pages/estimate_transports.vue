<template>
  <div>
    <div class="header_page_content">
      <h2>Transports</h2>
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc sed suscipit est, in sollicitudin nisl. Vivamus vehicula eget est non vestibulum. Ut quam arcu, pharetra eu nibh id, sodales euismod ipsum.</p>
    </div>

    <b-tabs>

      <b-tab active>
        <template slot="title">
          <div class="icon-tab"><unicon name="file-alt"></unicon></div>
          <p>Data</p>
        </template>

        <DataTable ref="table_main" :fields="transports_fields" collection="transports" :newitemtemplate='{"from_address": {}, "to_address": {}}' />
      </b-tab>

      <b-tab ref="tab_map" v-show="project.transports && project.transports.length>0">
        <template slot="title">
          <div class="icon-tab"><unicon name="map"></unicon></div>
          <p>Map</p>
        </template>
        
        <div class="row">
          <div class="col-lg-4">
            <div class="standard_block">
              <p class="block_title">Block title</p>

              <article class="legend_item">
                <div class="legend_data">
                  <p class="legend_info">Paris to Corse</p>
                  <span class="legend_details">123 attendees</span>
                </div>
                <p class="legend_total">789 tons</p>
              </article>
              <article class="legend_item">
                <div class="legend_data">
                  <p class="legend_info">Paris to Corse</p>
                  <span class="legend_details">123 attendees</span>
                </div>
                <p class="legend_total">789 tons</p>
              </article>
              <article class="legend_item">
                <div class="legend_data">
                  <p class="legend_info">Paris to Corse</p>
                  <span class="legend_details">123 attendees</span>
                </div>
                <p class="legend_total">789 tons</p>
              </article>
            </div>
          </div>

          <div class="col-lg-8">
            <div class="main_container_map"><div id="map"></div></div>
          </div>
        </div>
      </b-tab>

      <b-tab :active="(project.people||[]).length>0 && (project.transports||[]).length==0">
        <template slot="title">
          <div class="icon-tab"><unicon name="import"></unicon></div>
          <p>Import from attendees</p>
        </template>

        <b-form-group
          label="Add waypoint for everyone:"
          label-for="transport_from_people_waypoint"
        >
          <AddressField
            id="transport_from_people_waypoint"
            v-model="transport_from_people_waypoint"
          />
        </b-form-group>

        <b-button @click="addTransportsFromPeople()" variant="primary">Add transports from people <b-spinner v-if="loading_add_from_people" small type="grow" /></b-button>

      </b-tab>

      <b-tab :active="(project.people||[]).length==0 && (project.transports||[]).length==0">
        <template slot="title">
          <div class="icon-tab"><unicon name="upload"></unicon></div>
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
import Vue from 'vue'
import L from "leaflet"
import '@elfalem/leaflet-curve'

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
      this.$http.post("/api/project/"+this.project.id+"/set_transports", data).then((response) => {
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
      this.$http.post("/api/project/"+this.project.id+"/add_transports_from_people", options).then((response) => {
        this.$parent.refreshProject(() => {
          this.loading_add_from_people = false;
        });
      });
    },
    renderMap() {

      var latlngs = [];

      var map = L.map('map').setView([48.53, 2.14], 10);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: ' <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
      }).addTo(map);

      this.project.transports.forEach((transport) => {
        var line = [[transport.from_address.latitude, transport.from_address.longitude], [transport.to_address.latitude, transport.to_address.longitude]];
        latlngs.push(line);
        
        var center = L.polyline([line]).getBounds().getCenter();
        center.lat += (transport.from_address.latitude - center.lat) * 0.5
        center.lng -= (transport.from_address.longitude - center.lng) * 0.5

        
        L.curve(['M', [transport.from_address.latitude, transport.from_address.longitude], 
        'Q', [center.lat, center.lng], [transport.to_address.latitude, transport.to_address.longitude]]).addTo(map);

      });
      
      var polyline = L.polyline(latlngs, {color: 'blue'});
      map.fitBounds(polyline.getBounds());
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

  .main_container_map {
    width:100%;
    height:400px;
    overflow: hidden;
    border-radius:14px;

    #map {
      height:400px;
      width:100%;
    }
  }

</style>