from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.conf import settings
import pysolr
import logging
import datetime

logger = logging.getLogger(__name__)

SOLR_HOST = settings.__dict__.get('SOLR_HOST', "localhost")
SOLR_HOST_PORT = settings.__dict__.get('SOLR_HOST_PORT', "8983")


class SolrAPIView(TemplateView):
    """
    http://localhost:8000/api/indexing/solr/weblinks (weblinks is collections name)

    &fl=id,domain_s
    &page=4
    &rows=50
    &fq__status_i=404&fq__domain_s=scienceblogs.com
    &start_date=2018-01-12
    &end_date=2018-01-13
    """
    cached_solr_connections = {}

    def extract_from_query(self):
        url_query_dict = self.request.GET.copy()
        rows = url_query_dict.get("rows", 20)
        if "rows" in url_query_dict:
            del url_query_dict['rows']

        page = url_query_dict.get('page', 1)
        if "page" in url_query_dict:
            del url_query_dict['page']

        facet_fields = url_query_dict.get('facet_fields', "")
        if "facet_field" in url_query_dict:
            del url_query_dict['facet_field']

        fields = url_query_dict.get('fl', '*').split(",")
        if "fl" in url_query_dict:
            del url_query_dict['fl']

        field_queries_dict = {}
        for k, v in url_query_dict.items():
            if k.startswith("fq__"):
                field_queries_dict[k.replace("fq__", "")] = v

        if len(field_queries_dict.keys()) == 0:
            field_queries_dict = {"*": "*"}
        search_query = " AND ".join(["{}:{}".format(k, v) for k, v in field_queries_dict.items()])
        solr_kwargs = {
            "fl": fields,
            "rows": int(rows),
            "start": int(rows) * (int(page) - 1),
        }

        solr_kwargs["q"] = search_query
        if len(facet_fields) > 0:
            solr_kwargs['facet'] = "on"
            solr_kwargs['facet.field'] = facet_fields.split(",")
        return solr_kwargs, search_query

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

    def clean_docs(self, docs):
        cleaned_docs = []
        for doc in docs:
            cleaned_doc = {}
            for k, v in doc.items():
                if k.endswith("_dt"):
                    date_string = v.strip("Z")
                    if "." in date_string:
                        date_string = date_string.split(".")[0]
                    date_object = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
                    cleaned_doc[k] = date_object
                else:
                    cleaned_doc[k] = v
                cleaned_docs.append(cleaned_doc)

        return cleaned_docs

    def clean_data(self, data):
        cleaned_data = data
        for k, v in data.get('facets', {}).get('facet_fields', {}).items():
            cleaned_data['facets']['facet_fields'][k] = self.convert_facets_field_to_dict(v)

        cleaned_data['docs'] = self.clean_docs(data.get("docs", []))
        return cleaned_data

    def get(self, request, *args, **kwargs):
        collection_name = kwargs['collection_name']
        if collection_name not in self.cached_solr_connections.keys():
            solr_connection = pysolr.Solr('http://{}:{}/solr/{}/'.format(SOLR_HOST, SOLR_HOST_PORT, collection_name),
                                          timeout=10)
            self.cached_solr_connections[collection_name] = solr_connection
        else:
            solr_connection = self.cached_solr_connections.get(collection_name)

        solr_kwargs, search_query = self.extract_from_query()
        logger.info(solr_kwargs)

        try:
            data = solr_connection.search(**solr_kwargs).__dict__
        except Exception as e:
            print(e)
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
