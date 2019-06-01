from rest_framework import viewsets
from rest_framework.response import Response
from .models import Project, Transport, Location, Person, Footprint
from .serializers import ProjectSerializerFull, ProjectSerializerList, TransportSerializer
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return

class TransportViewSet(viewsets.ModelViewSet):
    queryset = Transport.objects.all().select_related('from_location').select_related('to_location')
    permission_classes = (AllowAny,)  # TODO!
    serializer_class = TransportSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = (AllowAny,)  # TODO!
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)  # TODO!

    def get_queryset(self):
      if getattr(self, 'action') == "list":
        return Project.objects.all()
      return Project.objects.all().prefetch_related("transports").prefetch_related("transports__to_location").prefetch_related("transports__from_location").prefetch_related("transports__tags")

    def get_serializer_class(self):
      if getattr(self, 'action') == "list":
        return ProjectSerializerList
      return ProjectSerializerFull

    @action(detail=True, methods=['POST'], name='Set Transports')
    def delete_transports(self, request, pk=None):
      project = self.get_object()
      Transport.objects.filter(project=project).delete()
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

      return Response(resp)

    @action(detail=True, methods=['POST'], name='Set Transports')
    def set_transports(self, request, pk=None):
      project = self.get_object()

      transports_count = project.transports.count()

      for i, row in enumerate(request.data):
        transport = Transport(project=project)

        if not row.get("name"):
          transport.name = "Transport #%s" % (i + transports_count)

        if row.get("from_address"):
          transport.from_location, created = Location.objects.get_or_create(
              source_name=row["from_address"],
              source_country=row.get("from_country") or "",
              defaults={}
          )
        if row.get("to_address"):
          transport.to_location, created = Location.objects.get_or_create(
              source_name=row["to_address"],
              source_country=row.get("to_country") or "",
              defaults={}
          )
        else:
          if project.main_location:
            transport.to_location = project.main_location

        transport.roundtrip = ((row.get("roundtrip") or "").lower() in ("1", "yes", "y", "true"))

        transport.save()



      return Response({'status': 'ok'})