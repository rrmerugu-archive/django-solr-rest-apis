# Django Solr Query

This module helps django query the solr using pysolr module and return
the json of the solr result.


In `INSTALLED_APPS` of `settings.py` add `django_solr_rest_apis`,

```python
INSTALLED_APPS = [
    ...
    'django_solr_rest_apis',
]

```

in `urls.py` add

```python

urlpatterns = [
    url(r'^', include('django_solr_rest_apis.urls')),
]

```

http://localhost:8000/api/indexing/solr/weblinks?q=*:*&rows=2&page=4&fl=status_i,domain_s,id