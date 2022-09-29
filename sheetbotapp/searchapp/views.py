from django.shortcuts import render
#從setting 取得linebot token
from django.conf import settings
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt,requires_csrf_token
#linebot相關
#Connet
from linebot import LineBotApi, WebhookParser
#ERROR
from linebot.exceptions import InvalidSignatureError, LineBotApiError
#判斷事件類別，回覆的message type
from linebot.models import MessageEvent, PostbackEvent, TextSendMessage, ImageSendMessage, TemplateSendMessage
#quick_reply message type
from linebot.models import QuickReply,ButtonsTemplate

import re

from .message_callback import message_request,postback_request
from .for_session import session_maker

#從setting取得LineBot憑證，進行Messaging API驗證
#注意，如果是 ngrok + Colab 產生的網址，每次重新執行就要再進入 LINE Developer 更新 Webhook。
linebot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


'''
    session:{
        (for linebot)
        now_state:int = 0到5?紀錄目前的state，並依此把目前狀態存進state[now_state]
        state:list[dict] = 0到5?存放每一個state當時的staticflag, searchby, add keyword, 
            每次搜尋完成或關機就清空。先進先出的stack，每次back的時候就將上一個排出去。
        [
            {
                'static':dict = 每一個state當時的flag狀態
                'searchby':str = 最主要搜尋的key
            },
        ]
        
    }
'''


# Create your views here.
#side project-finemusic

#session
def get_Session_id(source:str):
    '''
        Get user id from i.
        i is like json type message which sended by LineBot api.
        i struct:
        {
            reply_token:'',
            type:'',
            timestemp:'',
            source:{
                type:'',
                userId:'',
            },
            message:{
                id:'',
                type:'',
                ...
            }

        }
    '''
    userid = re.findall(r'userId[\W]+(\w+)',source)
    if len(userid) == 0:
        return 0
    userid = userid[0]
    return userid

def cleanSession(session):
    key = list(session.keys())
    for i in key:
        del session[i]
#首頁<search>
def index(request):

    return render(request,'search/searchindex.html',locals())



#for LineBot
'''state_flag = {
    #當呼叫時才出聲提供服務
    'shutdown':False,
    'server_flag':False,
    'name':False,
    'rid':False,
    'clean':False
    #未來exsearch時多個輸入用
    #'insert':False,
}'''
# 裝飾@csrf_exempt可以跳過中間層的驗證，但同時讓session、cookies消失
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        line_sign = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            line_events = parser.parse(body, line_sign)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for i in line_events:
            #從session.txt讀取session資料
            session = session_maker.read_session_from_txt()
            
            #判斷是否為Postback event(查詢的部分)
            if isinstance(i,PostbackEvent):
                #session test
                session_id = get_Session_id(str(i.source))
                if session_id == 0:
                    linebot_api.reply_message(
                        i.reply_token,
                        TextSendMessage(
                            text=str(i.source)
                        )
                    )
                if session == {}:
                    #session完全沒東西的情況，在postback的情況不應該發生，至少也應該有紀錄reply token
                    session[session_id] = {}
                    linebot_api.reply_message(
                        i.reply_token,
                        TextSendMessage(
                            text='請輸入sheetbot啟動',
                        )
                    )
                elif type(session) == str:
                    linebot_api.reply_message(
                        i.reply_token,
                        TextSendMessage(
                            text=session
                        )
                    )
                #取出post裡面的資訊
                action = re.findall(r'action=(\w+)',str(i.postback.data))
                if list(action) == 0:
                    action = 'none'
                else:
                    action = action[0]
                if action == 'start':
                    session[session_id],back_msg = postback_request.start(session[session_id])
                    
                elif action == 'insert':
                    session[session_id],back_msg = postback_request.insert(session[session_id],str(i.postback.data))
                elif action == 'shutdown':
                    session[session_id],back_msg = postback_request.shutdown(session[session_id])
                #寫入session
                session_maker.write_session(session)
                #輸出
                if back_msg != None:
                    linebot_api.reply_message(
                        i.reply_token,
                        back_msg,
                    )

            #判斷是否為信息事件
            elif isinstance(i,MessageEvent):
                #取得session id
                session_id = get_Session_id(str(i.source))
                if session_id == 0:
                    linebot_api.reply_message(
                        i.reply_token,
                        TextSendMessage(
                            text=str(i.source)
                        )
                    )
                if session == {}:
                    #至少在系統第一次啟動、或者手動清空的時候會發生一次以上
                    #製作第一個userID

                    session[session_id] = {}
                elif type(session) == str:
                    linebot_api.reply_message(
                        i.reply_token,
                        TextSendMessage(
                            text=session
                        )
                    )
                #i.message.text
                '''linebot_api.reply_message(
                    i.reply_token,
                    TextSendMessage(
                        text='g'
                    )
                )'''
                
                if re.search(r'[Ss][Hh][Ee][Ee][Tt]\s*[Bb][Oo][Tt]',str(i.message.text).lower()):
                    if session[session_id] != {}:
                        cleanSession(session[session_id])
                    session[session_id], back_msg = message_request.open(session[session_id])
                    #紀錄session
                    session_maker.write_session(session)
                    #輸出
                    linebot_api.reply_message(
                        i.reply_token,
                        back_msg,
                    )
                elif str(i.message.text).lower() == 'shutdown':
                    session[session_id],back_msg = message_request.shutdown(session[session_id])
                    #紀錄session
                    session_maker.write_session(session)
                    #輸出
                    linebot_api.reply_message(
                        i.reply_token,
                        back_msg,
                    )
                elif session[session_id].get('state'):
                    lest_state=len(session[session_id]['state'])-1
                    if session[session_id]['state'][lest_state].get('action') == 'insert':
                        session[session_id],img,back_msg = message_request.gosearch(session[session_id],keyword=i.message.text)
                        #紀錄session
                        session_maker.write_session(session)
                        #輸出
                        if back_msg!=None:
                            #沒找到資料
                            linebot_api.reply_message(
                                i.reply_token,
                                back_msg,
                            )
                        elif img!=None:
                            #img_test
                                
                            #找到資料
                            '''linebot_api.reply_message(
                                i.reply_token,
                                img[0],
                            )'''
                            linebot_api.reply_message(
                                i.reply_token,
                                img[1],
                            )
                #img text
                elif str(i.message.text).lower() == 'img':
                    img = message_request.img_text()
                    linebot_api.reply_message(
                        i.reply_token,
                        img,
                    )
                
                    

        return HttpResponse()
    else:
        return HttpResponseBadRequest()