from .yoopubugy import yoopubugy

def gobugy(searchkey):
    songlist = []
    #在yoopu.com爬蟲
    temp = yoopubugy(searchkey['sname'],searchkey['type'],searchkey['sband'],searchkey['keyword'])
    if temp != None:
        for i in range(len(temp)):
            songlist.append(temp[i])
    #爬其他網站...
    return songlist


