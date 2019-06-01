from config import celery_app
from .models import Location

@celery_app.task(bind=True)
def geocode_location(self, location_id):
    location = Location.objects.get(pk=location_id)
    location.geocode(save=True)
