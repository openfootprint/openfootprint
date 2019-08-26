from openfootprint.core.models import ActivePlugins
import json
import os


class BasePlugin():
    
    def __init__(self):
        # Load configs
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as json_file:
                cwd = os.getcwd()
                self.config = json.load(json_file)
    
    @staticmethod
    def get_all_plugins():
        plugins = []
        installed_plugins = {plugin["slug"]: plugin for plugin in ActivePlugins.objects.values("slug", "config")}
        for plugin_slug in [d for d in os.listdir("/app/openfootprint/plugins/") if os.path.isdir(os.path.join("/app/openfootprint/plugins/", d))]:
            if plugin_slug == "__pycache__":
                continue
            with open(os.path.join("/app/openfootprint/plugins/", plugin_slug, "plugin.json"), "r") as json_file:
                plugin_config = json.load(json_file)
                plugin_data = {
                    "slug": plugin_slug,
                    "types": plugin_config["types"],
                    "config_schema": plugin_config["config_schema"],
                    "name": plugin_config["name"]
                }
                if plugin_slug in installed_plugins:
                    plugin_data["installed"] = True
                    plugin_data["config"] = json.loads(installed_plugins[plugin_slug].get("config", "{}")) or {}

                plugins.append(plugin_data)
        return plugins
        
class FootPrint(BasePlugin):
    def compute_transport_footprint(self, emission_source):
        raise NotImplementedError

    def compute_hotel_footprint(self, emission_source):
        raise NotImplementedError

    def compute_meal_footprint(self, emission_source):
        raise NotImplementedError

    def compute_extra_footprint(self, emission_source):
        raise NotImplementedError


class Attendees(BasePlugin):
    pass
