<template>
  <div class="base">
    <div class="map" v-show="hasData" />
    <div class="nodata" v-if="!hasData">
      <div>No data yet...</div>
    </div>
  </div>
</template>

<script>
import L from "leaflet";
import Vue from "vue";
import "@elfalem/leaflet-curve";

import "leaflet/dist/leaflet.css";

L.Icon.Default.prototype.options.imagePath = "/static/images/leaflet/";

export default {
  data() {
    return {
      hasData: false
    };
  },
  props: {
    locations: Array,
    transports: Array
  },
  watch: {
    locations() {
      this.reDraw();
    },
    transports() {
      this.reDraw();
    }
  },
  mounted() {
    this.map = L.map(this.$el.querySelector(".map"));

    // TODO: do we need to wait until we have bounds to do that?
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: ' <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(this.map);

    this.reDraw();
  },
  methods: {
    reDraw() {
      this.map.invalidateSize();
      this.hasData = false;

      if ((this.locations || []).length > 0) {
        var markers = [];
        var customMarker = L.icon({
          iconUrl: "/static/images/leaflet/custom-marker.png",
          iconSize: [32, 40], // size of the icon
          iconAnchor: [16, 40] // point of the icon which will correspond to marker's location
        });
        this.locations.forEach(location => {
          if ((location.address || {}).status != "geocoded") return;
          markers.push(
            L.marker([location.address.latitude, location.address.longitude], {
              icon: customMarker
            })
          );
        });
        this.hasData = markers.length > 0;
        this.drawMarkers(markers);
      }

      if ((this.transports || []).length > 0) {
        var lines = [];
        this.transports.forEach(transport => {
          if (
            (transport.from_address || {}).status != "geocoded" ||
            (transport.to_address || {}).status != "geocoded"
          )
            return;
          lines.push([
            [transport.from_address.latitude, transport.from_address.longitude],
            [transport.to_address.latitude, transport.to_address.longitude]
          ]);
        });
        this.hasData = lines.length > 0;
        this.drawCurvedLines(lines);
      }
    },
    drawMarkers(markers) {
      if (markers.length === 0) return;
      var mapMarkers = new L.featureGroup(markers);

      Vue.nextTick(() => {
        this.map.fitBounds(mapMarkers.getBounds(), { maxZoom: 12 });
        mapMarkers.addTo(this.map);
      });
    },
    drawCurvedLines(lines) {
      if (lines.length === 0) return;
      var polyline = L.polyline(lines);
      this.map.fitBounds(polyline.getBounds(), { maxZoom: 12 });

      lines.forEach(line => {
        var center = L.polyline([line])
          .getBounds()
          .getCenter();
        center.lat += (line[0][0] - center.lat) * 0.5;
        center.lng -= (line[0][1] - center.lng) * 0.5;

        L.curve([
          "M",
          [line[0][0], line[0][1]],
          "Q",
          [center.lat, center.lng],
          [line[1][0], line[1][1]]
        ]).addTo(this.map);
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.base {
  border-radius: 14px;
  overflow: hidden;
}
.map {
  height: 100%;
}
.nodata {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  background: white;
}
</style>
