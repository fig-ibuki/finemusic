
import re
from turtle import back
from linebot.models import TextSendMessage, ImageSendMessage, TemplateSendMessage, FlexSendMessage
#quick_reply message type
from linebot.models import QuickReply, ButtonsTemplate,PostbackAction

#flex message
import json

from .image2flex import image2flex
from .searchlocals.searchDB import search_for_LineBot

ngrok = 'https://2d13-211-20-239-187.jp.ngrok.io'
help_text = '歡迎使用sheetbot!\n電腦請使用網頁版\n{}'.format(ngrok+'/sheetBot/search')
open_text = '電腦請使用網頁版：\n{}'.format(ngrok+'/sheetBot/search')
'''
    state:
        open
        start
        insert
        gosearch
        shutdown
'''

#接收Line message text，return字串or譜
def writeSession(session,key,value):
    session[key] = value
def cleanSession(session):
    key = session.keys()
    if len(key) != 0:
        key = list(key)
        for i in key:
            del session[i]
    return session
#def cleanState(session):

class message_request():
    def __init__(self):
        back_msg = None
        quick = None
        text = None
        global help_text
    def open(session:dict):
        #state 0
        back_msg = None
        quick = None
        text = None
        global open_text
        #呼叫服務，並等候呼叫
        #reset session
        
        state_flag = {}
        state_flag['shutdown'] = False
        state_flag['server_flag'] = False
        state_flag['name'] = False
        state_flag['rid'] = False
        state_flag['clean'] = False
        session['now_state'] = 0
        session['state'] = [{
            'state_flag':state_flag,
        },]
        #使用flex讓電腦版也能用
        flex = json.load(open('templates/linebot/open.json','r',encoding='utf-8'))
        back_msg = FlexSendMessage(
                alt_text='open',
                contents=flex,
            )
        #
        '''text = open_text
        quick = QuickReply(
            items=[
                {
                    'type':'action',
                    'action':{
                        "type": "postback",
                        "label": "Search Sheets",
                        "data": "action=start",
                        "displayText": "Search",
                        "inputOption": "openKeyboard",
                    }
                },
                {
                    'type':'action',
                    'action':{
                        "type": "postback",
                        "label": "Shutdown",
                        "data": "action=shutdown",
                        "displayText": "Shutdown",
                        "inputOption": "openKeyboard",
                    }
                }
            ]
        )
        
        back_msg = TextSendMessage(
            text=text,
            quick_reply=quick
        )
        back_msg = TemplateSendMessage(
            alt_text='open',
            template=ButtonsTemplate(
                title='歡迎使用SheetBot!',
                text = open_text,
                actions=[
                    PostbackAction(
                        label="開始搜尋",
                        data="action=start"
                    ),
                    PostbackAction(
                        label="結束",
                        data="action=shutdown"
                    ),
                ]
            )
        )'''
        return session, back_msg
    def shutdown(session:dict):
        back_msg = None
        text = None
        #呼叫服務，並等候呼叫
        #clean session
        session = cleanSession(session)
        #製作back_msg
        text = 'sleep...'
        back_msg = TextSendMessage(
            text=text,
        )
        return session, back_msg
    def gosearch(session:dict,keyword:str):
        #接收keyword，回傳檔案
        img = None
        back_msg = None
        global ngrok
        #write session
        #search DB
        #read session
        now_state = session['now_state']
        state_flag = session['state'][2]['state_flag']
        searchby = session['state'][2]['searchby']
        
        #查詢譜
        #直接接資料庫
        img_path = None
        if state_flag['name'] == True:
            print(keyword)
            img_path = search_for_LineBot(sname=keyword)
            
        elif state_flag['rid'] == True:
            img_path = search_for_LineBot(rid=keyword)
            
        else:
            back_msg = TextSendMessage(
                text='main key error'
            )
            return session,img,back_msg
        #write in session
        '''session['now_state'] = 3
        if len(session['state']) > 3:
            session['state'][3]={
                'state_flag':state_flag,
                'action':'gosearch',
                'searchby':searchby,
                'keyword':keyword
            }
        elif len(session['state']) == 3:
            session['state'].append(
                {
                    'state_flag':state_flag,
                    'action':'gosearch',
                    'searchby':searchby,
                    'keyword':keyword
                }
            )'''

        if img_path == None:
            print('抱歉，找不到欸。你要不要再輸入一次?')
            if state_flag['rid'] == True:
                flex = json.load(open('templates/linebot/failsearch_rid.json','r',encoding='utf-8'))
                back_msg = FlexSendMessage(
                    alt_text='failsearch_rid',
                    contents=flex,
                )
            elif state_flag['name'] == True:
                flex = json.load(open('templates/linebot/failsearch_name.json','r',encoding='utf-8'))
                back_msg = FlexSendMessage(
                    alt_text='failsearch_name',
                    contents=flex,
                )
        else:
            #找到樂譜了!!
            print('找到樂譜了!!')
            img = []
            img_path = image2flex(ngrok,img_path)
            if state_flag['rid'] == True:
                flex = json.load(open('templates/linebot/gosearch_rid.json','r',encoding='utf-8'))
                img.append(
                    FlexSendMessage(
                        alt_text='gosearch_rid',
                        contents=flex,
                    )
                )
                img.append(
                    ImageSendMessage(
                            original_content_url=img_path, 
                            preview_image_url=img_path
                    )
                )
            elif state_flag['name'] == True:
                flex = json.load(open('templates/linebot/gosearch_name.json','r',encoding='utf-8'))
                img.append(
                    FlexSendMessage(
                        alt_text='gosearch_name',
                        contents=flex,
                    )
                )
                print('img_path :',img_path)
                img.append(
                    ImageSendMessage(
                            original_content_url=img_path, 
                            preview_image_url=img_path
                        )
                    )

        state_flag['name'] == False
        state_flag['rid'] = False
        
        #write in session
        session['now_state'] = 3
        if len(session['state']) > 3:
            session['state'][3]={
                'state_flag':state_flag,
                'action':'gosearch',
                'searchby':searchby,
                'keyword':keyword
            }
        elif len(session['state']) == 3:
            session['state'].append(
                {
                    'state_flag':state_flag,
                    'action':'gosearch',
                    'searchby':searchby,
                    'keyword':keyword
                }
            )
        print("imglen:",len(img))
        return session,img,back_msg
    def img_text():
        global ngrok
        url = ngrok + '/static/media/sheet/chord/backgrand.jpg'
        img = ImageSendMessage(
            original_content_url=url, 
            preview_image_url=url
        )
        return img
