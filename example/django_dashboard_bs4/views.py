from django.views.generic import TemplateView
from django.http import JsonResponse
import logging
import random

logger = logging.getLogger(__name__)

widgets = [
    {
        'name': "Weblinks Collection",
        'API': "/api/indexing/solr/weblinks",
        'fields': ['id', 'domain_s', 'created_dt'],
        'filters': [{
            'key': 'status_i',
            'value': '404',
            'display_name': "404 Status"
        }, {
            'key': 'domain_s',
            'value': 'medium.com',
            'display_name': "medium.com"
        }, {
            'key': 'domain_s',
            'value': 'blog.github.com',
            'display_name': "Github"
        }],
        'paginate_by': 6,
        'filter_date_field': "created_dt",
        'facet_range': 'true'
    },
    {
        'name': "WebFeeds Collection",
        'API': "/api/indexing/solr/website_feeds",
        'fields': ['id', 'title_s', 'domain_s', 'pub_date_dt'],
        'filters': [],
        'paginate_by': 6,
        'filter_date_field': "pub_date_dt",
        'facet_range': 'true'
    }
]


class DjangoDashboardBS4Base(TemplateView):
    template_name = "page.html"

    def get_context_data(self, **kwargs):
        widgets_cleaned = []
        for widget in widgets:
            widget['widget_id'] = random.randint(312312, 1001231123)
            widgets_cleaned.append(widget)
        return {
            "widgets": widgets_cleaned
        }
