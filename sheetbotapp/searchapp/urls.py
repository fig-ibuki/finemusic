from django.urls import re_path as url
from django.urls import include
from .bugy import urls as bugy_Urls
from .searchlocals import urls as locals_Urls
from .views import *

urlpatterns = [
    #=====web========
    url(r'^$',index),
    url(r'^local/',include(locals_Urls)),
    url(r'^bugy/',include(bugy_Urls)),
    #=====LineBot=======
    url(r'^callback$',callback),
    #=====session=========
    
]
'''
    url(r'^writeSession/(\w+)/<\w+>/',writeSession),
    url(r'^delSession/(\w+)/<\w+>/',delSession),
    url(r'^readSession/(\w+)/<\w+>/',readSession),
    url(r'^readSession/(\w+)/<\w+>/',cleanSession),'''