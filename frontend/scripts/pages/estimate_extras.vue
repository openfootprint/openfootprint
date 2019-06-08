<template>
  <div>
    <h2>Extras</h2>
    <b-table ref="table_extras" class="project_extras" :fields="extras_fields" striped primary-key="id" v-if="$parent.project.extras" :items="$parent.project.extras">

      <template slot="name" slot-scope="row">
        <b-input v-model="row.item.name" class="project_extras_name" />
      </template>

      <template slot="kind" slot-scope="row">
        <b-form-select v-model="row.item.kind" :options="extras_kinds"></b-form-select>
      </template>

      <template slot="params" slot-scope="row">
        <b-input v-model="row.item.param_f1" />
      </template>

      <template slot="actions" slot-scope="row">
        <b-button @click="deleteRow(row)" ><v-icon name="trash" /></b-button>
      </template>
    </b-table>

    <b-button @click="addExtra()">Add extra</b-button>
    <b-button @click="saveExtras()">Save extras</b-button>
  </div>
</template>


<script>

import Vue from 'vue'

export default {
  data () {
    return {

      extras_fields: [
        {
          "key": "name",
          "label": "Name"
        },
        {
          "key": "kind",
          "label": "Type"
        },
        {
          "key": "params",
          "label": "Parameters"
        },
        {
          "key": "actions",
          "label": "Actions"
        }
      ],

      // TODO get these values directly from the Django model?
      extras_kinds: [
        {
          "value": "co2e",
          "text":"Raw CO2e in grams"
        },
        {
          "value": "wh",
          "text":"Watt hours"
        }
      ]
    };
  },
  methods: {
    addExtra() {
      this.$parent.project.extras.push({"kind": "co2e", "id": "new_"+Math.random()});
      Vue.nextTick(() => {
        var newInput = document.querySelector("table.project_extras tr:last-child input.project_extras_name");
        if (newInput) newInput.focus();
      });
    },
    deleteRow(row) {
      this.$parent.project.extras.splice(row.index,1);
    },
    saveExtras() {
      this.$http.post("/api/project/"+this.$parent.project.id+"/set_extras", this.$parent.project.extras).then((response) => {
        this.$parent.refreshProject();
      });
    }
  },
  components: {
  }
}
</script>

<style lang="scss" scoped>

</style>