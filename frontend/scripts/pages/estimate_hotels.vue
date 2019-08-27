<template>
  <div>
    <h2>Hotel nights</h2>

    <b-tabs>
      <b-tab active>
        <template slot="title">
          <div class="icon-tab">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              >
              <path
                d="M5,18H9.24a1,1,0,0,0,.71-.29l6.92-6.93h0L19.71,8a1,1,0,0,0,0-1.42L15.47,2.29a1,1,0,0,0-1.42,0L11.23,5.12h0L4.29,12.05a1,1,0,0,0-.29.71V17A1,1,0,0,0,5,18ZM14.76,4.41l2.83,2.83L16.17,8.66,13.34,5.83ZM6,13.17l5.93-5.93,2.83,2.83L8.83,16H6ZM21,20H3a1,1,0,0,0,0,2H21a1,1,0,0,0,0-2Z"
              />
            </svg>
          </div>
          <p>Data</p>
        </template>

        <DataTable
          ref="table_main"
          :fields="hotels_fields"
          collection="hotels"
          :newitemtemplate="{}"
        />
      </b-tab>

      <b-tab :active="(project.people || []).length > 0 && (project.hotels || []).length == 0">
        <template slot="title">
          <div class="icon-tab">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              >
              <path
                d="M8.29,13.29a1,1,0,0,0,0,1.42l3,3a1,1,0,0,0,1.42,0l3-3a1,1,0,0,0-1.42-1.42L13,14.59V3a1,1,0,0,0-2,0V14.59l-1.29-1.3A1,1,0,0,0,8.29,13.29ZM18,9H16a1,1,0,0,0,0,2h2a1,1,0,0,1,1,1v7a1,1,0,0,1-1,1H6a1,1,0,0,1-1-1V12a1,1,0,0,1,1-1H8A1,1,0,0,0,8,9H6a3,3,0,0,0-3,3v7a3,3,0,0,0,3,3H18a3,3,0,0,0,3-3V12A3,3,0,0,0,18,9Z"
              />
            </svg>
          </div>
          <p>Import from attendees</p>
        </template>

        <b-form-group
          label="Average room occupancy"
          label-for="hotels_from_people_averageoccupancy"
        >
          <b-form-input
            id="hotels_from_people_averageoccupancy"
            v-model="hotels_from_people_averageoccupancy"
          />
        </b-form-group>

        <b-button variant="primary" @click="addFromPeople()">
          Add hotels from people
          <b-spinner v-if="loading_add_from_people" small type="grow" />
        </b-button>
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import DataTable from "../components/datatable";

export default {
  components: {
    DataTable
  },
  data() {
    return {
      hotels_fields: [
        {
          key: "name",
          label: "Name"
        },
        {
          key: "address",
          label: "Address"
        },
        {
          key: "starts_at",
          label: "Check-in"
        },
        {
          key: "ends_at",
          label: "Check-out"
        },
        {
          key: "actions",
          label: "",
          class: "th_actions"
        }
      ],
      hotels_from_people_averageoccupancy: 1,
      loading_add_from_people: false
    };
  },
  methods: {
    addFromPeople() {
      this.loading_add_from_people = true;
      var options = {
        averageoccupancy: this.hotels_from_people_averageoccupancy
      };
      this.$http.post(this.project_api_root + "/add_hotels_from_people", options).then(() => {
        this.$parent.refreshProject(() => {
          this.loading_add_from_people = false;
        });
      });
    }
  }
};
</script>

<style lang="scss" scoped></style>
