<template>
  <div>
    <div class="btns_actions">
      <h2 v-if="$parent.project.kind=='event'">Attendees</h2>
      <div class="btns">
        <b-button @click="saveAll()" variant="save">Save<b-spinner v-if="loading_save" small type="grow" /></b-button>
      </div>
      <div class="clearfix"></div>
    </div>

    <b-tabs>
      <b-tab>
        <template slot="title">
          <div class="icon-tab"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M5,18H9.24a1,1,0,0,0,.71-.29l6.92-6.93h0L19.71,8a1,1,0,0,0,0-1.42L15.47,2.29a1,1,0,0,0-1.42,0L11.23,5.12h0L4.29,12.05a1,1,0,0,0-.29.71V17A1,1,0,0,0,5,18ZM14.76,4.41l2.83,2.83L16.17,8.66,13.34,5.83ZM6,13.17l5.93-5.93,2.83,2.83L8.83,16H6ZM21,20H3a1,1,0,0,0,0,2H21a1,1,0,0,0,0-2Z"/></svg></div>
          <p>Data</p>
        </template>

        <DataTable ref="table_main" :fields="people_fields" :root="$parent" :items="$parent.project.people" collection="people" :newitemtemplate='{"home_address": {}}' />

      </b-tab>

      <b-tab :active="($parent.project.people||[]).length==0">
        <template slot="title">
          <div class="icon-tab"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18.42,8.22A7,7,0,0,0,5.06,10.11,4,4,0,0,0,6,18a1,1,0,0,0,0-2,2,2,0,0,1,0-4,1,1,0,0,0,1-1,5,5,0,0,1,9.73-1.61,1,1,0,0,0,.78.67,3,3,0,0,1,.24,5.84,1,1,0,0,0,.5,1.94,5,5,0,0,0,.17-9.62Zm-5.71,2.07a1,1,0,0,0-.33-.21,1,1,0,0,0-.76,0,1,1,0,0,0-.33.21l-3,3a1,1,0,0,0,1.42,1.42L11,13.41V19a1,1,0,0,0,2,0V13.41l1.29,1.3a1,1,0,0,0,1.42,0,1,1,0,0,0,0-1.42Z"/></svg></div>
          <p>Upload a file</p>
        </template>

        <UploadSheet ref="uploaded_people" :columns='people_uploaded_columns' layout="full_width_upload"/>
      </b-tab>

    </b-tabs>


  </div>
</template>


<script>

import DataTable from "../components/datatable"
import AddressField from "../components/addressfield"
import UploadSheet from "../components/uploadsheet"
import Vue from 'vue'

export default {
  data () {
    return {
      loading_save: false,
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
          "label": "",
          "class": "th_actions"
        }
      ],
      people_uploaded_columns: {
        "home_address": "Address",
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
    addRow() {
      this.$parent.project.people.push({"id": "new_"+Math.random(), "home_address": {}});
      Vue.nextTick(() => {
        var newInput = this.$refs.table_main.$el.querySelector("tr:last-child input[type=text]");
        if (newInput) newInput.focus();
      });
    },
    deleteAll() {
      this.$http.post("/api/project/"+this.$parent.project.id+"/delete_people").then((response) => {
        this.$parent.refreshProject();
      });
    },
    deleteRow(row) {
      this.$parent.project.people.splice(row.index,1);
    },
    saveAll() {
      this.loading_save = true;
      this.$http.post("/api/project/"+this.$parent.project.id+"/set_people", this.$refs.table_main.items).then((response) => {
        this.$parent.refreshProject(() => {
          this.loading_save = false;
        });
      });
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

</style>