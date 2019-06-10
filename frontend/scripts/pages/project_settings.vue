<template>
  <div>

    <h2>Settings</h2>

    <b-form @submit.prevent.stop="onSubmit">
      <b-form-group
        label="Project name:"
        label-for="settings-project-name"
      >
        <b-form-input
          id="settings-project-name"
          v-model="$parent.project.name"
          type="text"
          required
          placeholder="Project name"
        ></b-form-input>
      </b-form-group>

      <b-form-group
        v-if="$parent.project.kind=='event'"
        label="Event start date:"
        label-for="settings-project-start-date"
      >
        <b-form-input
          id="settings-project-start-date"
          v-model="starts_at"
          type="date"
          placeholder="Start date..."
        ></b-form-input>
      </b-form-group>

      <b-form-group
        v-if="$parent.project.kind=='event'"
        label="Event end date:"
        label-for="settings-project-end-date"
      >
        <b-form-input
          id="settings-project-end-date"
          v-model="ends_at"
          type="date"
          placeholder="End date..."
        ></b-form-input>
      </b-form-group>

      <b-button type="submit" variant="primary">Submit</b-button>
    </b-form>
  </div>
</template>

<script>

export default {
  data () {
    return {
      main_location:((this.$parent.project.main_location||{}).address||{}).source_name||""
    }
  },
  methods:{
    onSubmit() {
      var data = {
        "main_location": this.main_location,
        "name": this.$parent.project.name,
        "start_at": this.$parent.project.start_at,
        "ends_at": this.$parent.project.ends_at,
      };
      this.$http.post("/api/project/"+this.$parent.project.id+"/set_settings", data).then((response) => {
        this.$parent.refreshProject();
      });
    }
  }
}
</script>

<style scoped>

</style>