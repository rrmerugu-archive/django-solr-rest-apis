# Django Solr Query

This module helps django query the solr using pysolr module and return
the json of the solr result.


- stats
- facets

## Install the module

```bash
pip install git+https://github.com/rrmerugu/django-solr-rest-apis.git#egg=django_solr_rest_apis

```

## Configure

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
    url(r'^api/indexing/solr/(?P<collection_name>[\w.@+-]+)$', include('django_solr_rest_apis.urls')),
]

```

## Usage


```
&fl=id,domain_s,url_s
&facet_fields=status_i,domain_s
&page=4
&rows=50
&fq__status_i=404
&fq__domain_s=scienceblogs.com
&fq__created_dt=[2015-01-11T00:00:00Z TO 2018-04-11T00:00:00Z]


http://localhost:8000/api/indexing/solr/weblinks?page=1&facet_fields=status_i,domain_s&fl=id,url_s,created_dt&fq__created_dt=[2018-03-15T12:22:45Z%20TO%202018-03-15T12:22:50Z]




```
### Date range facets

```json

http://localhost:8000/api/indexing/solr/weblinks?fl=id,url_s&facet_date_field=created_dt&facet_date_field_start=2018-03-01T00:00:00Z&facet_date_field_end=2018-05-01T00:00:00Z


{
  "data":{
    "docs":[
      {
        "url_s":"https://blog.github.com/category/policy/",
        "id":"blog.github.com/category/policy/"
      },
      ...
      {
        "url_s":"https://blog.github.com/index.html",
        "id":"blog.github.com/index.html"
      }
    ],
    "hits":3380,
    "debug":{

    },
    "highlighting":{

    },
    "facets":{
      "facet_queries":{

      },
      "facet_fields":{

      },
      "facet_ranges":{
        "created_dt":{
          "counts":[
            "2018-03-11T00:00:00Z",
            0,
            "2018-03-12T00:00:00Z",
            0,
            "2018-03-13T00:00:00Z",
            0,
            "2018-03-14T00:00:00Z",
            0,
            "2018-03-15T00:00:00Z",
            3316,
            "2018-03-16T00:00:00Z",
            0,
            "2018-03-17T00:00:00Z",
            0,
            "2018-03-18T00:00:00Z",
            31,
            "2018-03-19T00:00:00Z",
            0,
            "2018-03-20T00:00:00Z",
            0
          ],
          "gap":"+1DAY",
          "start":"2018-03-11T00:00:00Z",
          "end":"2018-03-21T00:00:00Z"
        }
      },
      "facet_intervals":{

      },
      "facet_heatmaps":{

      }
    },
    "spellcheck":{

    },
    "stats":{

    },
    "qtime":1,
    "grouped":{

    },
    "nextCursorMark":null,
    "docs_total_pages":169.0
  },
  "message":"Ok"
}
```

http://localhost:8000/api/indexing/solr/weblinks?q=*:*&rows=2&page=4&fl=status_i,domain_s,id