class postback_request():
    def __init__(self):
        back_msg = None
        quick = None
        text = None
        global help_text
    def start(session:dict):
        prev_state = session['now_state']
        back_msg = None

        #關機test
        prev_state = session.get('now_state')
        if prev_state == None:
            return session, None

        #寫進session
        state_flag = session['state'][prev_state]['state_flag']
        state_flag['shutdown'] = False
        state_flag['server_flag'] = True
        state_flag['name'] = False
        state_flag['rid'] = False
        if prev_state != 0:
            #從其他地方過來的
            session['state'][1]={
                'state_flag':state_flag,
                'action':'start',
            }
        else:
            #加入新的state
            session['state'].append(
                {
                    'state_flag':state_flag,
                    'action':'start',
                }
            )
        session['now_state'] = 1

        #製作back_msg
        flex = json.load(open('templates/linebot/start.json','r',encoding='utf-8'))
        back_msg = FlexSendMessage(
            alt_text='start',
            contents=flex,
        )
        
        
        return session, back_msg
    def insert(session:dict,post:str):
        #state 2
        back_msg = None
        text = None
        searchby = re.findall(r'^.*searchby=(\w+$)',post)
        if list(searchby) == 0:
            text = 'json Error'
        else:
            searchby = searchby[0]

        #now_state = session['now_state']
        #關機test
        prev_state = session.get('now_state')
        if prev_state == None:
            return session, None
        

        state_flag = session['state'][prev_state]['state_flag']
        if searchby == 'name':
            state_flag['name'] = True
            text = '請輸入曲名'
        elif searchby == 'rid':
            state_flag['rid'] = True
            text = '請輸入Real_ID'
        #寫入session
        session['now_state'] = 2
        if len(session['state']) > 2:
            session['state'][2] = {
                'state_flag':state_flag,
                'action':'insert',
                'searchby':searchby,
            }
        else:
            session['state'].append(
                {
                    'state_flag':state_flag,
                    'action':'insert',
                    'searchby':searchby,
                }
            )
        back_msg = TextSendMessage(
            text=text,
        )

        return session,back_msg
    def shutdown(session:dict):
        back_msg = None
        text = None
        #呼叫服務，並等候呼叫
        #clean session
        session = cleanSession(session)
        #製作back_msg
        text = 'sleep...'
        back_msg = TextSendMessage(
            text=text,
        )
        return session, back_msg


