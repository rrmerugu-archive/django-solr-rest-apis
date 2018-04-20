from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.conf import settings
import pysolr
import logging

logger = logging.getLogger(__name__)
# Create your views here.


SOLR_HOST = settings.__dict__.get('SOLR_HOST', "localhost")
SOLR_HOST_PORT = settings.__dict__.get('SOLR_HOST_PORT', "8983")


class SolrAPIView(TemplateView):
    """

    http://localhost:8000/api/indexing/solr/weblinks?q=*:*
    http://localhost:8000/api/indexing/solr/weblinks?page=4&fl=status_i,domain_s,id,created_dt,headers_Server_s&rows=6&facet_field=status_i,domain_s

    """
    cached_solr_connections = {}

    def extract_from_query(self):
        rows = self.request.GET.get("rows", 20)
        page = self.request.GET.get('page', 1)
        facet_fields = self.request.GET.get('facet_field', "").split(",")
        solr_kwargs = {
            "domain_s": "blog.github.com",
            "fl": self.request.GET.get('fl', 'id').split(","),
            "rows": int(rows),
            "start": int(rows) * (int(page) - 1),
        }
        if len(facet_fields)>0:
            solr_kwargs['facet'] = "on"
            solr_kwargs['facet.field'] = facet_fields
        search_query = self.request.GET.get('search_query', "*:*")

        q = search_query
        return solr_kwargs, q

    def convert_facets_field_to_dict(self, data):
        data_cleaned = []
        first = True
        first_word = None
        for i, k in enumerate(data):
            if first:
                first_word = k
                first = False
            else:
                d = {
                    first_word: k
                }
                data_cleaned.append(d)
                first_word = None
                first = True
        return data_cleaned

    def clean_data(self, data):
        cleaned_data = data
        for k, v in data.get('facets', {}).get('facet_fields', {}).items():
            cleaned_data['facets']['facet_fields'][k] = self.convert_facets_field_to_dict(v)
        return cleaned_data

    def get(self, request, *args, **kwargs):
        collection_name = kwargs['collection_name']
        if collection_name not in self.cached_solr_connections.keys():
            solr_connection = pysolr.Solr('http://{}:{}/solr/{}/'.format(SOLR_HOST, SOLR_HOST_PORT, collection_name),
                                          timeout=10)
            self.cached_solr_connections[collection_name] = solr_connection
        else:
            solr_connection = self.cached_solr_connections.get(collection_name)

        solr_kwargs, q = self.extract_from_query()
        logger.debug(solr_kwargs, q)

        try:
            data = solr_connection.search(q, **solr_kwargs).__dict__
        except Exception as e:
            return JsonResponse({"message": "Failed to connect to the collection: {}".format(collection_name)},
                                status=400)

        if "raw_response" in data.keys():
            del data['raw_response']

        cleaned_data = self.clean_data(data)

        return JsonResponse({"data": cleaned_data, "message": "Ok"}, status=200)


class ESApiView(TemplateView):
    es_index = None
    es_data_type = None
    cached_collections = []
