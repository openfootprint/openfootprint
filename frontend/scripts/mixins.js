import { mapState } from 'vuex'


// https://vuejs.org/v2/guide/mixins.html

var GlobalMixin = {
  computed: mapState({
    project: "project"
  }),
  methods: {
    refreshProject(callback) {
      // TODO loading
      this.$http.get("/api/project/"+this.project.id).then((response) => {
        response.data.locations.forEach((loc) => {
          loc.address_source_name = (loc.address||{}).source_name;
        });
        // TODO use vuex mutation
        this.$store.state.project = response.data;
        if (callback) callback();
      });
    }
  }
};

var ProjectMixin = {

};


export {
  GlobalMixin,
  ProjectMixin
};