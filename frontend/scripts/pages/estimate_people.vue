<template>
  <div>
    <div class="header_page_content">
      <h2 v-if="project.kind=='event'">Attendees</h2>
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc sed suscipit est, in sollicitudin nisl. Vivamus vehicula eget est non vestibulum. Ut quam arcu, pharetra eu nibh id, sodales euismod ipsum.</p>
    </div>

    <b-tabs>
      <b-tab>
        <template slot="title">
          <div class="icon-tab"><unicon name="file-alt"></unicon></div>
          <p>Data</p>
        </template>

        <DataTable ref="table_main" :fields="people_fields" collection="people" :newitemtemplate='{"home_address": {}}' />

      </b-tab>

      <b-tab :active="(project.people||[]).length==0">
        <template slot="title">
          <div class="icon-tab"><unicon name="upload"></unicon></div>
          <p>Upload a file</p>
        </template>

        <UploadSheet ref="uploaded_people" :columns='people_uploaded_columns' layout="full_width_upload"/>
      </b-tab>

    </b-tabs>


  </div>
</template>


<script>

import DataTable from "../components/datatable"
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
      this.$http.post("/api/project/"+this.project.id+"/set_people", data).then((response) => {
        this.refreshProject();
      });
    });
  },
  methods: {
  },
  components: {
    UploadSheet,
    DataTable
  }
}
</script>

<style lang="scss" scoped>

</style>