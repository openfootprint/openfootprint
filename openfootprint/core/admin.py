from django.contrib import admin
from . import models


class ProjectAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("kind",)
    list_display = ("name", "kind")

    fieldsets = (("General", {"fields": ("name", "kind", "starts_at", "ends_at")}),)


admin.site.register(models.Project, ProjectAdmin)

admin.site.register(models.Report)

admin.site.register(models.Tag)

admin.site.register(models.ActivePlugin)

admin.site.register(models.Location)

admin.site.register(models.Person)

admin.site.register(models.Transport)

admin.site.register(models.Extra)

admin.site.register(models.Address)

admin.site.register(models.Meal)

admin.site.register(models.Hotel)

admin.site.register(models.File)
