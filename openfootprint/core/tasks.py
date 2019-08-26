from config import celery_app
from .models import Address, Transport, Project, Report
import importlib


EMISSION_HANDLERS_BY_SOURCE = {
  "transport": "compute_transport_footprint",
  "hotel": "compute_hotel_footprint",
  "meal": "compute_meal_footprint",
  "extra": "compute_extra_footprint"
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
def compute_footprint(self, report_id, provider="openfootprint.plugins.carbonkit"):
    report = Report.objects.get(pk=int(report_id))

    project_json = report.get_flat_items()

    footprint_provider = importlib.import_module(provider).Plugin() # type: ignore
    for emission_source in project_json["items"]:
        co2e = getattr(footprint_provider, EMISSION_HANDLERS_BY_SOURCE[emission_source["type"]])(emission_source)
        emission_source.setdefault("f", {})["co2e"] = co2e * emission_source.get("weight", 1.0)

    return project_json
