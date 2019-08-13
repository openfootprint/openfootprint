from rest_framework import serializers
from .models import Project, Extra, Transport, Report, Person, Tag, Location, Address, Hotel, Meal, File, ActivePlugins
import json
import os
import importlib

# TODO: filter fields properly

class ExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extra
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("source_name", "source_country", "id", "latitude", "longitude", "country", "status")


class LocationSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False, read_only=True)

    class Meta:
        model = Location
        fields = '__all__'


class HotelSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False, read_only=True)

    class Meta:
        model = Hotel
        fields = '__all__'


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'


class TransportSerializer(serializers.ModelSerializer):
    to_address = AddressSerializer(many=False, read_only=True)
    from_address = AddressSerializer(many=False, read_only=True)

    class Meta:
        model = Transport
        fields = '__all__'


class ActivePluginsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivePlugins
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep["config"] = json.loads(rep.get("config") or "{}") or {}

        # TODO: move to a proper plugin
        rep["config_schema"] = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "header_image": {
                    "type": "object",
                    "title": "Header image",
                    "attrs": {
                        "type": "file"
                    },
                    "properties": {
                        "id": {
                            "type": "number"
                        }
                    }
                },
                "website_url": {
                    "type": "string",
                    "title": "Event website URL",
                    "format": "uri"
                }
            }
        }

        return rep


class PersonSerializer(serializers.ModelSerializer):

    home_address = AddressSerializer(many=False, read_only=True)

    class Meta:
        model = Person
        fields = '__all__'


class ProjectSerializerFull(serializers.ModelSerializer):
    extras = ExtraSerializer(many=True, read_only=True)
    transports = TransportSerializer(many=True, read_only=True)
    active_plugins = ActivePluginsSerializer(many=True, read_only=True)
    reports = ReportSerializer(many=True, read_only=True)
    people = PersonSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    locations = LocationSerializer(many=True, read_only=True)
    meals = MealSerializer(many=True, read_only=True)
    hotels = HotelSerializer(many=True, read_only=True)

    starts_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    ends_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")

    class Meta:
        model = Project
        fields = '__all__'

    def to_representation(self, obj):
        data = super().to_representation(obj)
        installed_plugins = {plugin["slug"]: plugin for plugin in data["active_plugins"]}
        data.setdefault("plugins", [])
        for plugin_type in [d for d in os.listdir("/app/openfootprint/plugins/") if os.path.isdir(os.path.join("/app/openfootprint/plugins/", d))]:
            for plugin_slug in [d for d in os.listdir(os.path.join("/app/openfootprint/plugins/", plugin_type)) if os.path.isdir(os.path.join("/app/openfootprint/plugins/", plugin_type, d))]:
                if plugin_type in ["__pycache__", "templates"] or plugin_slug == "__pycache__":
                    continue
                imported_plugin = importlib.import_module("openfootprint.plugins.%s.%s" % (plugin_type, plugin_slug)).Plugin()
                plugin_data = {
                    "slug": plugin_slug,
                    "type": plugin_type,
                    "config_schema": imported_plugin.config_schema,
                    "name": imported_plugin.name
                }
                if plugin_slug in installed_plugins:
                    plugin_data["installed"] = True
                    plugin_data["config"] = json.loads(installed_plugins[plugin_slug].get("config", "{}")) or {}

                data['plugins'].append(plugin_data)

        return data


class ProjectSerializerList(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'name', 'kind')
