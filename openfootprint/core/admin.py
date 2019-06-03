from django.contrib import admin
from . import models

admin.site.register(models.Project)

admin.site.register(models.Footprint)

admin.site.register(models.Tag)

admin.site.register(models.Location)

admin.site.register(models.Person)

admin.site.register(models.Transport)

admin.site.register(models.Extra)