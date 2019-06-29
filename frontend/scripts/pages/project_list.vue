<template>
  <div>
    <ul v-for="project in projects" :key="project.id">
      <li><b-link :to='{"name": "project_home", "params": {"id": project.id}}'>{{project.name}}</b-link></li>
    </ul>
  </div>
</template>


<script>

import Vue from 'vue'

export default {
  data () {
    return {
      projects: []
    };
  },
  created() {
    this.$http.get("/api/project").then((response) => {
      this.projects = response.data;
    });
  },
  mounted() {

  },
  methods: {

  },
  components: {
  }
}
</script>


<style lang="scss" scoped>
  
</style>