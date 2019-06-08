from openfootprint.core.providers import FootprintProvider as BaseFootprintProvider
import requests
import os


class FootprintProvider(BaseFootprintProvider):
    name = "carbonkit"

    def __init__(self):
        BaseFootprintProvider.__init__(self)
        if "CARBONKIT_USERNAME" in os.environ:
            self.config["USERNAME"] = os.environ["CARBONKIT_USERNAME"]
        if "CARBONKIT_PASSWORD" in os.environ:
            self.config["PASSWORD"] = os.environ["CARBONKIT_PASSWORD"]

    def _do_requests(self, path):
        r = requests.get(
        "https://api.carbonkit.net/3.6/%s" % path,
        headers={
            "Accept": "application/json"
        },
        auth=(self.config["USERNAME"], self.config["PASSWORD"])
        )
        # TODO handle errors
        return r.json()

    def compute_transports_footprint(self, emission_source):
        path = "categories/Great_Circle_flight_methodology/calculation"\
               "?type=great+circle+route&values.isReturn=false&values.journeys=1"\
               "&values.lat1=%f&values.lat2=%f&values.long1=%f&values.long2=%f&values.passengers=1" % (
            emission_source["from_address"]["latitude"],
            emission_source["to_address"]["latitude"],
            emission_source["from_address"]["longitude"],
            emission_source["to_address"]["longitude"]
        )
        emmission = self._do_requests(path)
        if emmission.get("status") == "OK":
            for amount in emmission["output"]["amounts"]:
                if amount["type"] == "totalDirectCO2e":
                    return amount["value"] * 1000

        return -1

    def compute_extras_footprint(self, emission_source):
        if emission_source["kind"] == "co2e":
            return emission_source["param_f1"]
        return -1
