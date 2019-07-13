<template>
  <div>
    <b-form @submit.prevent.stop="submit" :class="className">

      <ul style="color:red;" v-if="errors.length">
        <li v-for="error in errors">
          {{error}}
        </li>
      </ul>

      <div v-for="(property, key) in schema.properties">
        <b-form-group
          v-if="property.type=='string'"
          :label="property.title"
          :label-for="'_jsf_'+uuid+'_'+key"
        >
          <b-form-input
            :id="'_jsf_'+uuid+'_'+key"
            :type="property.format||'text'"
            v-model="currentValue[key]"
            :required="schema.required.indexOf(key)>=0"
          />
        </b-form-group>

      </div>

      <b-button type="submit" variant="primary">Submit <b-spinner v-if="submitting" small type="grow" /></b-button>

    </b-form>
  </div>
</template>



<script>
import Vue from 'vue'
import Ajv from 'ajv'

export default {
  props: ["schema", "className", "value", "submitting"],
  data () {
    return {
      currentValue: {},
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
    }
  }
};

</script>