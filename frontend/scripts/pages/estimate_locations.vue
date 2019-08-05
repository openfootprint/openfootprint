<template>
  <div>
    <div class="header_page_content">
      <h2>Locations</h2>
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc sed suscipit est, in sollicitudin nisl. Vivamus vehicula eget est non vestibulum. Ut quam arcu, pharetra eu nibh id, sodales euismod ipsum.</p>
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
        <DataTable ref="table_main" :fields="locations_fields" collection="locations" :newitemtemplate='{}' />
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
          "key": "address_source_name",
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
  },
  components: {
    DataTable
  },
  mounted() {
    var locationmap = L.map('map').setView([48.53, 2.14], 10);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: ' <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(locationmap);
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