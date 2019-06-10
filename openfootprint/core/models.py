import datetime
import time
import json
import sys
from django.db import models
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from autoslug import AutoSlugField

geolocator = Nominatim(user_agent="openfootprint")


class Project(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    name = models.CharField("Name", max_length=200)

    # TODO autoslug
    slug = AutoSlugField("Slug", unique=True, populate_from="name", max_length=100, db_index=True)

    kind = models.CharField(
        max_length=30,
        default="company",
        choices=(
            ("company", "Company"),
            ("event", "Event"),
            ("household", "Household")
        )
    )

    starts_at = models.DateTimeField(blank=True, null=True)
    ends_at = models.DateTimeField(blank=True, null=True)

    # TODO admin_users
    # TODO subprojects / linkedprojects?

    def __str__(self):
        return self.name

    def get_default_location(self):
        return Location.objects.filter(project=self, is_default=True).first()

    def iter_adresses(self):
        """ Iterate through all addresses linked to this project """

        for transport in self.transports.all():
            if transport.from_address:
                yield transport.from_address
            if transport.to_address:
                yield transport.to_address
            for step in transport.steps.all():
                if step.from_address:
                    yield step.from_address
                if step.to_address:
                    yield step.to_address

        for location in self.locations.all():
            if location.address:
                yield location.address

        for person in self.people.all():
            if person.home_address:
                yield person.home_address

class Tag(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    project = models.ForeignKey(Project, db_index=True, related_name='tags', on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=200)
    # TODO color, creator, footprint

    def __str__(self):
        return self.name


class Footprint(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    project = models.ForeignKey(Project, db_index=True, related_name='footprints', on_delete=models.CASCADE)
    version = models.CharField("CR version", max_length=50)
    footprint = models.FloatField("Footprint in gCO2e", blank=True, null=True)

    raw_json = models.TextField("Raw JSON")

    starts_at = models.DateTimeField(blank=True, null=True)
    ends_at = models.DateTimeField(blank=True, null=True)

    def _flatten(self):
        project_json = []
        for emission_type in ["transports", "extras"]:
            for emission_source in getattr(self.project, emission_type).all():
                emission_data = {
                    "type": emission_type,
                    "weight": 1.0
                }
                emission_data.update(getattr(sys.modules["openfootprint.core.serializers"], "%sSerializer" % emission_type.capitalize()[:-1])(emission_source).data)

                if emission_type == "transports" and emission_data.get("roundtrip"):
                    emission_data["weight"] *= 2

                project_json.append(emission_data)
        if self.project.kind == "event":
            night_stays = (self.project.ends_at - self.project.starts_at).days
            # TODO handle other location than main
            event_location = self.project.get_default_location()
            if night_stays <= 0:
                night_stays = 1
            number_of_attendees = self.project.people.exclude(main_location=event_location).count()
            project_json.append({
                "type": "hotel",
                "attendees": number_of_attendees,
                "night_stays": night_stays
            })
            # TODO specify number of meals per day in project settings
            project_json.append({
                "type": "food",
                "number_of_meals": 3,
                "attendees": number_of_attendees,
                "night_stays": night_stays
            })

        return project_json

    def compute(self):
        from .tasks import compute_footprint

        # 3. save json & generate templates
        project_json = self._flatten()
        raw_data = compute_footprint(project_json)

        self.footprint = sum([(emission_source.get("f", {}).get("co2e") or 0) for emission_source in raw_data])
        # self.version = raw_data["f"]["version"]

        self.raw_json = json.dumps(raw_data)

        return raw_data


class Person(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    project = models.ForeignKey(Project, db_index=True, related_name='people', on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=200)
    tags = models.ManyToManyField(Tag, blank=True)

    main_location = models.ForeignKey("Location", db_index=True, related_name='people', on_delete=models.CASCADE, blank=True, null=True)
    home_address = models.ForeignKey("Address", on_delete=models.PROTECT, blank=True, null=True)

    kind = models.CharField(
        max_length=30,
        default="other",
        choices=(
            ("employee", "Employee"),
            ("attendee", "Attendee"),
            ("other", "Other")
        )
    )

    # TODO teams

    def __str__(self):
        return self.name


class AddressManager(models.Manager):
    def create_from_source(self, source_name, source_country=""):
        from .tasks import geocode_address

        address, created = Address.objects.get_or_create(
            source_name=source_name,
            source_country=source_country or "",
            defaults={}
        )
        if created:
            geocode_address.apply_async((address.pk, ), countdown=5)
        return address

class Address(models.Model):
    """ Adresses are shared between projects and thus are immutable once their source_name/source_country is set """

    objects = AddressManager()

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    source_name = models.CharField("Name", max_length=250, db_index=True)
    source_country = models.CharField("Country", max_length=2, db_index=True, blank=True)

    # Computed fields
    latitude = models.FloatField("Latitude", blank=True, null=True)
    longitude = models.FloatField("Longitude", blank=True, null=True)
    country = models.CharField("Country", max_length=2, blank=True, null=True)

    # TODO more fields from geocode

    def geocode(self, force=False):

        if self.latitude is not None and not force:
            return

        time.sleep(1)  # simple rate limit

        # TODO country hint
        try:
            geo = geolocator.geocode(self.source_name, timeout=10, addressdetails=True)
        except Exception as e:
            print("Geocode error %s (%s)" % (e, self.source_name))
            return False

        if not geo:
            return False

        self.latitude = geo.latitude
        self.longitude = geo.longitude
        self.country = geo.raw["address"]["country_code"]

        self.save(update_fields=["latitude", "longitude", "country"])

    def __str__(self):
        return "%s [%s]" % (self.source_name, self.source_country)


TransportModeField = models.CharField(
    max_length=100,
    blank=False,
    null=True,
    choices=(
        ("guess", "Guess"),
        ("plane", "Plane"),
        ("car", "Car"),
        ("train", "Train"),
        ("truck", "Truck"),
        ("bus", "Bus"),
        ("foot", "Foot")
    )
)

class Transport(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    project = models.ForeignKey(Project, db_index=True, related_name='transports', on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=200, blank=True)
    from_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='+', blank=True, null=True)
    to_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='+', blank=True, null=True)

    roundtrip = models.BooleanField(default=True)

    frequency = models.CharField(
        max_length=30,
        default="none",
        choices=(
            ("none", "N times"),
            ("workday", "Every work day"),
            ("perweek", "N per week"),
            ("permonth", "N per month"),
            ("peryear", "N per year")
        )
    )
    frequency_n = models.IntegerField(default=1)
    weight = models.FloatField(default=1.0)

    # For one-shot transports
    done_at = models.DateTimeField(blank=True, null=True)
    return_at = models.DateTimeField(blank=True, null=True)


    # TODO multiple?
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, null=True)

    tags = models.ManyToManyField(Tag, blank=True)

    mode = TransportModeField

    def __str__(self):
        return str(self.name)

    def get_distance(self):
        if not self.from_address or not self.to_address:
            return None
        return geodesic((self.from_address.latitude, self.from_address.longitude), (self.to_address.latitude, self.to_address.longitude)).m

    def guess_mode(self):
        # Guess the most likely form of transport, with rough naive assumptions.
        # To be improved over time and spun off into a proper module

        km = (self.get_distance() or 0) / 1000

        if not km:
            return None

        # c1 = self.from_address.country
        # c2 = self.to_address.country

        if km > 800:
            return "plane"

        if km > 200:
            return "train"

        if km > 1:
            return "car"

        return "foot"

    def get_time_weight(self, start_date, end_date):
        # This is all very approximative for now
        delta = end_date - start_date
        daysyear = 365.0
        daysworked = 218.0  # FR!

        yearshare = delta.days / daysyear

        if self.frequency == "none":
            return self.frequency_n
        elif self.frequency == "workday":
            return yearshare * daysworked
        elif self.frequency == "perweek":
            return yearshare / (daysyear / 7.0)
        elif self.frequency == "permonth":
            return yearshare / 12.0
        elif self.frequency == "peryear":
            return yearshare

        return 1

class TransportWaypoint(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    transport = models.ForeignKey(Transport, db_index=True, related_name='waypoints', on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='+')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", )
        unique_together = ("transport", "order")


class TransportStep(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    from_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='+', blank=True, null=True)
    to_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='+', blank=True, null=True)

    mode = TransportModeField
    transport = models.ForeignKey(Transport, related_name='steps', on_delete=models.CASCADE)


class Extra(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    # All other items that don't have a dedicated model yet
    project = models.ForeignKey(Project, db_index=True, related_name='extras', on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=200)
    tags = models.ManyToManyField(Tag, blank=True)

    kind = models.CharField(
        max_length=30,
        default="co2e",
        choices=(
            ("co2e", "Raw CO2e in g"),
            ("wh", "Watt hours")
        )
    )
    param_f1 = models.FloatField(blank=True, null=True)
    param_f2 = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    project = models.ForeignKey(Project, db_index=True, related_name='locations', on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=200)
    tags = models.ManyToManyField(Tag, blank=True)

    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='+', blank=True, null=True)

    area = models.FloatField(blank=True, null=True)  # in m2
    is_default = models.BooleanField(default=False)
    # heating?
    # power source?


class DataPoint(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    project = models.ForeignKey(Project, db_index=True, related_name='powerdatapoints', on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='+', blank=True, null=True)
    wh = models.FloatField()  # absolute measurement from electrical counter

    # photo, creator