<template>
  <div>

    <h2 v-if="$parent.project.kind=='event'">Attendees</h2>

    <UploadSheet ref="uploaded_people" :columns='people_uploaded_columns' />

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

</style>