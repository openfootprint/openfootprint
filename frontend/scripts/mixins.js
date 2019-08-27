import { mapState } from "vuex";

// https://vuejs.org/v2/guide/mixins.html
var uuid = 0;

var computed = mapState({
  project: "project"
});

computed["project_api_root"] = function() {
  return "/api/project/" + this.project.id;
};

var GlobalMixin = {
  beforeCreate() {
    this.uuid = uuid.toString();
    uuid += 1;
  },
  computed: computed,
  methods: {
    refreshProject(callback) {
      // TODO loading
      this.$http.get(this.project_api_root).then(response => {
        /*
        response.data.locations.forEach((loc) => {
          loc.address_source_name = (loc.address||{}).source_name;
        });
        */

        // TODO use vuex mutation
        this.$store.state.project = response.data;
        if (callback) callback();
      });
    }
  }
};

var ProjectMixin = {};

export { GlobalMixin, ProjectMixin };
