from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
#首頁<1234>
def index(request):
    return render(request, "main/index.html",locals())