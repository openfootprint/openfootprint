from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from .models import Report, TransportModeField
from django.views import static
import json


class ReportView(TemplateView):

  def get_template_names(self):
    return ["reports/event1/index.html"]

  def get_context_data(self, **kwargs):
    self.report = get_object_or_404(Report, id=kwargs["report_id"])
    context = super().get_context_data(**kwargs)
    context["report"] = self.report
    context["report"].config = json.loads(context["report"].config or "{}")
    return context

def report_static_serve(request, **kwargs):
  report = get_object_or_404(Report, id=kwargs["report_id"])
  document_root = "openfootprint/templates/reports/event1/"
  return static.serve(request, kwargs["static_path"], document_root=document_root)


class HomeView(TemplateView):
  template_name = "pages/home.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["OPENFOOTPRINT_GLOBAL"] = {
      "transport_modes": [
        {"value": k, "text": v}
        for (k, v) in TransportModeField.choices
      ]
    }
    return context