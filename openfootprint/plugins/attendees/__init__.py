import os
import json


class Plugin():
    name = ""
    config_schema = {}

    def __init__(self):
        config_path = "config.%s.json" % self.name
        # Load configs
        if os.path.exists(config_path):
            with open(config_path, "r") as json_file:
                cwd = os.getcwd()
                self.config = json.load(json_file)
