import pymysql

def pdf_to_img(path:str):
    #將pdf檔另存成jpg
    return True
def search_for_LineBot(sname:str=None,rid:str=None):
    #從資料庫SELECT
    print('sname=',sname)
    db = pymysql.connect(host='127.0.0.1', user='use1',passwd='123',database='fine_music')
    scursor = db.cursor()
    if rid != None:
        #用real id搜尋
        sql = 'SELECT song_id FROM Real_filed WHERE real_id=\'{}\''.format(rid)
        scursor.execute(sql)
        sid = scursor.fetchone()
        if sid == None:
            return None
        #篩出Iyrics, Chord, Piano sheet
        sql  = 'SELECT iyrics_path,chord_path,piano_path FROM song WHERE id={}'.format(sid)
    else:
        #用name搜尋，需要改良成寬鬆一點，因為曲名很難記
        sql = 'SELECT iyrics_path,chord_path,piano_path FROM `song` WHERE name=\'{}\''.format(sname)
    scursor.execute(sql)
    song_list=scursor.fetchall()
    song_list = list(song_list)
    song_list = list(song_list[0])
    db.close()

    
    #有沒有找到檔案
    no_file = True
    #轉換格式
    for i in range(len(song_list)):
        if str(song_list[i]) =='None' or song_list[i] == None or str(song_list[i]) == '':
            song_list[i] == None
        else:
            no_file = False
            song_list[i] = str(song_list[i])
    if no_file == True:
        return None
    

    #解壓縮圖像(like .jpg)
    '''for i in range(song_list):
        if song_list[i] !=None:
            for song_path in song_list[i]:
                #判斷檔案類型
                song_type = song_path[-3:]
                if song_type == 'pdf':
                    #轉成pdf後存入輸出用的資料夾
                    #如果PDF存有多張圖片就會傳回list
                    song_path = pdf_to_img(song_path)'''
    #存入輸出用的temp dir(in static)

    #return img path

    return song_list


#img = search_for_LineBot(sname='尋回所愛')
#print(img)