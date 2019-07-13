<template>
  <div>
    <h2>Settings</h2>

    <div class="row">
      <json-schema-form :value="values" :schema="schema" @submit="onSubmit" :submitting="submitting" class="col-lg-6" />
    </div>
  </div>
</template>

<script>

import JsonSchemaForm from "../components/jsonschemaform"

export default {
  data () {
    return {
      "submitting": false
    }
  },
  computed:{
    values() {
      return {
        "name": this.project.name,
        "starts_at": this.project.starts_at,
        "ends_at": this.project.ends_at
      }
    },
    schema() {
      var required = ["name"];
      var properties = {
        "name": {
          "type": "string",
          "title": "Project name"
        }
      };

      if (this.project.kind="event") {
        properties["starts_at"] = {
          "type": "string",
          "title": "Event start date",
          "format": "date"
        };
        properties["ends_at"] = {
          "type": "string",
          "title": "Event start date",
          "format": "date"
        };
      }

      return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": required,
        "properties": properties,
        "additionalProperties": false
      };
    }
  },
  methods:{
    onSubmit(newValues) {
      this.submitting = true;
      this.$http.post("/api/project/"+this.project.id+"/set_settings", newValues).then((response) => {
        this.submitting = false;
        this.$parent.refreshProject();
      });
    }
  },
  components: {
    JsonSchemaForm
  }
}
</script>

<style scoped>

</style>