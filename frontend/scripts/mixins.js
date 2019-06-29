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
        response.data.reports = [
          { name: "Report #1", report_template: "Template rp1", report_date:"18/06/2019", id:"1"},
          { name: "Report #2", report_template: "Template rp1", report_date:"20/06/2019", id:"2"}
        ];
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