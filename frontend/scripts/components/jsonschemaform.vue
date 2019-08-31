<template>
  <b-form @submit.prevent.stop="submit">
    <b-alert v-for="(error, i) in errors" :key="i" show dismissible variant="danger">
      {{ error.dataPath }}: {{ error.message }}
    </b-alert>

    <slot name="pre_fields" />

    <div v-for="(property, key) in schema.properties" :key="key">
      <b-form-group :label="property.title" :label-for="'_jsf_' + uuid + '_' + key">
        <b-form-file
          v-if="(property.attrs || {}).type == 'file'"
          :id="'_jsf_' + uuid + '_' + key"
          :data-key="key"
          :required="(schema.required || []).indexOf(key) >= 0"
          @change="onFileChange($event, key)"
        />

        <b-form-input
          v-else
          :id="'_jsf_' + uuid + '_' + key"
          v-model="currentValue[key]"
          :type="{ uri: 'text' }[property.format] || property.format || 'text'"
          :required="(schema.required || []).indexOf(key) >= 0"
          autocomplete="off"
        />
      </b-form-group>
    </div>

    <b-button type="submit" variant="primary">
      Submit <b-spinner v-if="submitting" small type="grow" />
    </b-button>
  </b-form>
</template>

<script>
import Ajv from "ajv";

export default {
  props: ["schema", "value", "submitting"],
  data() {
    return {
      currentValue: JSON.parse(JSON.stringify(this.value)),
      errors: []
    };
  },
  watch: {
    value() {
      this.currentValue = JSON.parse(JSON.stringify(this.value));
    }
  },
  methods: {
    submit() {
      var ajv = new Ajv({
        allErrors: true,
        jsonPointers: false,
        format: "full"
      });
      var validated = ajv.validate(this.schema, this.currentValue);
      this.errors = ajv.errors || [];
      if (!validated) {
        return;
      }
      this.$emit("input", this.currentValue);
      this.$emit("submit", this.currentValue);
    },
    onFileChange(evt, key) {
      // We upload files right after they have been selected in the browser

      if (!evt.target.files || evt.target.files.length === 0) return;

      var formData = new FormData();
      formData.append("file", evt.target.files[0]);
      this.$http
        .post(this.project_api_root + "/upload_file", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(response => {
          this.currentValue[key] = {
            id: response.data.file.id,
            url: response.data.file.url
          };
        });
    }
  }
};
</script>
