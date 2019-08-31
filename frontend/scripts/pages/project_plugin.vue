<template>
  <div v-if="!plugin">Loading...</div>
  <div v-else>
    <div>
      <div style="float:right;">
        <b-button v-if="plugin.enabled" @click="disablePlugin" variant="danger">Disable</b-button>
      </div>

      <h2><b-link :to="{ name: 'project_plugins' }">Plugins</b-link> / {{ plugin.name }}</h2>

      <p v-if="plugin.description">{{ plugin.description }}</p>
      <p v-if="plugin.url">
        <a :href="plugin.url" target="_blank">{{ plugin.url }}</a>
      </p>
    </div>

    <div v-if="plugin.enabled">
      <json-schema-form
        :value="plugin.config || {}"
        :schema="plugin.config_schema"
        @submit="onSubmit"
        :submitting="submitting"
      >
      </json-schema-form>
    </div>

    <b-button v-else @click="enablePlugin()">Enable</b-button>
  </div>
</template>

<script>
import JsonSchemaForm from "../components/jsonschemaform";
import { pickById, updateById } from "../utils";

export default {
  data() {
    return {
      submitting: false
    };
  },
  computed: {
    plugin() {
      return pickById(this.project.plugins, this.$route.params.plugin_slug, "slug");
    }
  },
  methods: {
    disablePlugin() {
      this.submitting = true;
      this.$http.post(this.project_api_root + "/remove_plugins", [this.plugin.slug]).then(() => {
        this.submitting = false;
        this.project.plugins = updateById(
          this.project.plugins,
          this.$route.params.plugin_slug,
          "slug",
          { enabled: false }
        );
        this.$router.push({ name: "project_plugins" });
      });
    },
    enablePlugin() {
      this.submitting = true;
      this.$http.post(this.project_api_root + "/set_plugins", [this.plugin]).then(() => {
        this.submitting = false;
        this.plugin.enabled = true;
      });
    },
    onSubmit(newConfig) {
      this.submitting = true;
      this.plugin.config = newConfig;
      this.$http.post(this.project_api_root + "/set_plugins", ["partial", this.plugin]).then(() => {
        this.submitting = false;
      });
    }
  },
  components: {
    JsonSchemaForm
  }
};
</script>

<style lang="scss" scoped></style>
