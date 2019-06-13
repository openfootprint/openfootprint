<template>
  <div>
    <div class="btns_actions">
      <h2>Locations</h2>
      <div class="btns">
        <b-button @click="saveAll()" variant="save">Save locations <b-spinner v-if="loading_save" small type="grow" /></b-button>
      </div>
      <div class="clearfix"></div>
    </div>

    <b-table ref="table_main" :fields="locations_fields" striped primary-key="id" v-if="$parent.project.locations" :items="$parent.project.locations">

      <template slot="name" slot-scope="row">
        <b-input v-model="row.item.name" class="project_location_name" />
      </template>

      <template slot="address_source_name" slot-scope="row">
        <div class="input_w_icon">
          <label for="address_source_name"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12,2a8,8,0,0,0-8,8c0,5.4,7.05,11.5,7.35,11.76a1,1,0,0,0,1.3,0C13,21.5,20,15.4,20,10A8,8,0,0,0,12,2Zm0,17.65c-2.13-2-6-6.31-6-9.65a6,6,0,0,1,12,0C18,13.34,14.13,17.66,12,19.65ZM12,6a4,4,0,1,0,4,4A4,4,0,0,0,12,6Zm0,6a2,2,0,1,1,2-2A2,2,0,0,1,12,12Z"/></svg></label>
          <b-input v-model="row.item.address_source_name" id="address_source_name"/>
        </div>
      </template>

      <!-- <template slot="is_default" slot-scope="row">
        <b-form-checkbox
          v-model="row.item.is_default"
        >
        </b-form-checkbox>
      </template> -->

      <template slot="is_default" slot-scope="row">
        <label>
          <input type="checkbox" class="check-custom toggle-switch" v-model="row.item.is_default">
          <span class="check-toggle"></span>
        </label>
      </template>

      <template slot="actions" slot-scope="row">
        <div class="btn-action" @click="deleteRow(row)" ><v-icon name="trash" /></div>
      </template>

    </b-table>

    <b-button @click="addRow()">Add location</b-button>
    <!-- <b-button @click="saveAll()" variant="primary">Save locations <b-spinner v-if="loading_save" small type="grow" /></b-button> -->
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