<template>
  <div class="base">
  </div>
</template>

<script>

import L from "leaflet"
import '@elfalem/leaflet-curve'

import 'leaflet/dist/leaflet.css';

L.Icon.Default.prototype.options.imagePath="/static/images/leaflet/";

export default {
  props: {
    "locations": Array,
    "transports": Array
  },
  mounted() {
    this.map = L.map(this.$el);

    // TODO: do we need to wait until we have bounds to do that?
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: ' <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(this.map);

    this.reDraw();
  },
  watch: {
    locations(val) {
      this.reDraw();
    },
    transports(val) {
      this.reDraw();
    }
  },
  methods: {
    reDraw() {

      this.map.invalidateSize();

      if ((this.locations||[]).length > 0) {
        var markers = [];
        var customMarker = L.icon({
          iconUrl: '/static/images/leaflet/custom-marker.png',

          iconSize:     [32, 40], // size of the icon
          iconAnchor:   [16, 40], // point of the icon which will correspond to marker's location
        });
        this.locations.forEach((location) => {
          if ((location.address||{}).status != "geocoded") return;
          markers.push(L.marker([location.address.latitude, location.address.longitude], {icon: customMarker}));
        });
        this.drawMarkers(markers);
      }

      if ((this.transports||[]).length > 0) {
        var lines = [];
        this.transports.forEach((transport) => {
          if ((transport.from_address||{}).status != "geocoded" || (transport.to_address||{}).status != "geocoded") return;
          lines.push([[transport.from_address.latitude, transport.from_address.longitude], [transport.to_address.latitude, transport.to_address.longitude]]);
        });
        this.drawCurvedLines(lines);
      }

    },
    drawMarkers(markers) {
      var mapMarkers = new L.featureGroup(markers);
      this.map.fitBounds(mapMarkers.getBounds());
      mapMarkers.addTo(this.map);
    },
    drawCurvedLines(lines) {

      var polyline = L.polyline(lines);
      this.map.fitBounds(polyline.getBounds());

      lines.forEach((line) => {
        var center = L.polyline([line]).getBounds().getCenter();
        center.lat += (line[0][0] - center.lat) * 0.5
        center.lng -= (line[0][1] - center.lng) * 0.5

        L.curve([
          'M', [line[0][0], line[0][1]],
          'Q', [center.lat, center.lng], [line[1][0], line[1][1]]
        ]).addTo(this.map);

      });

    }
  }
};
</script>