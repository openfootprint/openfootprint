import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import axios from 'axios'

// Icons
import 'vue-awesome/icons/trash'
import 'vue-awesome/icons/regular/times-circle'
import Icon from 'vue-awesome/components/Icon'

// https://bootstrap-vue.js.org/docs
import '../styles/bootstrap.scss'

import {GlobalMixin} from "./mixins"

import App from './app'

Vue.prototype.$http = axios
Vue.prototype.$OPENFOOTPRINT_GLOBAL = JSON.parse(document.getElementById("OPENFOOTPRINT_GLOBAL").textContent);
Vue.prototype.$OPENFOOTPRINT_GLOBAL["transport_modes"].unshift({"value": null, "text":""});

Vue.component('v-icon', Icon)

Vue.use(BootstrapVue)

Vue.mixin(GlobalMixin)

new Vue(App);