<template>
  <div v-if="!item">
    Loading...
  </div>
  <div v-else>
    <div class="btns_actions">
      <h2>
        <b-link :to="{ name: 'project_plugins' }">
          Plugins
        </b-link>
        / {{ item.name }}
      </h2>
      <div class="btns">
        <b-button variant="danger" target="_blank">
          Uninstall plugin
        </b-button>
      </div>
      <div class="clearfix" />
    </div>

    <div>
      <json-schema-form
        :value="item.config"
        :schema="item.config_schema"
        :submitting="submitting"
        @submit="onSubmit"
      />
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
      return pickById(this.project.plugins, this.$route.params.plugin_slug, "slug");
    }
  },
  methods: {
    onSubmit(newConfig) {
      this.submitting = true;
      this.item.config = newConfig;
      this.$http.post(this.project_api_root + "/set_plugins", ["partial", this.item]).then(() => {
        this.submitting = false;
      });
    }
  }
};
</script>

<style lang="scss" scoped></style>
