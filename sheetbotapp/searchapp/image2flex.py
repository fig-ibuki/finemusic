#為了將圖片檔案顯示在Flex message上，需要將DB取出來的path轉換成url，然後把json模板拿出來修改，在吐回去給json_load()
import re

def image2flex(ngrok:str,img_path:list,searchby:str):
    '''
        ngrok:轉換成url用
        img_path:list[iyrics, chord, piano]

    '''
    #path轉換成url
    print('img_path :',img_path)
    for i in range(len(img_path)):
        if img_path[i] != None:
            temp = re.findall(r'(\\static[\\\.\w]+\.jpg)',img_path[i])
            #print(temp)
            if len(temp) > 0:
                img_path[i] = temp[0]
            #需要注意url是用/，檔案路徑path是用\
            img_path[i] = re.sub(r'\\',r'/',img_path[i])
            img_path[i] = ngrok + img_path[i]
            #測試用
            return img_path[i]
    
    #寫入flex

    #讀檔
    if searchby == 'name':
        flex = open('templates/linebot/gosearch_name.json','r',encoding='utf-8')
    elif searchby == 'rid':
        flex = open('templates/linebot/gosearch_rid.json','r',encoding='utf-8')
    
    flex_str = flex.read()
    

def backgrandflex(ngrok:str):
    backgrand_path = ngrok + '/static/images/backgrand.jpg'
    flex = open('templates/linebot/gosearch_rid.json','r',encoding='utf-8')
    

'''ngrok = 'https://2d13-211-20-239-187.jp.ngrok.io'
a_list = [None, 'C:\\Users\\RaySu\\Desktop\\python課程\\找樂譜\\finemusic\\static\\media\\sheet\\chord\\backgrand.jpg', None]
temp = image2flex(ngrok,a_list)
print(temp)'''