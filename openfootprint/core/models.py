import datetime
import time
import json
from django.db import models
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="openfootprint")

def compute_footprint():
    return

class Project(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    name = models.CharField("Name", max_length=200)

    # TODO autoslug
    slug = models.SlugField("Slug", max_length=100, db_index=True)

    kind = models.CharField(
        max_length=30,
        default="company",
        choices=(
            ("company", "Company"),
            ("event", "Event"),
            ("household", "Household")
        )
    )

    main_venue = models.ForeignKey("Venue", on_delete=models.PROTECT, related_name='+', blank=True, null=True)

    # TODO admin_users
    # TODO subprojects / linkedprojects?

    def __str__(self):
        return self.name

    def iter_locations(self):
        """ Iterate through all locations linked to this project """

        if self.main_venue and self.main_venue.location:
            yield self.main_venue.location

        for transport in self.transports.all():
            if transport.from_location:
                yield transport.from_location
            if transport.to_location:
                yield transport.to_location


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

    def compute(self):

        # Make sure all locations are geocoded
        for location in self.project.iter_locations():
            location.geocode(save=True)

        # Update transport weights depending on the time
        if self.starts_at and self.ends_at:
            for transport in self.project.transports:
                multiplier = transport.get_time_weight(self.starts_at, self.ends_at)
                transport.weight = transport.weight * multiplier  # won't be saved, just for the footprint

        # Send to carbonfootprint library
        from .serializers import ProjectSerializerFull
        serialized_project = ProjectSerializerFull(self.project)
        project_json = serialized_project.data

        # 3. save json & generate templates
        raw_data = compute_footprint(project_json)

        self.footprint = raw_data["f"]["co2e"]
        self.version = raw_data["f"]["version"]

        self.raw_json = json.dumps(raw_data)

        return raw_data


class Person(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    project = models.ForeignKey(Project, db_index=True, related_name='persons', on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=200)
    tags = models.ManyToManyField(Tag)

    main_venue = models.ForeignKey("Venue", db_index=True, related_name='persons', on_delete=models.CASCADE, blank=True, null=True)
    origin_location = models.ForeignKey("Location", on_delete=models.PROTECT, blank=True, null=True)

    kind = models.CharField(
        max_length=30,
        default="other",
        choices=(
            ("employee", "Employee"),
            ("attendee", "Attendee"),
            ("other", "Other")
        )
    )

    def __str__(self):
        return self.name


class Location(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    source_name = models.CharField("Name", max_length=250, db_index=True)
    source_country = models.CharField("Country", max_length=2, db_index=True)

    # Computed fields
    latitude = models.FloatField("Latitude", blank=True, null=True)
    longitude = models.FloatField("Longitude", blank=True, null=True)
    country = models.CharField("Country", max_length=2, blank=True, null=True)

    # TODO more fields from geocode

    def geocode(self, force=False, save=False):

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

        if save:
            self.save()

    def save(self, *args, **kwargs):
        from .tasks import geocode_location

        models.Model.save(self, *args, **kwargs)
        geocode_location.delay(self.pk)

    def __str__(self):
        return "%s [%s]" % (self.source_name, self.source_country)


class TransportMode(models.Model):
    name = models.CharField("Name", max_length=200)


class TransportStep(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    project = models.ForeignKey(Project, db_index=True, related_name='transportsteps', on_delete=models.CASCADE)

    from_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='+', blank=True, null=True)
    to_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='+', blank=True, null=True)

    mode = models.ForeignKey(TransportMode, blank=True, null=True, on_delete=models.PROTECT)
    transport = models.ForeignKey(TransportMode, related_name='transportsteps', on_delete=models.CASCADE)



class Transport(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    project = models.ForeignKey(Project, db_index=True, related_name='transports', on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=200, blank=True, null=True)
    from_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='+', blank=True, null=True)
    to_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='+', blank=True, null=True)

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

    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

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

        return m


class Extra(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    # All other items that don't have a dedicated model yet
    project = models.ForeignKey(Project, db_index=True, related_name='extras', on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=200, blank=True, null=True)
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


class Venue(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    project = models.ForeignKey(Project, db_index=True, related_name='venues', on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=200, blank=True, null=True)
    tags = models.ManyToManyField(Tag)

    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='+', blank=True, null=True)

    area = models.FloatField(blank=True, null=True)  # in m2
    # heating?
    # power source?


class DataPoint(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    project = models.ForeignKey(Project, db_index=True, related_name='powerdatapoints', on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT, related_name='+')
    wh = models.FloatField()  # absolute measurement from electrical counter

    # photo, creator