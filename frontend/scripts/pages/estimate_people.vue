<template>
  <div>
    <div class="header_page_content">
      <h2 v-if="project.kind == 'event'">
        Attendees
      </h2>
      <p>
        We need data about your attendees (most importantly, their origin location) in order to
        compute a footprint.
      </p>
    </div>

    <b-tabs>
      <b-tab>
        <template slot="title">
          <div class="icon-tab">
            <unicon name="file-alt" />
          </div>
          <p>Data</p>
        </template>

        <DataTable
          ref="table_main"
          autosave
          :fields="people_fields"
          collection="people"
          :newitemtemplate="{ home_address: {} }"
        />
      </b-tab>

      <b-tab :active="(project.people || []).length == 0">
        <template slot="title">
          <div class="icon-tab">
            <unicon name="upload" />
          </div>
          <p>Upload a file</p>
        </template>

        <UploadSheet
          ref="uploaded_people"
          :columns="people_uploaded_columns"
          layout="full_width_upload"
        />
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import DataTable from "../components/datatable";
import UploadSheet from "../components/uploadsheet";

export default {
  components: {
    UploadSheet,
    DataTable
  },
  data() {
    return {
      loading_save: false,
      people_fields: [
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
          key: "home_address",
          label: "From"
        },
        {
          key: "actions",
          label: "",
          class: "th_actions"
        }
      ],
      people_uploaded_columns: {
        home_address: "Address",
        country: "Country",
        name: "Name"
      }
    };
  },
  mounted() {
    this.$refs.uploaded_people.$on("data", data => {
      // TODO loading (https://bootstrap-vue.js.org/docs/components/table#table-busy-state)
      this.$http.post(this.project_api_root + "/set_people", data).then(() => {
        this.refreshProject();
      });
    });
  },
  methods: {}
};
</script>

<style lang="scss" scoped></style>
