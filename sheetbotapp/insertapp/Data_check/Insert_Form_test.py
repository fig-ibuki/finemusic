import re
import pymysql

def name_test(name):
    msgtemp = ''
    #len
    if len(name) > 50:
        msgtemp = '曲名過長'
    elif len(name) < 2:
        msgtemp = '曲名過短'
    #特殊字元
    if re.search(r'\W',name):
        msgtemp = '取名應由文字、數字組成'
    
    #回傳
    if len(msgtemp) > 0:
        return msgtemp
def lan_test(lan):
    if lan not in ['ch','jp','en','tw']:
        return '未知的語言'
def band_test(band,bdict):
    if bdict.get(band) == None:
        #不在已知的樂團內
        return '未知的樂團'
def rid_test(rid,band,bdict):
    #檢查長度
    if len(rid) != 8:
        return rid
        #return '長度錯誤'
    #檢查格式
    if re.search(r'^\w\d{7}$',rid) == False:
        return '格式錯誤'
    #檢查字數是否正確
    #檢查樂團是否正確
    if rid[0] != bdict[band]:
        return '樂團資料不相符'

def sheet_test(sheet):
    #預設為沒有譜
    no_file = True
    for i in sheet:
        if i != None:
            no_file = False
            break
    if no_file:
        #沒有加入任何樂譜
        return '必須加入至少1份樂譜'

def DB_test(name, language, band):
    db = pymysql.connect(host='127.0.0.1', user='use1',passwd='123',database='fine_music')
    scursor = db.cursor()
    #檢查帳號是否重複
    sql = "SELECT * FROM song WHERE name='{}' AND language='{}' AND band='{}'".format(name,language,band)
    scursor.execute(sql)
    db.commit()
    db.close()
    if scursor.fetchone():
        return '已經有這首曲子了!'

