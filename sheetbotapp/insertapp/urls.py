from django.urls import re_path as url
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
urlpatterns = [
    url(r'^$',insert),
    url(r'^post/',insert),
    url(r'^show/',show_insert),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)