<template>
  <div>

    <a class="btn" href="/#/new">Create new project</a>

    <ul v-for="project in projects">
      <li><a :href="'/#/project/'+project.id">{{project.name}}</a></li>
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