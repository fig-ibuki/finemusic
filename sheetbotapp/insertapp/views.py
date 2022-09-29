import os
from django.shortcuts import render,redirect
from django.http import HttpResponse

from sheetbotapp.insertapp.FilewithD_B.save_file import save_file
from .Data_check.formtest import SongForm_Test
#從setting 取得檔案存放路徑
from django.conf import settings
# Create your views here.
#首頁<insert>
def insert(request):
    err_msg = []
    if request.method == 'POST':
        songdict = {}
        songdict['sname']= request.POST.get('sname')
        songdict['sband'] = request.POST.get('sband')
        songdict['srid'] = request.POST.get('srid')
        songdict['slanguage'] = request.POST.get('slanguage')
        songdict['Isheet'] = request.FILES.get('Isheet')
        songdict['Csheet'] = request.FILES.get('Csheet')
        songdict['Psheet'] = request.FILES.get('Psheet')
        #資料驗證
        err_msg = SongForm_Test(songdict)
        if len(err_msg) > 1:
            return HttpResponse(err_msg)
            return render(request,'insert/insertalt.html',{'initdata':songdict,'erraddr':err_msg[0]})
        #儲存譜 + 存入資料庫
        data = save_file(songdict)
        return HttpResponse(data)
        #return show_insert(request)
    return render(request, "insert/insert.html")

def show_insert(request, file_dict = None):
    '''
        顯示資料讓使用者確認已經上傳
    '''
    sheet_flag = [False,False,False]
    song_name = file_dict['sname']
    Isheet = file_dict['Isheet']
    Csheet = file_dict['Csheet']
    Psheet = file_dict['Psheet']
    
    return render(request, "insert/insert_show.html",locals())
