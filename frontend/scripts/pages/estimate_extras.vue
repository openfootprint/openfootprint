<template>
  <div>
    <h2>Extras</h2>

    <DataTable
      ref="table_main"
      :fields="extras_fields"
      collection="extras"
      :newitemtemplate="{ kind: 'co2e' }"
    />
  </div>
</template>

<script>
import DataTable from "../components/datatable";

export default {
  components: {
    DataTable
  },
  data() {
    return {
      extras_fields: [
        {
          key: "name",
          label: "Name"
        },
        {
          key: "kind",
          label: "Type",
          class: "th_dropdown"
        },
        {
          key: "params",
          label: "Parameters"
        },
        {
          key: "actions",
          label: "",
          class: "th_actions"
        }
      ]
    };
  },
  methods: {}
};
</script>

<style lang="scss" scoped></style>
