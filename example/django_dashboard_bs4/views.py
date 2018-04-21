from django.views.generic import TemplateView
from django.http import JsonResponse
import logging
import random

logger = logging.getLogger(__name__)


class DjangoDashboardBS4Base(TemplateView):
    template_name = "page.html"
    widget_id = random.randint(312312, 1001231123)

    def get_context_data(self, **kwargs):
        return {
            "widget_id": self.widget_id
        }
