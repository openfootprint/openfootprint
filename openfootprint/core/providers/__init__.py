import os
import json


class FootprintProvider():
    name = ""

    def __init__(self):
        config_path = "config.%s.json" % self.name
        # Load configs
        if os.path.exists(config_path):
            with open(config_path, "r") as json_file:
                cwd = os.getcwd()
                self.config = json.load(json_file)

    def compute_transport_footprint(self, emission_source):
        raise NotImplementedError

    def compute_hotel_footprint(self, emission_source):
        raise NotImplementedError

    def compute_meal_footprint(self, emission_source):
        raise NotImplementedError

    def compute_extra_footprint(self, emission_source):
        raise NotImplementedError
