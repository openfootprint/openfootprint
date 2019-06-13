<template>
  <div>

    <b-table ref="table_main"  striped primary-key="id" v-if="$parent.project.people" :items="$parent.project.people">

      <template slot="name" slot-scope="row">
        <b-input v-model="row.item.name"/>
      </template>

      <template slot="home_address" slot-scope="row">
        <AddressField v-model="row.item.home_address" />
      </template>

      <template slot="actions" slot-scope="row">
        <b-button @click="deleteRow(row)" ><v-icon name="trash" /></b-button>
      </template>
    </b-table>

    <b-button @click="addRow()">Add transport</b-button>
    <b-button @click="saveAll()" variant="primary">Save all <b-spinner v-if="loading_save" small type="grow" /></b-button>
    <b-button @click="deleteAll()" variant="danger">Delete all</b-button>

  </div>
</template>

<script>
export default {
  props: ['collection'],
  mounted() {
    this.items = this.$parent.project[this.collection]
  },
  methods: {
    addRow() {
      this.items.push({"id": "new_"+Math.random(), "from_address": {}, "to_address": {}});
      Vue.nextTick(() => {
        var newInput = this.$refs.table_main.$el.querySelector("tr:last-child input[type=text]");
        if (newInput) newInput.focus();
      });
    },
    deleteRow(row) {
      this.$refs.table_main.items.splice(row.index,1);
    },
    deleteAll() {
      this.$http.post("/api/project/"+this.$parent.project.id+"/delete_transports").then((response) => {
        this.$parent.refreshProject();
      });
    },
    saveAll() {
      this.loading_save = true;
      this.$http.post("/api/project/"+this.$parent.project.id+"/set_transports", this.$refs.table_main.items).then((response) => {
        this.$parent.refreshProject(() => {
          this.loading_save = false;
        });
      });
    },
  }
}
</script>

<style lang="scss" scoped>

</style>