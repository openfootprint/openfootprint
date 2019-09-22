from openfootprint.core.models import ActivePlugin
import json
import os

PLUGIN_DIRECTORY = "/app/plugins/"


def discover_available_plugins(project_id):

    enabled_plugins = {
        plugin["slug"]: plugin
        for plugin in ActivePlugin.objects.filter(
            enabled=True, project=project_id
        ).values("slug", "config")
    }

    plugins = []
    # TODO cache on production
    for plugin_slug in os.listdir(PLUGIN_DIRECTORY):
        if (
            not os.path.isdir(os.path.join(PLUGIN_DIRECTORY, plugin_slug))
            or plugin_slug == "__pycache__"
            or plugin_slug.startswith(".")
        ):
            continue
        try:
            with open(
                os.path.join(PLUGIN_DIRECTORY, plugin_slug, "plugin.json"), "r"
            ) as json_file:
                plugin_metadata = json.load(json_file)
        except Exception as e:
            # TODO better error reporting
            print("Couldn't load plugin %s : %s" % (plugin_slug, e))

        plugin_data = {"slug": plugin_slug}
        for whitelisted_key in (
            "type",
            "name",
            "url",
            "description",
            "config_schema",
            "thumbnail",
            "version",
        ):
            if plugin_metadata.get(whitelisted_key):
                plugin_data[whitelisted_key] = plugin_metadata[whitelisted_key]

        if plugin_slug in enabled_plugins:
            plugin_data["enabled"] = True
            plugin_data["config"] = (
                json.loads(enabled_plugins[plugin_slug].get("config", "{}")) or {}
            )

        plugins.append(plugin_data)

    # TODO warning when active plugin is not available anymore

    return plugins


class BasePlugin:
    def __init__(self):
        self.init()

    def init(self):
        pass


class FootprintPlugin(BasePlugin):
    def compute_transport_footprint(self, emission_source):
        raise NotImplementedError

    def compute_hotel_footprint(self, emission_source):
        raise NotImplementedError

    def compute_meal_footprint(self, emission_source):
        raise NotImplementedError

    def compute_extra_footprint(self, emission_source):
        raise NotImplementedError


class AttendeePlugin(BasePlugin):
    pass


class ReportTemplatePlugin(BasePlugin):
    pass
