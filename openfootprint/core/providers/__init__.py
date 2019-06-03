import json


class FootprintProvider():
    name = None

    def __init__(self):
        # Load configs
        with open("config.%s.json" % self.name, "r") as json_file:
            import os
            cwd = os.getcwd()
            print("JSON", json_file, cwd)
            self.config = json.load(json_file)

    def compute_transports_footprint(self, emission_source):
        raise NotImplementedError

    def compute_extra_footprint(self, emission_source):
        raise NotImplementedError
