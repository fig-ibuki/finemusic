import pymysql

def save_in_DB(data:dict):
    #開啟資料庫
    db = pymysql.connect(host="127.0.0.1", user="use1",passwd="123",database="fine_music")
    scursor = db.cursor()

    #未來要搬去search的地方
    #sheet[item,path]
    sheet = [',','']
    if data['Isheet'] != None:
        sheet[0] = sheet[0] + 'Iyrics_path'
        sheet[1] = sheet[1] + '\'' + data['Isheet'] + '\''
    if data['Csheet'] != None:
        if len(sheet[1]) > 0:
            sheet[0] = sheet[0] + ','
            sheet[1] = sheet[1] + ','
        sheet[0] = sheet[0] + 'chord_path'
        sheet[1] = sheet[1] +'\'' + data['Csheet'] + '\''
    if data['Psheet'] != None:
        if len(sheet[1]) > 0:
            sheet[0] = sheet[0] + ','
            sheet[1] = sheet[1] + ','
        sheet[0] = sheet[0] + 'piano_path'
        sheet[1] = sheet[1] + '\'' + data['Psheet'] + '\''

    #有沒有辦法從譜辨識出歌詞??用DLLLLLL阿阿阿阿阿阿阿阿!!!!!!!!!!

    sql = 'INSERT INTO song (name,language,band{}) \
        value (\'{}\',\'{}\',\'{}\',{})'.format( \
            sheet[0],
            data['sname'],
            data['slanguage'],
            data['sband'],
            sheet[1],
            )
    #把消失的\補回來
    i = 0
    while i < len(sql):
        if sql[i] == '\\':
            sql = sql[:i] + '\\' + sql[i:]
            i+=1
        i+=1
    try:
        #輸入DB
        scursor.execute(sql)
        db.commit()
        db.close()
        return sql
    except:
        return False