from django.urls import re_path as url
from django.urls import include
from .views import *

urlpatterns = [
    #=====web========
    url(r'^$',index),
    url(r'^answer/',answer),
    #=====session=========
]