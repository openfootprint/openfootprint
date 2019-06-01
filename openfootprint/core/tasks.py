from config import celery_app

@celery_app.task(bind=True)
def geocode_location(self, location):
    print(f'GEO: {self.request!r}')  # pragma: no cover

    location.geocode(save=True)
