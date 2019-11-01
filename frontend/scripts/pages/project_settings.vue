<template>
  <div>
    <h2>Settings</h2>

    <div class="row">
      <json-schema-form
        :value="values"
        :schema="schema"
        :submitting="submitting"
        class="col-lg-6"
        @submit="onSubmit"
      />
    </div>

    <b-card
      border-variant="danger"
      header="Danger zone"
      header-border-variant="danger"
      header-text-variant="danger"
      style="margin-top:30px;"
    >
      <b-button variant="danger" @click="deleteProject">Delete project</b-button>
    </b-card>
  </div>
</template>

<script>
import JsonSchemaForm from "../components/jsonschemaform";

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
    values() {
      return {
        name: this.project.name,
        starts_at: this.project.starts_at,
        ends_at: this.project.ends_at
      };
    },
    schema() {
      var required = ["name"];
      var properties = {
        name: {
          type: "string",
          title: "Project name"
        }
      };

      if (this.project.kind == "event") {
        properties["starts_at"] = {
          type: "string",
          title: "Event start date",
          format: "date"
        };
        properties["ends_at"] = {
          type: "string",
          title: "Event end date",
          format: "date"
        };
      }

      return {
        $schema: "http://json-schema.org/draft-07/schema#",
        type: "object",
        required: required,
        properties: properties,
        additionalProperties: false
      };
    }
  },
  methods: {
    onSubmit(newValues) {
      this.submitting = true;
      this.$http.post(this.project_api_root + "/set_settings", newValues).then(() => {
        this.submitting = false;
        this.$parent.refreshProject();
      });
    },
    deleteProject() {
      this.submitting = true;
      if (window.confirm("Are you sure you want to permanently delete this project?")) {
        this.$http.post(this.project_api_root + "/delete").then(() => {
          this.submitting = false;
          this.$router.push("/");
        });
      }
    }
  }
};
</script>

<style scoped></style>
