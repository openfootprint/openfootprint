<template>
  <div>

    <b-table ref="table_main" sort-by="id" primary-key="id" v-if="project[collection]" :items="project[collection]" :fields="fields">

      <template slot="name" slot-scope="row">
        <div v-if="collection!='reports'">
          <b-input v-model="row.item.name"/>
        </div>
        <div v-else>
          <b-link :to="{'name':'project_report', 'params': {'report_id': row.item.id}}">{{row.item.name}}</b-link>
        </div>
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
        <ul class="btn-action">
          <li v-if="collection=='reports'"><a :href="'/report/'+row.item.id+'/'" target="_blank"><span class="icon icon-eye"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="22"><path d="M21.92,11.6C19.9,6.91,16.1,4,12,4S4.1,6.91,2.08,11.6a1,1,0,0,0,0,.8C4.1,17.09,7.9,20,12,20s7.9-2.91,9.92-7.6A1,1,0,0,0,21.92,11.6ZM12,18c-3.17,0-6.17-2.29-7.9-6C5.83,8.29,8.83,6,12,6s6.17,2.29,7.9,6C18.17,15.71,15.17,18,12,18ZM12,8a4,4,0,1,0,4,4A4,4,0,0,0,12,8Zm0,6a2,2,0,1,1,2-2A2,2,0,0,1,12,14Z"/></svg></span></a></li>
          <li @click="deleteRow(row)"><span class="icon icon-trash"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18"><path d="M10,18a1,1,0,0,0,1-1V11a1,1,0,0,0-2,0v6A1,1,0,0,0,10,18ZM20,6H16V5a3,3,0,0,0-3-3H11A3,3,0,0,0,8,5V6H4A1,1,0,0,0,4,8H5V19a3,3,0,0,0,3,3h8a3,3,0,0,0,3-3V8h1a1,1,0,0,0,0-2ZM10,5a1,1,0,0,1,1-1h2a1,1,0,0,1,1,1V6H10Zm7,14a1,1,0,0,1-1,1H8a1,1,0,0,1-1-1V8H17Zm-3-1a1,1,0,0,0,1-1V11a1,1,0,0,0-2,0v6A1,1,0,0,0,14,18Z"/></svg></span></li>
        </ul>
      </template>

      <template slot="report_name" slot-scope="row">
        <p>Report name</p>
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