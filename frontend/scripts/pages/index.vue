<template>
  <div>

    <b-button :to='{"name": "new"}'>Create new project</b-button>

    <ul v-for="project in projects" :key="project.id">
      <li><b-link :to='{"name": "project_home", "params": {"project_id": project.id}}'>{{project.name}}</b-link></li>
    </ul>
  </div>
</template>

<script>

export default {
  data () {
    return {
      projects: []
    }
  },
  created() {
    this.$http.get("/api/project").then((response) => {
      this.projects = response.data;
    });
  },
  components: {
  }
}
</script>

<style scoped>

</style>