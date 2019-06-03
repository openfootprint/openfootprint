import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import axios from 'axios'

// Icons
import 'vue-awesome/icons/trash'
import 'vue-awesome/icons/regular/times-circle'
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