<template>

  <b-form @submit.prevent.stop="submit">

    <ul style="color:red;" v-if="errors.length">
      <li v-for="error in errors">
        {{error}}
      </li>
    </ul>

    <slot name="pre_fields"></slot>

    <div v-for="(property, key) in schema.properties">
      <b-form-group
        v-if="property.type=='string' || property.type=='number'"
        :label="property.title"
        :label-for="'_jsf_'+uuid+'_'+key"
      >

        <b-form-file
          v-if="(property.attrs||{}).type=='file'"
          :id="'_jsf_'+uuid+'_'+key"
          @change="onFileChange"
          :data-key="key"
          :required="(schema.required||[]).indexOf(key)>=0"
        />

        <b-form-input
          v-else
          :id="'_jsf_'+uuid+'_'+key"
          :type="{'uri': 'text'}[property.format]||property.format||'text'"
          v-model="currentValue[key]"
          :required="(schema.required||[]).indexOf(key)>=0"
        />

      </b-form-group>

    </div>

    <b-button type="submit" variant="primary">Submit <b-spinner v-if="submitting" small type="grow" /></b-button>

  </b-form>

</template>



<script>
import Vue from 'vue'
import Ajv from 'ajv'

export default {
  props: ["schema", "value", "submitting"],
  data () {
    return {
      currentValue: JSON.parse(JSON.stringify(this.value)),
      errors: []
    }
  },
  watch: {
    value() {
      this.currentValue = JSON.parse(JSON.stringify(this.value));
    }
  },
  methods: {
    submit() {
      var ajv = new Ajv({allErrors: true, jsonPointers: false, format: 'full'});
      var validated = ajv.validate(this.schema, this.currentValue);
      this.errors = ajv.errors || [];
      if (!validated) {
        return;
      }
      this.$emit('input', this.currentValue);
      this.$emit('submit', this.currentValue);
    },
    onFileChange(evt) {
      // We upload files right after they have been selected in the browser

      if (!evt.target.files || evt.target.files.length === 0) return;

      var formData = new FormData();
      formData.append("file", evt.target.files[0]);
      this.$http.post("/api/project/"+this.project.id+"/upload_file", formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
      }).then((response) => {
        this.currentValue[evt.target.getAttribute("data-key")] = response.data.file.id;
      })
    }
  }
};

</script>