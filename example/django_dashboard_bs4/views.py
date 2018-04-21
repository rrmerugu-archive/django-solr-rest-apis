from django.views.generic import TemplateView
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)


class DjangoDashboardBS4Base(TemplateView):
    template_name = "page.html"
