<template>
  <div>

    <h2>Settings</h2>

    <b-form @submit.prevent.stop="onSubmit">
      <b-form-group
        label="Name:"
        label-for="settings-project-name"
        description="Name of this project."
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
        label="Main event location:"
        label-for="settings-project-main-location"
        description="Main location where the event takes place"
      >
        <b-form-input
          id="settings-project-main-location"
          v-model="main_location"
          type="text"
          placeholder="Address..."
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
        "name": this.$parent.project.name
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