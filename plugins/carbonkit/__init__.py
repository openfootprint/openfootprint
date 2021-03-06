from openfootprint.plugin import FootprintPlugin
from django.core.cache import caches
import requests
import os


class Plugin(FootprintPlugin):

    def init(self):
        self.config.setdefault("username", os.getenv("CARBONKIT_USERNAME"))
        self.config.setdefault("password", os.getenv("CARBONKIT_PASSWORD"))

    def _do_request(self, path):

        # TODO cache could be compressed and store only arguments+precise result
        # TODO have a self.cache scoped for the plugin
        if caches["default"].get(path):
            return caches["default"].get(path)

        r = requests.get(
            "https://api.carbonkit.net/3.6/%s" % path,
            headers={"Accept": "application/json"},
            auth=(self.config["username"], self.config["password"]),
        )
        # TODO handle errors

        resp = r.json()
        caches["default"].set(path, resp, timeout=24 * 3600)
        return resp

    def compute_transport_footprint(self, emission_source):
        path = (
            "categories/Great_Circle_flight_methodology/calculation"
            "?type=great+circle+route&values.isReturn=false&values.journeys=1"
            "&values.lat1=%f&values.lat2=%f&values.long1=%f&values.long2=%f&values.passengers=1"
            % (
                emission_source["from_address"]["latitude"],
                emission_source["to_address"]["latitude"],
                emission_source["from_address"]["longitude"],
                emission_source["to_address"]["longitude"],
            )
        )
        emmission = self._do_request(path)
        if emmission.get("status") == "OK":
            for amount in emmission["output"]["amounts"]:
                if amount["type"] == "totalDirectCO2e":
                    return amount["value"] * 1000 * emission_source["weight"]

        return -1

    def compute_hotel_footprint(self, emission_source):
        # https://gitlab.com/carbonkit/datasets/blob/master/business/buildings/hotel/generic/algorithm.js
        return 36.63 * 1000 * emission_source["nights"] * emission_source["weight"]

    def compute_meal_footprint(self, emission_source):

        # Just assume everything is cheese for now. (Also known as "the cheese method")
        # http://www.greeneatz.com/foods-carbon-footprint.html
        return 13.5 * emission_source["mass"] * emission_source["weight"]

    def compute_extra_footprint(self, emission_source):
        if emission_source["kind"] == "co2e":
            return emission_source["param_f1"]
        return -1
