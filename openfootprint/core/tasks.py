from config import celery_app
from .models import Location
import importlib


EMISSION_HANDLERS_BY_SOURCE = {
  "transports": "compute_transports_footprint",
  "extra": "compute_extras_footprint"
}


@celery_app.task(bind=True)
def geocode_location(self, location_id):
    location = Location.objects.get(pk=location_id)
    location.geocode(save=True)

@celery_app.task(bind=True)
def compute_footprint(self, project_json, provider="openfootprint.core.providers.carbonkit"):

    footprint_provider = importlib.import_module(provider).FootprintProvider()

    for emission_source in project_json:
      emission_source.setdefault("f", {})["co2e"] = getattr(footprint_provider, EMISSION_HANDLERS_BY_SOURCE[emission_source["type"]])(emission_source)

    return project_json
