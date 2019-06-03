from rest_framework import routers
from .viewsets import ProjectViewSet, TransportViewSet, ExtraViewSet

api_router = routers.DefaultRouter(trailing_slash=False)

api_router.register(r'project', ProjectViewSet)

# TODO permissions!
api_router.register(r'transport', TransportViewSet)
api_router.register(r'extra', ExtraViewSet)
