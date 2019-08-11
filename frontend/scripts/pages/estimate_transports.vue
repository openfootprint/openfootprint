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
            <Map class="transports_map" ref="map" :transports="project.transports" />
          </div>
        </div>
      </b-tab>

      <b-tab :active="(project.people||[]).length>0 && (project.transports||[]).length==0">
        <template slot="title">
          <div class="icon-tab"><unicon name="map"></unicon></div>
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
import Map from "../components/map"
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
        this.$refs.map.reDraw();
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
    }
  },
  components: {
    UploadSheet,
    AddressField,
    DataTable,
    Map
  }
}
</script>

<style lang="scss" scoped>

  .transports_map {
    width:100%;
    height:400px;
    border-radius:14px;
  }

</style>