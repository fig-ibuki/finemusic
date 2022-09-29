#利用include實現urls分流
from django.urls import re_path as url
from django.urls import include
from sheetbotapp import urls as Bot_urls
urlpatterns = [
    url(r'^sheetBot/',include(Bot_urls)),
]