import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import axios from 'axios'

// Icons
// TODO: only import specific ones cf https://github.com/Justineo/vue-awesome
import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon'

// https://bootstrap-vue.js.org/docs
import '../styles/bootstrap.scss'

import App from './app'
import router from './router'


Vue.component('v-icon', Icon)

Vue.prototype.$http = axios

Vue.use(BootstrapVue)

new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})