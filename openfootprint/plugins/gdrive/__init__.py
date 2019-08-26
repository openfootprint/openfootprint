from openfootprint.plugins.attendees import Plugin as BasePlugin


class Plugin(BasePlugin):
    name = "Google drive"
    config_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "api_key": {
                "type": "string",
                "title": "Grive API key",
                # "format": "uri"
            }
        }
    }