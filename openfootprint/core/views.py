from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from .models import Footprint, TransportModeField
from django.views import static


class ReportView(TemplateView):

  def get_template_names(self):
    return ["reports/event1/index.html"]

  def get_context_data(self, **kwargs):
    self.footprint = get_object_or_404(Footprint, id=kwargs["footprint_id"])
    context = super().get_context_data(**kwargs)
    context["footprint"] = self.footprint
    return context

def report_static_serve(request, **kwargs):
  footprint = get_object_or_404(Footprint, id=kwargs["footprint_id"])
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