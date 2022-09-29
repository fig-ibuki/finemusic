from django.urls import re_path as url
from .views import *
urlpatterns = [
    url(r'^dice3/$',dice3),
    url(r'^show/$',show),
    url(r'^mdu/$',mdu),
    url(r'^mdu2/$',mdu2),
]