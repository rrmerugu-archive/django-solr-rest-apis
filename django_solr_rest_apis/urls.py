from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^', views.SolrAPIView.as_view()),
]
