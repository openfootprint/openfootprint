import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import axios from 'axios'


// https://bootstrap-vue.js.org/docs
import '../styles/bootstrap.scss'

// Leaflet
// import L from 'leaflet';

// import 'leaflet/dist/leaflet.css';

// import marker from 'leaflet/dist/images/marker-icon.png';
// import marker2x from 'leaflet/dist/images/marker-icon-2x.png';
// import markerShadow from 'leaflet/dist/images/marker-shadow.png';

// delete L.Icon.Default.prototype._getIconUrl;

// L.Icon.Default.mergeOptions({
//     iconRetinaUrl: marker2x,
//     iconUrl: marker,
//     shadowUrl: markerShadow
// });


import {GlobalMixin} from "./mixins"

import App from './app'

// Icons

import Unicon from 'vue-unicons'
import { uniHomeAlt, uniChart, uniChartLine, uniBoltAlt, uniCog, uniTicket, uniBriefcaseAlt, uniBuilding, uniTrashAlt } from 'vue-unicons/src/icons'

Unicon.add([uniHomeAlt, uniChart, uniChartLine, uniBoltAlt, uniCog, uniTicket, uniBriefcaseAlt, uniBuilding, uniTrashAlt])


// import { uniTicket, uniBriefcaseAlt, uniBuilding, uniHomeAlt, uniChart, uniChartLine, uniCog, uniRedo, uniTimesCircle, uniEditAlt, uniCloudUpload, uniMap, uniDownArrow, uniListUl, uniCheck, uniEye, uniTrashAlt, uniBoltAlt } from 'vue-unicons/src/icons'
// Unicon.add([uniTicket, uniBriefcaseAlt, uniBuilding, uniHomeAlt, uniChart, uniChartLine, uniCog, uniRedo, uniTimesCircle, uniEditAlt, uniCloudUpload, uniMap, uniDownArrow, uniListUl, uniCheck, uniEye, uniTrashAlt, uniBoltAlt])
Vue.use(Unicon)

Vue.prototype.$http = axios
Vue.prototype.$OPENFOOTPRINT_GLOBAL = JSON.parse(document.getElementById("OPENFOOTPRINT_GLOBAL").textContent);
Vue.prototype.$OPENFOOTPRINT_GLOBAL["transport_modes"].unshift({"value": null, "text":""});

Vue.use(BootstrapVue)

Vue.mixin(GlobalMixin)

new Vue(App);