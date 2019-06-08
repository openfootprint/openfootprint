from config import celery_app
from .models import Address
import importlib


EMISSION_HANDLERS_BY_SOURCE = {
  "transports": "compute_transports_footprint",
  "extras": "compute_extras_footprint"
}


@celery_app.task(bind=True)
def geocode_address(self, address_id):
    print("Geoloc %s" % address_id)
    print(list(Address.objects.all()))
    address = Address.objects.get(pk=int(address_id))
    address.geocode()

@celery_app.task(bind=True)
def compute_footprint(self, project_json, provider="openfootprint.core.providers.carbonkit"):

    footprint_provider = importlib.import_module(provider).FootprintProvider() # type: ignore

    for emission_source in project_json:
      co2e = getattr(footprint_provider, EMISSION_HANDLERS_BY_SOURCE[emission_source["type"]])(emission_source)
      emission_source.setdefault("f", {})["co2e"] = co2e * emission_source.get("weight", 1.0)

    return project_json
