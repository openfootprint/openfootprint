<template>
  <div>
    <b-link :to="{ name: 'index' }">
      <img
        src="/static/images/logo/logo_openfootprint.svg"
        alt="OpenFootprint"
        class="openfootprint_logo"
      />
    </b-link>

    <b-card header="Select a project" style="width:400px;margin:50px auto 30px auto;">
      <b-list-group>
        <b-list-group-item
          v-for="project in projects"
          :key="project.id"
          :to="{ name: 'project_home', params: { project_id: project.id } }"
          >{{ project.name }}</b-list-group-item
        >
      </b-list-group>

      <br />

      <b-button :to="{ name: 'new' }">
        Create new project
      </b-button>
    </b-card>
  </div>
</template>

<script>
export default {
  components: {},
  data() {
    return {
      projects: []
    };
  },
  created() {
    this.$http.get("/api/project").then(response => {
      this.projects = response.data;
    });
  }
};
</script>

<style lang="scss" scoped>
.openfootprint_logo {
  width: 300px;
  margin: 40px auto;
  display: block;
}
</style>
