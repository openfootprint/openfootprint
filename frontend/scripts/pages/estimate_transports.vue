<template>
  <div>
    <div class="header_page_content">
      <h2>Transports</h2>
    </div>

    <b-tabs>
      <b-tab active>
        <template slot="title">
          <div class="icon-tab">
            <unicon name="file-alt" />
          </div>
          <p>Data</p>
        </template>

        <DataTable
          ref="table_main"
          :fields="transports_fields"
          collection="transports"
          :newitemtemplate="{ from_address: {}, to_address: {} }"
        />
      </b-tab>

      <b-tab v-show="project.transports && project.transports.length > 0" ref="tab_map">
        <template slot="title">
          <div class="icon-tab">
            <unicon name="map" />
          </div>
          <p>Map</p>
        </template>

        <div class="row">
          <!--
          <div class="col-lg-4">
            <div class="standard_block">
              <p class="block_title">
                Block title
              </p>

              <article class="legend_item">
                <div class="legend_data">
                  <p class="legend_info">
                    Paris to Corse
                  </p>
                  <span class="legend_details">123 attendees</span>
                </div>
                <p class="legend_total">
                  789 tons
                </p>
              </article>
              <article class="legend_item">
                <div class="legend_data">
                  <p class="legend_info">
                    Paris to Corse
                  </p>
                  <span class="legend_details">123 attendees</span>
                </div>
                <p class="legend_total">
                  789 tons
                </p>
              </article>
              <article class="legend_item">
                <div class="legend_data">
                  <p class="legend_info">
                    Paris to Corse
                  </p>
                  <span class="legend_details">123 attendees</span>
                </div>
                <p class="legend_total">
                  789 tons
                </p>
              </article>
            </div>
          </div>
          -->
          <div class="col-lg-12">
            <Map ref="map" class="transports_map" :transports="project.transports" />
          </div>
        </div>
      </b-tab>

      <b-tab :active="(project.people || []).length > 0 && (project.transports || []).length == 0">
        <template slot="title">
          <div class="icon-tab">
            <!--<unicon name="import" />-->
          </div>
          <p>Import from attendees</p>
        </template>

        <b-form-group label="Add waypoint for everyone:" label-for="transport_from_people_waypoint">
          <AddressField
            id="transport_from_people_waypoint"
            v-model="transport_from_people_waypoint"
          />
        </b-form-group>

        <b-button variant="primary" @click="addTransportsFromPeople()">
          Add transports from people
          <b-spinner v-if="loading_add_from_people" small type="grow" />
        </b-button>
      </b-tab>

      <b-tab :active="(project.people || []).length == 0 && (project.transports || []).length == 0">
        <template slot="title">
          <div class="icon-tab">
            <unicon name="upload" />
          </div>
          <p>Upload a file</p>
        </template>

        <UploadSheet
          ref="uploaded_transports"
          :columns="transports_uploaded_columns"
          layout="full_width_upload"
        />
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import DataTable from "../components/datatable";
import UploadSheet from "../components/uploadsheet";
import AddressField from "../components/addressfield";
import Map from "../components/map";

export default {
  components: {
    UploadSheet,
    AddressField,
    DataTable,
    Map
  },
  data() {
    return {
      loading_save: false,
      loading_add_from_people: false,

      transport_from_people_waypoint: null,

      transports_fields: [
        {
          key: "checkbox",
          label: "",
          class: "th_checkbox"
        },
        {
          key: "name",
          label: "Name"
        },
        {
          key: "from_address",
          label: "From"
        },
        {
          key: "to_address",
          label: "To"
        },
        {
          key: "mode",
          label: "Mode",
          class: "th_dropdown"
        },
        {
          key: "roundtrip",
          label: "Roundtrip?",
          class: "th_checkbox_toggle"
        },
        {
          key: "actions",
          label: "",
          class: "th_actions"
        }
      ],
      transports_uploaded_columns: {
        from_address: "Address from",
        to_address: "Address to",
        mode: "Mode",
        roundtrip: "Roundtrip",
        name: "Name"
      }
    };
  },
  mounted() {
    this.$refs.uploaded_transports.$on("data", data => {
      // TODO loading (https://bootstrap-vue.js.org/docs/components/table#table-busy-state)
      this.$http.post(this.project_api_root + "/set_transports", data).then(() => {
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
        waypoints: this.transport_from_people_waypoint
          ? [this.transport_from_people_waypoint.source_name]
          : []
      };
      this.$http.post(this.project_api_root + "/add_transports_from_people", options).then(() => {
        this.$parent.refreshProject(() => {
          this.loading_add_from_people = false;
        });
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.transports_map {
  width: 100%;
  height: 400px;
}
</style>
