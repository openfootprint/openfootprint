from config import celery_app
from .models import Address, Transport, Project
import importlib


EMISSION_HANDLERS_BY_SOURCE = {
  "transports": "compute_transports_footprint",
  "hotel": "compute_hotel_footprint",
  "food": "compute_food_footprint",
  "extras": "compute_extras_footprint"
}


@celery_app.task(bind=True)
def geocode_project(self, project_id):
    project = Project.objects.get(pk=int(project_id))

    # 1. Try geocoding all addresses
    for address in project.iter_adresses():
        address.geocode()

    # 2. Guess modes of transport when requested
    for transport in Transport.objects.filter(project=project_id, mode="guess"):
        transport.mode = transport.guess_mode()
        transport.save()

@celery_app.task(bind=True)
def geocode_address(self, address_id):
    address = Address.objects.get(pk=int(address_id))
    address.geocode()

@celery_app.task(bind=True)
def compute_footprint(self, project_json, provider="openfootprint.core.providers.carbonkit"):

    footprint_provider = importlib.import_module(provider).FootprintProvider() # type: ignore

    for emission_source in project_json:
        co2e = getattr(footprint_provider, EMISSION_HANDLERS_BY_SOURCE[emission_source["type"]])(emission_source)
        emission_source.setdefault("f", {})["co2e"] = co2e * emission_source.get("weight", 1.0)

    return project_json
