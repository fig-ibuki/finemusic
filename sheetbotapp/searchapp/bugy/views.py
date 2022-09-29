from django.shortcuts import render,redirect
from django.http import HttpResponse
from sheetbotapp.searchapp.bugy.songbugy import gobugy
from .songbugy import gobugy
def index(request):
    if request.method == 'POST':
        #get commen,keyword
        searchkey = {}
        searchkey['sname'] = request.POST.get('sname')
        searchkey['type'] = request.POST.get('type')
        searchkey['sband'] = request.POST.get('sband')
        searchkey['keyword'] = request.POST.get('keyword')
        return answer(request,key=searchkey)
    return render(request,'search/search_bugy.html')
def answer(request,key:dict=None):
    
    if key == None:
    #return HttpResponse(song[0].values())
        return render(request,'search/answer_bugy.html',{'song':0})
    #to bugy get list
    song = gobugy(key)
    return render(request,'search/answer_bugy.html',{'song':song})