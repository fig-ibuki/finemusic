from django.urls import re_path as url
from django.urls import include
from .views import *
from .searchapp import urls as search_urls
from .insertapp import urls as insert_urls
urlpatterns = [
    url(r'^$',index),
    url(r'^search/',include(search_urls)),
    url(r'^insert/',include(insert_urls)),
]