from rest_framework import viewsets
from rest_framework.response import Response
from .models import (
    Project,
    Transport,
    Location,
    Person,
    Report,
    Extra,
    Address,
    Hotel,
    Meal,
    File,
    ActivePlugin,
)
from .serializers import (
    ProjectSerializerFull,
    ProjectSerializerList,
    TransportSerializer,
    ExtraSerializer,
    FileSerializer,
)
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .tasks import geocode_project
import datetime
import json


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class TransportViewSet(viewsets.ModelViewSet):
    queryset = (
        Transport.objects.all()
        .select_related("from_address")
        .select_related("to_address")
    )
    permission_classes = (AllowAny,)  # TODO!
    serializer_class = TransportSerializer


class ExtraViewSet(viewsets.ModelViewSet):
    queryset = Extra.objects.all()
    permission_classes = (AllowAny,)  # TODO!
    serializer_class = ExtraSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = (AllowAny,)  # TODO!
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        BasicAuthentication,
    )  # TODO!

    def get_queryset(self):
        if getattr(self, "action") == "list":
            return Project.objects.all()
        return (
            Project.objects.all()
            .prefetch_related("transports")
            .prefetch_related("transports__to_address")
            .prefetch_related("transports__from_address")
            .prefetch_related("transports__tags")
            .prefetch_related("people")
            .prefetch_related("people__tags")
            .prefetch_related("people__home_address")
            .prefetch_related("hotels")
            .prefetch_related("hotels__address")
            .prefetch_related("hotels__tags")
            .prefetch_related("meals")
            .prefetch_related("meals__tags")
        )

    def get_serializer_class(self):
        print("action:", self.action)
        if getattr(self, "action") in ("list", "create"):
            return ProjectSerializerList
        return ProjectSerializerFull

    @action(detail=True, methods=["POST", "GET"], name="Estimate footprint")
    def footprint(self, request, pk=None):
        project = self.get_object()

        # Create a default report if it doesn't exist
        report_count = project.reports.count()
        if report_count == 0:
            report = Report(project=project, name="Default report")
            report.save()

        data = None
        for report in project.reports.all():
            data = report.compute()
            report.save()

        # Return data for the last report
        resp = {
            "status": "ok",
            "result": data,
            "report_id": report.id,
            "footprint": report.footprint,
        }

        return Response(resp)

    @action(detail=True, methods=["POST"], name="Generic delete row")
    def generic_delete_row(self, request, pk=None):
        project = self.get_object()

        row_id = request.data["id"]
        collection = request.data["collection"]

        getattr(project, collection).filter(pk=row_id).delete()

        return Response({"status": "ok"})

    @action(detail=True, methods=["POST"], name="Delete project")
    def delete(self, request, pk=None):
        project = self.get_object()
        project.delete()
        return Response({"status": "ok"})

    @action(detail=True, methods=["POST"], name="Set Extras")
    def set_extras(self, request, pk=None):
        project = self.get_object()

        # TODO see if we can make this more generic

        for row in request.data:
            if row.get("id") and str(row["id"]).startswith("new"):
                row.pop("id")

        ids = {row["id"] for row in request.data if row.get("id")}

        project.extras.exclude(id__in=ids).delete()

        for i, row in enumerate(request.data):
            extra = None
            if row.get("id"):
                extra = Extra.objects.get(pk=row["id"])
            if not extra:
                extra = Extra(project=project)

            for field in ("name", "kind", "param_f1", "param_f2"):
                setattr(extra, field, row.get(field))

            extra.save()

        return Response({"status": "ok"})

    @action(detail=True, methods=["POST"], name="Set Hotels")
    def set_hotels(self, request, pk=None):
        project = self.get_object()

        # TODO see if we can make this more generic

        for row in request.data:
            if row.get("id") and str(row["id"]).startswith("new"):
                row.pop("id")

        ids = {row["id"] for row in request.data if row.get("id")}

        project.hotels.exclude(id__in=ids).delete()

        for i, row in enumerate(request.data):
            obj = None
            if row.get("id"):
                obj = Hotel.objects.get(pk=row["id"])
            if not obj:
                obj = Hotel(project=project)

            for field, default in (
                ("name", ""),
                ("starts_at", None),
                ("ends_at", None),
            ):
                setattr(obj, field, row.get(field, default))

            if row.get("address"):
                if type(row["address"]) == dict:
                    row["country"] = row["address"].get("source_country")
                    row["address"] = row["address"]["source_name"]
                obj.address = Address.objects.create_from_source(
                    row["address"], row.get("country")
                )

            obj.save()

        return Response({"status": "ok"})

    @action(detail=True, methods=["POST"], name="Set Meals")
    def set_meals(self, request, pk=None):
        project = self.get_object()

        # TODO see if we can make this more generic

        for row in request.data:
            if row.get("id") and str(row["id"]).startswith("new"):
                row.pop("id")

        ids = {row["id"] for row in request.data if row.get("id")}

        project.meals.exclude(id__in=ids).delete()

        for i, row in enumerate(request.data):
            obj = None
            if row.get("id"):
                obj = Meal.objects.get(pk=row["id"])
            if not obj:
                obj = Meal(project=project)

            for field, default in (("name", ""), ("mass", 0)):
                setattr(obj, field, row.get(field, default))

            obj.save()

        return Response({"status": "ok"})

    @action(detail=True, methods=["POST"], name="Set Locations")
    def set_locations(self, request, pk=None):
        project = self.get_object()

        # TODO see if we can make this more generic

        for row in request.data:
            if row.get("id") and str(row["id"]).startswith("new"):
                row.pop("id")

        ids = {row["id"] for row in request.data if row.get("id")}

        project.locations.exclude(id__in=ids).delete()

        for i, row in enumerate(request.data):
            obj = None
            if row.get("id"):
                obj = Location.objects.get(pk=row["id"])
            if not obj:
                obj = Location(project=project)

            for field, default in (("name", ""), ("is_default", False)):
                setattr(obj, field, row.get(field, default))

            if row.get("address") or {}:
                if type(row["address"]) == dict:
                    row["country"] = row["address"].get("source_country")
                    row["address"] = row["address"]["source_name"]
                obj.address = Address.objects.create_from_source(
                    row["address"], row.get("country")
                )

            obj.save()

        return Response({"status": "ok"})

    @action(detail=True, methods=["POST"], name="Set Project settings")
    def set_settings(self, request, pk=None):
        project = self.get_object()

        project.name = request.data["name"]
        if request.data.get("starts_at"):
            project.starts_at = datetime.datetime.strptime(
                request.data.get("starts_at"), "%Y-%m-%d"
            )
        if request.data.get("ends_at"):
            project.ends_at = datetime.datetime.strptime(
                request.data.get("ends_at"), "%Y-%m-%d"
            )

        project.save()

        return Response({"status": "ok"})

    @action(detail=True, methods=["POST"], name="Set People")
    def set_people(self, request, pk=None):
        project = self.get_object()

        for row in request.data:
            if row.get("id") and str(row["id"]).startswith("new"):
                row.pop("id")

        ids = {row["id"] for row in request.data if row.get("id")}

        project.people.exclude(id__in=ids).delete()

        people_count = project.people.count()

        for i, row in enumerate(request.data):
            obj = None
            if row.get("id"):
                obj = Person.objects.get(pk=row["id"])
            if not obj:
                obj = Person(project=project)

            if row.get("name"):
                obj.name = row["name"]
            else:
                obj.name = "Person #%s" % (i + people_count)

            if row.get("home_address"):
                if type(row["home_address"]) == dict:
                    row["home_country"] = row["home_address"].get("source_country")
                    row["home_address"] = row["home_address"]["source_name"]
                obj.home_address = Address.objects.create_from_source(
                    row["home_address"], row.get("home_country")
                )

            obj.save()

        return Response({"status": "ok"})

    @action(detail=True, methods=["POST"], name="Set Transports")
    def set_transports(self, request, pk=None):
        project = self.get_object()

        for row in request.data:
            if row.get("id") and str(row["id"]).startswith("new"):
                row.pop("id")

        ids = {row["id"] for row in request.data if row.get("id")}

        project.transports.exclude(id__in=ids).delete()

        transports_count = project.transports.count()

        for i, row in enumerate(request.data):

            obj = None
            if row.get("id"):
                obj = Transport.objects.get(pk=row["id"])
            if not obj:
                obj = Transport(project=project)

            if row.get("mode"):
                obj.mode = row["mode"]

            if row.get("name"):
                obj.name = row["name"]
            else:
                obj.name = "Transport #%s" % (i + transports_count)

            if row.get("from_address"):
                if type(row["from_address"]) == dict:
                    row["from_country"] = row["from_address"].get("source_country")
                    row["from_address"] = row["from_address"]["source_name"]
                obj.from_address = Address.objects.create_from_source(
                    row["from_address"], row.get("from_country")
                )

            if row.get("to_address"):
                if type(row["to_address"]) == dict:
                    row["to_country"] = row["to_address"].get("source_country")
                    row["to_address"] = row["to_address"]["source_name"]
                obj.to_address = Address.objects.create_from_source(
                    row["to_address"], row.get("to_country")
                )

            obj.roundtrip = str(row.get("roundtrip") or "").lower() in (
                "1",
                "yes",
                "y",
                "true",
            )

            obj.save()

        geocode_project.apply_async((project.id,), countdown=5)

        return Response({"status": "ok"})

    @action(detail=True, methods=["POST"], name="Remove Plugins")
    def remove_plugins(self, request, pk=None):
        ActivePlugin.objects.filter(slug=request.data[0]).delete()
        return Response({"status": "ok"})

    @action(detail=True, methods=["POST"], name="Set Plugins")
    def set_plugins(self, request, pk=None):
        project = self.get_object()

        partial = False
        for row in request.data:
            if row == "partial":
                partial = True
            elif row.get("id") and str(row["id"]).startswith("new"):
                row.pop("id")

        for i, row in enumerate(request.data):
            if partial and i == 0:
                continue
            obj = None
            try:
                if row.get("slug"):
                    obj = ActivePlugin.objects.get(slug=row["slug"])
            except ActivePlugin.DoesNotExist:
                obj = ActivePlugin(project=project)
                if row.get("slug"):
                    obj.slug = row["slug"]
                if row.get("name"):
                    obj.name = row["name"]

            obj.config = json.dumps(row.get("config") or {})
            obj.save()
        return Response({"status": "ok"})

    @action(detail=True, methods=["POST"], name="Set Reports")
    def set_reports(self, request, pk=None):
        project = self.get_object()

        partial = False

        for row in request.data:
            if row == "partial":
                partial = True
            elif row.get("id") and str(row["id"]).startswith("new"):
                row.pop("id")

        if not partial:
            ids = {row["id"] for row in request.data if row.get("id")}
            project.reports.exclude(id__in=ids).delete()

        report_count = project.reports.count()

        for i, row in enumerate(request.data):
            if partial and i == 0:
                continue
            obj = None
            if row.get("id"):
                obj = Report.objects.get(pk=row["id"])
            if not obj:
                obj = Report(project=project)

            if row.get("name"):
                obj.name = row["name"]
            else:
                obj.name = "Report #%s" % (i + report_count)

            obj.theme_slug = row["theme_slug"]
            obj.theme_config = json.dumps(row.get("theme_config") or {})

            obj.save()

        return Response({"status": "ok"})

    @action(detail=True, methods=["POST"], name="Add Transports from people")
    def add_transports_from_people(self, request, pk=None):
        project = self.get_object()

        transports = {
            t.person_id: t for t in project.transports.filter(person__isnull=False)
        }

        for person in project.people.all():
            if not transports.get(person.id):

                from_address = None
                to_address = None
                project_location = project.get_default_location()

                if person.main_location:
                    to_address = person.main_location.address
                if not to_address and project_location:
                    to_address = project_location.address

                if person.home_address:
                    from_address = person.home_address

                if from_address and to_address:
                    addresses = (
                        [from_address]
                        + [
                            Address.objects.create_from_source(waypoint)
                            for waypoint in request.data.get("waypoints") or []
                        ]
                        + [to_address]
                    )

                    # TODO native waypoint support
                    for i in range(len(addresses) - 1):

                        # TODO date
                        t = Transport(
                            project=project,
                            roundtrip=True,
                            from_address=addresses[i],
                            to_address=addresses[i + 1],
                            name="Transport for %s" % person.name,
                            person=person,
                            mode="guess",
                        )
                        t.save()

        geocode_project.apply_async((project.id,), countdown=5)

        return Response({"status": "ok"})

    @action(detail=True, methods=["POST"], name="Add Meals from people")
    def add_meals_from_people(self, request, pk=None):
        project = self.get_object()

        meals = {t.person_id: t for t in project.meals.filter(person__isnull=False)}

        massperday = int(request.data.get("massperday") or 1000)

        days = project.get_days() or 1

        nights = project.get_nights() or 1
        if nights > 0:
            for person in project.people.all():
                if not meals.get(person.id):
                    for day in range(days):
                        name = "Meal for %s" % person.name
                        if days > 1:
                            name += " on day %s" % day
                        m = Meal(
                            project=project, mass=massperday, name=name, person=person
                        )
                        m.save()

        return Response({"status": "ok"})

    @action(detail=True, methods=["POST"], name="Add Hotels from people")
    def add_hotels_from_people(self, request, pk=None):
        project = self.get_object()

        existing = {t.person_id: t for t in project.hotels.filter(person__isnull=False)}

        averageoccupancy = float(request.data.get("averageoccupancy") or 1)

        # TODO additional nights for attendees coming from far away
        # TODO hotel address + transports (!)

        nights = project.get_nights() or 1
        print(nights)
        if nights > 0:
            for person in project.people.all():
                if not existing.get(person.id):
                    name = "Hotel for %s" % person.name
                    m = Hotel(
                        project=project,
                        weight=1 / averageoccupancy,
                        name=name,
                        person=person,
                        starts_at=project.starts_at.date(),
                        ends_at=project.ends_at.date(),
                    )
                    m.save()

        return Response({"status": "ok"})

    @action(detail=True, methods=["POST"], name="Upload a file")
    def upload_file(self, request, pk=None):
        project = self.get_object()

        file = FileSerializer(
            data={"file": request.data.get("file"), "project": project.id}
        )

        if not file.is_valid():
            return Response({"status": "nok"})

        file.save()

        f = File.objects.get(id=file.data["id"])

        return Response({"status": "ok", "file": {"id": f.id, "url": f.file.url}})
