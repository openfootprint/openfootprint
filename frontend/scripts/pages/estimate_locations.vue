<template>
  <div>

    <h2>Locations</h2>

    <b-table ref="table_main" :fields="locations_fields" striped primary-key="id" v-if="$parent.project.locations" :items="$parent.project.locations">

      <template slot="name" slot-scope="row">
        <b-input v-model="row.item.name" class="project_location_name" />
      </template>

      <template slot="address_source_name" slot-scope="row">
        <b-input v-model="row.item.address_source_name" />
      </template>

      <template slot="is_default" slot-scope="row">
        <b-form-checkbox
          v-model="row.item.is_default"
        >
        </b-form-checkbox>
      </template>

      <template slot="actions" slot-scope="row">
        <b-button @click="deleteRow(row)" ><v-icon name="trash" /></b-button>
      </template>

    </b-table>

    <b-button @click="addRow()">Add location</b-button>
    <b-button @click="saveAll()" variant="primary">Save locations <b-spinner v-if="loading_save" small type="grow" /></b-button>
  </div>
</template>


<script>

import Vue from 'vue'

export default {
  data () {
    return {
      loading_save: false,
      locations_fields: [
        {
          "key": "name",
          "label": "Name"
        },
        {
          "key": "address_source_name",
          "label": "Address"
        },
        {
          "key": "is_default",
          "label": "Default"
        },
        {
          "key": "actions",
          "label": "Actions"
        }
      ]
    };
  },
  methods: {
    addRow() {
      this.$refs.table_main.items.push({"id": "new_"+Math.random(), "is_default": (this.$refs.table_main.items.length==0)});
      Vue.nextTick(() => {
        var newInput = this.$refs.table_main.$el.querySelector("tr:last-child input[type=text]");
        if (newInput) newInput.focus();
      });
    },
    deleteRow(row) {
      this.$refs.table_main.items.splice(row.index,1);
    },
    saveAll() {
      this.loading_save = true;
      this.$http.post("/api/project/"+this.$parent.project.id+"/set_locations", this.$refs.table_main.items).then((response) => {
        this.$parent.refreshProject(() => {
          this.loading_save = false;
        });
      });
    }
  }
}
</script>

<style lang="scss" scoped>

</style>