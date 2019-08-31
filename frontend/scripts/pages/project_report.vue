<template>
  <div v-if="!item">
    Loading...
  </div>
  <div v-else>
    <div>
      <h2>
        <b-link :to="{ name: 'project_reports' }">
          Reports
        </b-link>
        / {{ item.name }}
      </h2>
      <div>
        <b-button :href="'/reports/' + item.id + '/'" target="_blank">
          Open report
        </b-button>
      </div>
      <div class="clearfix" />
    </div>

    <div>
      <json-schema-form
        :value="item.theme_config||{}"
        :schema="item.theme_config_schema"
        :submitting="submitting"
        @submit="onSubmit"
      >
        <template v-slot:pre_fields>
          <b-form-group label="Report name" label-for="_edit_report_name">
            <b-form-input id="_edit_report_name" v-model="item.name" required />
          </b-form-group>
        </template>
      </json-schema-form>
    </div>
  </div>
</template>

<script>
import JsonSchemaForm from "../components/jsonschemaform";
import { pickById } from "../utils";

export default {
  components: {
    JsonSchemaForm
  },
  data() {
    return {
      submitting: false
    };
  },
  computed: {
    item() {
      return pickById(this.project.reports, this.$route.params.report_id);
    }
  },
  methods: {
    onSubmit(newConfig) {
      this.submitting = true;
      this.item.config = newConfig;
      this.$http.post(this.project_api_root + "/set_reports", ["partial", this.item]).then(() => {
        this.submitting = false;
      });
    }
  }
};
</script>

<style lang="scss" scoped></style>
