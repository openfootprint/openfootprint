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
          <div class="icon-tab"><unicon name="edit-alt"></unicon></div>
          <p>Data</p>
        </template>

        <DataTable ref="table_main" :fields="transports_fields" collection="transports" :newitemtemplate='{"from_address": {}, "to_address": {}}' />

      </b-tab>

      <b-tab ref="tab_map" v-show="project.transports && project.transports.length>0">
        <template slot="title">
          <div class="icon-tab"><unicon name="map"></unicon></div>
          <p>Map</p>
        </template>

        <div class="main_container_map"><div class="map_container"></div></div>
      </b-tab>

      <b-tab :active="(project.people||[]).length>0 && (project.transports||[]).length==0">
        <template slot="title">
          <div class="icon-tab"><unicon name="down-arrow"></unicon></div>
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
          <div class="icon-tab"><unicon name="cloud-upload"></unicon></div>
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

      var data = [];

      var latitudes = [];
      var longitudes = [];

      this.project.transports.forEach((transport) => {
        data.push({
          type: 'scattergeo',
          lon: [ transport.from_address.longitude, transport.to_address.longitude ],
          lat: [ transport.from_address.latitude, transport.to_address.latitude ],
          mode: 'lines',
          line: {
              width: 3,
              color: 'red'
          },
          opacity: 0.1
        });
        latitudes.push(transport.from_address.latitude);
        latitudes.push(transport.to_address.latitude);
        longitudes.push(transport.from_address.longitude);
        longitudes.push(transport.to_address.longitude);
      });

      // Find the bounding box
      // TODO: test this with corner cases
      var topleft = [Math.max(...latitudes), Math.min(...longitudes)];
      var bottomright = [Math.min(...latitudes), Math.max(...longitudes)];

      var center = [(topleft[0] + bottomright[0])/2, (topleft[1] + bottomright[1])/2];
      var maxSize = Math.max(topleft[0] - bottomright[0], bottomright[1] - topleft[1]);

      var layout = {
          showlegend: false,
          geo:{
              scope: 'world',
              projection: {
                  type: 'mercator',
                  scale: maxSize / 2
              },
              showland: true,
              showframe: false,
              showcountries: true,
              showcoastlines: false,
              showocean: true,
              oceancolor: "#8acdec",
              landcolor: "#f1ede8",
              countrycolor: "#d9d4cd",
              center: {
                  lat: center[0] - (maxSize / 2), // Compensate for overflow position. TODO: should be done in CSS
                  lon: center[1]
              },
          },
          margin: {
            l: 0,
            r: 0,
            b: 0,
            t: 0,
            pad: 0
        },
        autosize: true,
        //width:900,
        height: 1400 // TODO make this dynamic
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

  .main_container_map {
    width:100%;
    height:500px;
    overflow: hidden;
    border-radius: 8px;
    position:relative;

    .map_container {
      position: absolute;
      top:-50%;
      width:100%;
    }
  }

</style>