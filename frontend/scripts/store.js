import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

// TODO: make it strict again
var debug = false; //process.env.NODE_ENV !== 'production'

var store = new Vuex.Store({
  state: {
    project: {}
  },
  mutations: {},
  strict: debug
});

export default store;
