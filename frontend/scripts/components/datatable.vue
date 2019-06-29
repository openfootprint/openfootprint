<template>
  <div>

    <b-table ref="table_main" sort-by="id" primary-key="id" v-if="project[collection]" :items="project[collection]" :fields="fields">

      <template slot="name" slot-scope="row">
        <b-input v-model="row.item.name"/>
      </template>

      <template slot="home_address" slot-scope="row">
        <AddressField v-model="row.item.home_address" />
      </template>

      <template slot="address_source_name" slot-scope="row">
        <b-input v-model="row.item.address_source_name" />
      </template>

      <template slot="mass" slot-scope="row">
        <b-input v-model="row.item.mass" />
      </template>

      <template slot="starts_at" slot-scope="row">
        <b-form-input type="date" v-model="row.item.starts_at" />
      </template>

      <template slot="ends_at" slot-scope="row">
        <b-form-input type="date" v-model="row.item.ends_at" />
      </template>

      <template slot="is_default" slot-scope="row">
        <label>
          <input type="checkbox" class="check-custom toggle-switch" v-model="row.item.is_default">
          <span class="check-toggle"></span>
        </label>
      </template>

      <template slot="mode" slot-scope="row">
        <b-form-select v-model="row.item.mode" :options="$OPENFOOTPRINT_GLOBAL.transport_modes" />
      </template>

      <template slot="roundtrip" slot-scope="row">
        <label>
          <input type="checkbox" class="check-custom toggle-switch" v-model="row.item.roundtrip">
          <span class="check-toggle"></span>
        </label>
      </template>

      <template slot="address" slot-scope="row">
        <AddressField v-model="row.item.address" />
      </template>

      <template slot="from_address" slot-scope="row">
        <AddressField v-model="row.item.from_address" />
      </template>

      <template slot="to_address" slot-scope="row">
        <AddressField v-model="row.item.to_address" />
      </template>

      <template v-if="collection=='extras'" slot="kind" slot-scope="row">
        <b-form-select v-model="row.item.kind" :options="extras_kinds"></b-form-select>
      </template>

      <template v-if="collection=='extras'" slot="params" slot-scope="row">
        <b-input v-model="row.item.param_f1" />
      </template>

      <template slot="actions" slot-scope="row">
        <div class="btn-action" @click="deleteRow(row)" ><v-icon name="trash" /></div>
      </template>

    </b-table>

    <b-button @click="addRow()">Add new</b-button>
    <b-button @click="saveAll()" variant="primary">Save all <b-spinner v-if="loading_save" small type="grow" /></b-button>
    <b-button @click="deleteAll()" variant="danger">Delete all</b-button>

  </div>
</template>

<script>
import AddressField from "../components/addressfield"
import Vue from 'vue'

export default {
  props: ['collection', 'fields', 'newitemtemplate'],
  data() {
    return {
      loading_save: false,

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
  mounted() {
    this.fieldkeys = this.fields.map((f) => { return f.key });
  },
  methods: {
    addRow() {
      var newitem = JSON.parse(JSON.stringify(this.newitemtemplate));
      newitem["id"] = "new_"+Math.random();

      // TODO this shouldn't be hardcoded here
      if (this.collection == "locations") {
        newitem["is_default"] = (this.project[this.collection].length==0)
      }

      this.project[this.collection].push(newitem);

      Vue.nextTick(() => {
        var newInput = this.$refs.table_main.$el.querySelector("tr:last-child input[type=text]");
        if (newInput) newInput.focus();
      });
    },
    deleteRow(row) {
      // TODO: investigate why splice doesn't behave correctly
      this.project[this.collection].splice(row.index,1);
    },
    deleteAll() {
      this.$http.post("/api/project/"+this.project.id+"/delete_"+this.collection).then((response) => {
        this.refreshProject();
      });
    },
    saveAll() {
      this.loading_save = true;
      this.$http.post("/api/project/"+this.project.id+"/set_"+this.collection, this.project[this.collection]).then((response) => {
        this.refreshProject(() => {
          this.loading_save = false;
        });
      });
    },
  },
  components: {
    AddressField
  }
}
</script>

<style lang="scss" scoped>

</style>