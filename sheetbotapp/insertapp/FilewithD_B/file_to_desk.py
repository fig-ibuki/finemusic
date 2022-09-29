#從setting 取得檔案存放路徑
from django.conf import settings
import os

def pdf2img(file):
    #為了訓練模型將pdf轉成img!!!!!!!1
    return True

def Saveindeck(data:dict):
    file_path = []
    if data['Isheet']:
        #path
        path = os.path.join(str(settings.MEDIA_ROOT[0]),'sheet\\iyrics\\',data['Isheet'].name)
        file_path.append([path, data['Isheet']])
        data['Isheet'] = path
    if data['Csheet']:
        #path
        path = os.path.join(str(settings.MEDIA_ROOT[0]),'sheet\\chord\\',data['Csheet'].name)
        file_path.append([path, data['Csheet']])
        data['Csheet'] = path
    if data['Psheet']:
        #path
        path = os.path.join(str(settings.MEDIA_ROOT[0]),'sheet\\piano\\',data['Psheet'].name)
        file_path.append([path, data['Psheet']])
        data['Psheet'] = path
        #加入file
    for i in file_path:
        fname = i[0]
        f = open(fname,'wb')
        for f_part in i[1].chunks():
            f.write(f_part)
        f.close()
    return data
    