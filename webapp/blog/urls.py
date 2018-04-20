from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/indexing/solr/(?P<collection_name>[\w.@+-]+)$', views.SolrAPIView.as_view()),
]
