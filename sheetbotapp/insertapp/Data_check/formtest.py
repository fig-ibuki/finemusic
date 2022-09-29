#songname
from .Insert_Form_test import *

def SongForm_Test(song_dict):
    '''
        err_msg:list[msg,msg,msg...]
        由錯誤訊息組成，以stack的方式排出msg(str)。

        err_addr:list[boolen]
        標記每一個回傳msg的步驟，可以回傳出錯的位置
    '''
    
    err_addr = [False,False,False,False,False]
    err_msg = []

    #驗證曲名
    msgtemp = name_test(song_dict['sname'])
    if msgtemp != None:
            err_addr[0] = True
            err_msg.append(msgtemp)
    
    #驗證語言(if 檔案毀損)
    msgtemp = lan_test(song_dict.get('slanguage'))
    if msgtemp != None:
            err_addr[1] = True
            err_msg.append(msgtemp)
    
    #驗證樂團(if 檔案毀損)
    banddict = {
        '讚美之泉':'A',
        '約書亞':'B',
        '以斯拉':'C',
        '生命河':'D',
        '有情天':'E',
        '我心旋律':'F',
        '祝瑞蓮':'G',
        '華人的讚美敬拜':"H",
        '慕主先鋒':'I',
        '小羊詩歌':'J',
        '萬國敬拜與讚美':'K',
        '長沢崇史':'JA',
        '其他':'M'
    }
    msgtemp = band_test(song_dict['sband'],banddict)
    if msgtemp != None:
            err_addr[2] = True
            err_msg.append(msgtemp)
    
    #如果有，驗證RID
    if len(song_dict['srid']) > 0:
        msgtemp = rid_test(song_dict['srid'],song_dict['sband'],banddict)
        if msgtemp != None:
            err_addr[3] = True
            err_msg.append(msgtemp)
    
    #驗證sheet
    sheet = [song_dict['Isheet'],song_dict['Csheet'],song_dict['Psheet']]
    #msgtemp = 'I:{}, C:{}, P:{}'.format(type(song_dict['Isheet']),type(song_dict['Csheet']),type(song_dict['Psheet']))
    msgtemp = sheet_test(sheet)
    if msgtemp != None:
            err_addr[4] = True
            err_msg.append(msgtemp)


    #驗證是否已經建檔
    msgtemp = DB_test(song_dict['sname'],song_dict['slanguage'],song_dict['sband'])
    if msgtemp != None:
        err_msg.append(msgtemp)
    #串接錯誤訊息
    errlist = [err_addr]
    for i in err_msg:
        errlist.append(i)
    return errlist