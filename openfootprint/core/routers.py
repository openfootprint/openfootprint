from rest_framework import routers
from .viewsets import ProjectViewSet, TransportViewSet

api_router = routers.DefaultRouter(trailing_slash=False)

api_router.register(r'project', ProjectViewSet)

# TODO permissions!
api_router.register(r'transport', TransportViewSet)
