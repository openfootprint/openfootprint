<template>
  <div>

    <div class="datatable_block" :class="collection">
      <div class="table_actions">
        <div class="table_actions_buttons">
          <b-button @click="addRow()" variant="secondary">Add new</b-button>
          <b-dropdown right variant="outline-secondary">
            <b-dropdown-item @click="saveAll()"><unicon name="sync"></unicon>Save all <b-spinner v-if="loading_save" small type="grow" /></b-dropdown-item>
            <b-dropdown-item @click="deleteAll()"><unicon name="trash-alt"></unicon>Delete all</b-dropdown-item>
          </b-dropdown>
        </div>
        <div class="clearfix"></div>
      </div>

      <b-table ref="table_main" sort-by="id" primary-key="id" v-show="project[collection]" :items="project[collection]" :fields="fields">

        <template slot="checkbox" slot-scope="row">
          <label class="checkbox_label">
            <input type="checkbox">
            <span class="checkmark"></span>
          </label>
        </template>

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

        <template slot="address" slot-scope="row">
          <AddressField v-model="row.item.address" />
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
            <input data-bypass-autosave="1" @change="removeAllDefault(row.item.id)" type="checkbox" class="check-custom toggle-switch" v-model="row.item.is_default">
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
            <li v-if="collection=='reports'"><a :href="'/reports/'+row.item.id+'/'" target="_blank"><span class="icon icon-eye"><unicon name="eye"></unicon></span></a></li>
            <li @click="deleteRow(row)"><span class="icon icon-trash"><unicon name="trash-alt"></unicon></span></li>
          </ul>
        </template>

        <template slot="report_name" slot-scope="row">
          <p>Report name</p>
        </template>

      </b-table>

      <div class="pagination" v-if="collection!='locations'">
        <p><span class="cp_pagination">1 – 100</span> of <span class="total_pagination">19,154</span></p>
        <ul>
          <li><unicon name="angle-left"></unicon></li>
          <li><unicon name="angle-right"></unicon></li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import AddressField from "../components/addressfield"
import Vue from 'vue'
import { pickById, deleteById } from '../utils'

export default {
  props: {
    'collection': String,
    'fields': Array,
    'newitemtemplate': Object,
    'autosave': Boolean
  },
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
    if (this.autosave) {
      this.$refs.table_main.$el.addEventListener("change", (evt) => {
        if (evt.target.getAttribute("data-bypass-autosave")) return;
        this.saveAll();
      });
    }
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

      // TODO: there must be a better way to do this but splice() wasn't behaving correctly.
      Vue.set(this.project, this.collection, deleteById(this.project[this.collection], row.item.id));

      this.$http.post("/api/project/"+this.project.id+"/generic_delete_row", {id:row.item.id, collection:this.collection}).then((response) => {
      });
    },
    deleteAll() {
      this.$http.post("/api/project/"+this.project.id+"/set_"+this.collection, []).then((response) => {
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
    saveOne(id) {
      var obj = pickById(this.project[this.collection], id);
      if (!obj) return;
      this.$http.post("/api/project/"+this.project.id+"/set_"+this.collection, ["partial", obj]).then((response) => {

      });
    },
    removeAllDefault(from_id) {
      this.project[this.collection].forEach((elt) => {
        if (elt.id == from_id) return;
        elt.is_default = false;
      });
      this.saveAll();
    }
  },
  components: {
    AddressField
  }
}
</script>

<style lang="scss" scoped>

</style>