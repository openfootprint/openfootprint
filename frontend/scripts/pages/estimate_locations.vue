<template>
  <div>
    <div class="header_page_content">
      <h2>Locations</h2>
      <p>
        Your event might have one or more locations (main venue, staff HQ, ...). You can enter their
        addresses here.
      </p>
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
        <DataTable
          ref="table_main"
          autosave
          :fields="locations_fields"
          collection="locations"
          :newitemtemplate="{}"
        />
      </div>

      <div class="col-lg-4">
        <Map ref="map" class="location_map" :locations="project.locations" />
      </div>
    </div>
  </div>
</template>

<script>
import DataTable from "../components/datatable";
import Map from "../components/map";

export default {
  components: {
    DataTable,
    Map
  },
  data() {
    return {
      loading_save: false,
      locations_fields: [
        {
          key: "address",
          label: "Address"
        },
        {
          key: "name",
          label: "Name"
        },
        {
          key: "is_default",
          label: "Default",
          class: "th_checkbox_toggle"
        },
        {
          key: "actions",
          label: "",
          class: "th_actions"
        }
      ]
    };
  },
  mounted() {
    // TODO: refresh if some un-geolocated addresses
  },
  methods: {}
};
</script>

<style lang="scss" scoped>
.location_map {
  height: 400px;
  width: 100%;
}
</style>
