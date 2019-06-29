<template>
  <div>
    <h2>Settings</h2>

    <div class="row">
      <b-form @submit.prevent.stop="onSubmit" class="col-lg-6">
        <b-form-group
          label="Project name:"
          label-for="settings-project-name"
        >
          <b-form-input
            id="settings-project-name"
            v-model="project.name"
            type="text"
            required
            placeholder="Project name"
          ></b-form-input>
        </b-form-group>

        <b-form-group
          v-if="project.kind=='event'"
          label="Event start date:"
          label-for="settings-project-start-date"
        >
          <b-form-input
            id="settings-project-start-date"
            v-model="project.starts_at"
            type="date"
            placeholder="Start date..."
          ></b-form-input>
        </b-form-group>

        <b-form-group
          v-if="project.kind=='event'"
          label="Event end date:"
          label-for="settings-project-end-date"
        >
          <b-form-input
            id="settings-project-end-date"
            v-model="project.ends_at"
            type="date"
            placeholder="End date..."
          ></b-form-input>
        </b-form-group>

        <b-button type="submit" variant="primary">Submit</b-button>
      </b-form>
    </div>
  </div>
</template>

<script>

export default {
  data () {
    return {
      main_location:((this.project.main_location||{}).address||{}).source_name||""
    }
  },
  methods:{
    onSubmit() {

      var data = {
        "name": this.project.name,
        "starts_at": this.project.starts_at,
        "ends_at": this.project.ends_at,
      };

      this.$http.post("/api/project/"+this.project.id+"/set_settings", data).then((response) => {
        this.$parent.refreshProject();
      });
    }
  }
}
</script>

<style scoped>

</style>