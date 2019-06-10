from rest_framework import viewsets
from rest_framework.response import Response
from .models import Project, Transport, Location, Person, Footprint, Extra, Address
from .serializers import ProjectSerializerFull, ProjectSerializerList, TransportSerializer, ExtraSerializer
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .tasks import geocode_project


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return

class TransportViewSet(viewsets.ModelViewSet):
    queryset = Transport.objects.all().select_related('from_address').select_related('to_address')
    permission_classes = (AllowAny,)  # TODO!
    serializer_class = TransportSerializer

class ExtraViewSet(viewsets.ModelViewSet):
    queryset = Extra.objects.all()
    permission_classes = (AllowAny,)  # TODO!
    serializer_class = ExtraSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = (AllowAny,)  # TODO!
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)  # TODO!

    def get_queryset(self):
      if getattr(self, 'action') == "list":
        return Project.objects.all()
      return Project.objects.all().prefetch_related("transports").prefetch_related("transports__to_address").prefetch_related("transports__from_address").prefetch_related("transports__tags")

    def get_serializer_class(self):
      if getattr(self, 'action') == "list":
        return ProjectSerializerList
      return ProjectSerializerFull

    @action(detail=True, methods=['POST'], name='Delete all transports')
    def delete_transports(self, request, pk=None):
      project = self.get_object()
      project.transports.all().delete()
      return Response({'status': 'ok'})

    @action(detail=True, methods=['POST'], name='Delete all people')
    def delete_people(self, request, pk=None):
      project = self.get_object()
      project.people.all().delete()
      return Response({'status': 'ok'})

    @action(detail=True, methods=['POST'], name='Estimate footprint')
    def footprint(self, request, pk=None):
      project = self.get_object()

      footprint = Footprint(project=project)
      data = footprint.compute()

      save = True

      resp = {'status': 'ok', 'result': data}

      if resp:
        footprint.save()
        resp["footprint_id"] = footprint.id
        resp["footprint"] = footprint.footprint

      return Response(resp)


    @action(detail=True, methods=['POST'], name='Set Extras')
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

      return Response({'status': 'ok'})


    @action(detail=True, methods=['POST'], name='Set Locations')
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

        if row.get("address_source_name"):
          obj.address = Address.objects.create_from_source(row["address_source_name"])

        obj.save()

      return Response({'status': 'ok'})

    @action(detail=True, methods=['POST'], name='Set Project settings')
    def set_settings(self, request, pk=None):
      project = self.get_object()

      project.name = request.data["name"]

      project.save()

      return Response({'status': 'ok'})

    @action(detail=True, methods=['POST'], name='Set People')
    def set_people(self, request, pk=None):
      project = self.get_object()

      people_count = project.people.count()

      for i, row in enumerate(request.data):
        person = Person(project=project)

        if row.get("name"):
          person.name = row["name"]
        else:
          person.name = "Person #%s" % (i + people_count)

        if row.get("from_address"):
          person.home_address = Address.objects.create_from_source(row["from_address"],row.get("from_country"))

        person.save()

      return Response({'status': 'ok'})


    @action(detail=True, methods=['POST'], name='Set Transports')
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
          obj.from_address = Address.objects.create_from_source(row["from_address"],row.get("from_country"))

        if row.get("to_address"):
          if type(row["to_address"]) == dict:
            row["to_country"] = row["to_address"].get("source_country")
            row["to_address"] = row["to_address"]["source_name"]
          obj.to_address = Address.objects.create_from_source(row["to_address"],row.get("to_country"))

        obj.roundtrip = (str(row.get("roundtrip") or "").lower() in ("1", "yes", "y", "true"))

        obj.save()

      geocode_project.apply_async((project.id, ), countdown=5)

      return Response({'status': 'ok'})

    @action(detail=True, methods=['POST'], name='Add Transports from people')
    def add_transports_from_people(self, request, pk=None):
      project = self.get_object()

      transports = {
        t.person_id: t
        for t in Transport.objects.filter(person__isnull=False)
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
            t = Transport(
              project=project,
              roundtrip=True,
              from_address=from_address,
              to_address=to_address,
              name="Transport for %s" % person.name,
              person=person,
              mode="guess"
            )
            t.save()

      geocode_project.apply_async((project.id, ), countdown=5)

      return Response({'status': 'ok'})
