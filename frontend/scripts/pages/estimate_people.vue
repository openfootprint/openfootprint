<template>
  <div>

    <h2 v-if="$parent.project.kind=='event'">Attendees</h2>

    <UploadSheet ref="uploaded_people" :columns='people_uploaded_columns' layout="button"/>
    
    <div class="clearfix"></div>

    <b-tabs>
      <b-tab active>
        <template slot="title">
          <div class="icon-tab"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18.42,8.22A7,7,0,0,0,5.06,10.11,4,4,0,0,0,6,18a1,1,0,0,0,0-2,2,2,0,0,1,0-4,1,1,0,0,0,1-1,5,5,0,0,1,9.73-1.61,1,1,0,0,0,.78.67,3,3,0,0,1,.24,5.84,1,1,0,0,0,.5,1.94,5,5,0,0,0,.17-9.62Zm-5.71,2.07a1,1,0,0,0-.33-.21,1,1,0,0,0-.76,0,1,1,0,0,0-.33.21l-3,3a1,1,0,0,0,1.42,1.42L11,13.41V19a1,1,0,0,0,2,0V13.41l1.29,1.3a1,1,0,0,0,1.42,0,1,1,0,0,0,0-1.42Z"/></svg></div>
          <p>Upload a file</p>
        </template>

        <UploadSheet ref="uploaded_people" :columns='people_uploaded_columns' layout="full_width_upload"/>
      </b-tab>

      <b-tab>
        <template slot="title">
          <div class="icon-tab"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M5,18H9.24a1,1,0,0,0,.71-.29l6.92-6.93h0L19.71,8a1,1,0,0,0,0-1.42L15.47,2.29a1,1,0,0,0-1.42,0L11.23,5.12h0L4.29,12.05a1,1,0,0,0-.29.71V17A1,1,0,0,0,5,18ZM14.76,4.41l2.83,2.83L16.17,8.66,13.34,5.83ZM6,13.17l5.93-5.93,2.83,2.83L8.83,16H6ZM21,20H3a1,1,0,0,0,0,2H21a1,1,0,0,0,0-2Z"/></svg></div>
          <p>Manually fill data</p>
        </template>

        <p>This option will come in a few weeks.</p>
      </b-tab>
    </b-tabs>


    <b-table ref="table_people" :fields="people_fields" striped primary-key="id" v-if="$parent.project.people" :items="$parent.project.people">

      <template slot="home_address" slot-scope="row">
        {{row.value.source_name}}
      </template>

      <template slot="actions" slot-scope="row">
        <b-button @click="deleteRow(row)" ><v-icon name="trash" /></b-button>
      </template>
    </b-table>

    <b-button @click="deleteAllPeople()">Delete all people</b-button>

  </div>
</template>


<script>

import UploadSheet from "../components/uploadsheet"
import Vue from 'vue'

export default {
  data () {
    return {

      people_fields: [
        {
          "key": "name",
          "label": "Name"
        },
        {
          "key": "home_address",
          "label": "From"
        },
        {
          "key": "actions",
          "label": "Actions"
        }
      ],
      people_uploaded_columns: {
        "from_address": "Address from",
        "country": "Country",
        "name": "Name"
      }
    };
  },
  mounted() {
    this.$refs.uploaded_people.$on("data", (data) => {
      // TODO loading (https://bootstrap-vue.js.org/docs/components/table#table-busy-state)
      this.$http.post("/api/project/"+this.$parent.project.id+"/set_people", data).then((response) => {
        this.$parent.refreshProject();
      });
    });
  },
  methods: {
    deleteAllPeople() {
      // TODO loading
      this.$http.post("/api/project/"+this.$parent.project.id+"/delete_people").then((response) => {
        this.$parent.refreshProject();
      });
    },
    deleteRow(row) {
      return alert("TODO");
      this.$parent.project.people.splice(row.index,1);
    },
  },
  components: {
    UploadSheet
  }
}
</script>

<style lang="scss" scoped>

  h2 {
    float: left;
  }
</style>