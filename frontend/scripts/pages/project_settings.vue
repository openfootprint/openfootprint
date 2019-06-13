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
            v-model="$parent.project.starts_at"
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
            v-model="$parent.project.ends_at"
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
      main_location:((this.$parent.project.main_location||{}).address||{}).source_name||""
    }
  },
  methods:{
    onSubmit() {

      var data = {
        "name": this.$parent.project.name,
        "starts_at": this.$parent.project.starts_at,
        "ends_at": this.$parent.project.ends_at,
      };
      console.log(data);
      this.$http.post("/api/project/"+this.$parent.project.id+"/set_settings", data).then((response) => {
        this.$parent.refreshProject();
      });
    }
  }
}
</script>

<style scoped>

</style>