from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import Report, TransportModeField
from openfootprint.core.ofplib.plugins import PLUGIN_DIRECTORY
from django.views import static
from django.template import engines
import json
import os


class ReportView(TemplateView):
    def get(self, request, *args, **kwargs):

        report = get_object_or_404(Report, id=kwargs["report_id"])
        report.theme_config = json.loads(report.theme_config or "{}")

        template_file = os.path.join(PLUGIN_DIRECTORY, report.theme_slug, "index.html")
        with open(template_file, "r") as f:
            template_string = f.read()
        template = engines["django"].from_string(template_string)

        print(report.project)
        out = template.render({"report": report})

        return HttpResponse(out)


def report_static_serve(request, **kwargs):
    report = get_object_or_404(Report, id=kwargs["report_id"])
    document_root = os.path.join(PLUGIN_DIRECTORY, report.theme_slug, "static")
    return static.serve(request, kwargs["static_path"], document_root=document_root)


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["OPENFOOTPRINT_GLOBAL"] = {
            "transport_modes": [
                {"value": k, "text": v} for (k, v) in TransportModeField.choices
            ]
        }
        return context
