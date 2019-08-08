<template>
  <div>
    <div class="header_page_content">
      <h2>Locations</h2>
      <p>Your event might have one or more locations (main venue, staff HQ, ...). You can enter their addresses here.</p>
    </div>

    <!-- <div class="btns_actions">
      <h2>Locations</h2>
      <div class="btns">
        <b-button @click="saveAll()" variant="save">Save <b-spinner v-if="loading_save" small type="grow" /></b-button>
      </div>
      <div class="clearfix"></div>
    </div> -->

    <div class="row">
      <div class="col-lg-8">
        <DataTable autosave ref="table_main" :fields="locations_fields" collection="locations" :newitemtemplate='{}' />
      </div>

      <div class="col-lg-4">
        <div class="location_map">
           <div id="map"></div>
        </div>
      </div>
    </div>
 </div>
</template>


<script>

import DataTable from "../components/datatable"
import Vue from 'vue'
import L from "leaflet"

export default {
  data () {
    return {
      loading_save: false,
      locations_fields: [
        {
          "key": "address",
          "label": "Address"
        },
        {
          "key": "name",
          "label": "Name"
        },
        {
          "key": "is_default",
          "label": "Default",
          "class": "th_checkbox"
        },
        {
          "key": "actions",
          "label": "",
          "class": "th_actions"
        }
      ]
    };
  },
  methods: {
    redrawMap() {

      if (!this.project["locations"]) return;

      if (this.mapMarkers) {
        this.map.removeLayer(this.mapMarkers)
      }

      var markers = [];
      this.project["locations"].forEach((location) => {
        if (!(location.address||{}).latitude && !(location.address||{}).longitude) return;
        markers.push(L.marker([location.address.latitude, location.address.longitude]));
      });

      this.mapMarkers = new L.featureGroup(markers);

      var justcreated = false;
      if (!this.map) {
        this.map = L.map('map');
        justcreated = true;
      }

      this.map.fitBounds(this.mapMarkers.getBounds());

      if (justcreated) {
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          maxZoom: 19,
          attribution: ' <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(this.map);
      }

      this.mapMarkers.addTo(this.map);

    }
  },
  components: {
    DataTable
  },
  mounted() {
    this.redrawMap();
    this.$watch("project", (evt) => {
      this.redrawMap();
    });
    this.$watch("project.locations", (evt) => {
      this.redrawMap();
    });
    // TODO: refresh if some un-geolocated addresses
  }
}
</script>

<style lang="scss" scoped>
  #map {
    height:400px;
    width:100%;
    border-radius:14px;
  }

  .location_map {
    height:400px;
    width:100%;
  }

</style>