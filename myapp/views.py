from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
from datetime import datetime
# Create your views here.
#learn
times = 0
def dice3(request):
    global times
    dict1 = {
        'name':'Ray',
        'age':22,
    }
    no = np.random.randint(1,6)
    times += 1
    local_times = times
    return render(request, 'dice3.html',locals())
def show(request):
    persons = []
    persons.append({'name':'Amy', 'phone':'04-1234567'})
    persons.append({'name':'Kuga', 'phone':'05-1464567'})
    persons.append({'name':'Hajaj', 'phone':'04-1654327'})
    for i in range(len(persons)):
        persons[i]['age'] = np.random.randint(12,50)

    return render(request,'show.html',locals())
def mdu(request):
    now = datetime.today().weekday()
    chw = ['一','二','三','四','五','六','日']
    toweek = '禮拜'+chw[now]
    start = now*4+1
    end = start + 14
    imgname = []
    if end <= 30:
        for i in range(start, end+1):
            imgname.append("mdu_img/{}.jpg".format(i))
    elif end > 30:
        for i in range(start, 31):
            imgname.append("mdu_img/{}.jpg".format(i))
        for i in range(1,end-30+1):
            imgname.append("mdu_img/{}.jpg".format(i))
    return render(request,'mdu3.html',locals())
def mdu2(request,start):
    imgname = []
    if start == 0:
        start+=1
    elif start >30 or start < 1:
        start = (np.abs(start))%30
    end = start+14
    if end <= 30:
        for i in range(start, end+1):
            #temp = np.random.randint(1,30)
            imgname.append("mdu_img/{}.jpg".format(i))
    elif end > 30:
        for i in range(start, 31):
            imgname.append("mdu_img/{}.jpg".format(i))
        for i in range(1,end-30+1):
            imgname.append("mdu_img/{}.jpg".format(i))
    return render(request,'mdu2.html',locals())
light = {'red':False,'yellow':False,'green':False}


