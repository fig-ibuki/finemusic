import re

def str_to_state(string:str):
    #make sure there are only dict inside, no any list or tuple
    #only for session txt

    # 1. 先把最外圈的dict抓出來
    inside_dict = False
    dict_count = 0
    mutidict = []
    for i in range(len(string)):
        if string[i] =='{':
            if dict_count == 0:
                mutidict.append(i)
            dict_count +=1
        elif string[i] == '}':
            dict_count-=1
            if dict_count == 0:
                mutidict.append(i)
    #2.把dict拆開
    while True:
        if type(mutidict[0]) == int and type(mutidict[1]) == int:
            mutidict.append(string[mutidict[0]+1:mutidict[1]])
            del mutidict[0]
            del mutidict[0]
        else:
            break
    print('len(muti):',len(mutidict))
    #3.對每個dict的內部再做處理
    for i in range(len(mutidict)):
        temp_str = mutidict[i]
        print('muti[i] : ' + temp_str)
        temp = {'state_flag':{},}

        #print('shutdown:',re.findall(r'\'shutdown\':(\w+),',temp_str))
        temp['state_flag']['shutdown'] = re.findall(r'\'shutdown\':(\w+),',temp_str)[0]
        #print('server_flag:',re.findall(r'\'server_flag\':(\w+),',temp_str))
        temp['state_flag']['server_flag'] = re.findall(r'\'server_flag\':(\w+)',temp_str)[0]
        #print('name:',re.findall(r'\'name\':(\w+),',temp_str))
        temp['state_flag']['name'] = re.findall(r'\'name\':(\w+)',temp_str)[0]
        #print('rid:',re.findall(r'\'rid\':(\w+),',temp_str))
        temp['state_flag']['rid'] = re.findall(r'\'rid\':(\w+)',temp_str)[0]
        #print('research:',re.findall(r'\'clean\':(\w+)',temp_str))
        temp['state_flag']['clean'] = re.findall(r'\'clean\':(\w+)',temp_str)[0]
        #print('\n\n')
        #print(temp['state_flag'])
        #將['state'][i]['state_flag']調整成type:Boolen
        for j in list(temp['state_flag'].keys()):
            #print(j)
            if temp['state_flag'][j].lower() == 'true':
                temp['state_flag'][j] = True
            elif temp['state_flag'][j].lower() == 'false':
                temp['state_flag'][j] = False
        #把key跟資料找出來
        key = re.findall(r'\'(\w+)\':',temp_str)
        print('key')
        print(key)
        data = re.findall(r'\':\'([\w&]+)\'',temp_str)
        print('data')
        print(data)
        if len(key) > 6:
            #state_flag以外的key
            key = key[6:]
            for j in range(len(key)):
                temp[key[j]] = data[j]
        mutidict[i] = temp
    return mutidict


class session_maker():
    def __init__(self) -> None:
        pass
    def write_session(session:dict):
        #空的情況
        '''
            最終輸入進session.txt保存，每次都是重新覆寫
            紀錄格式 一筆資料一行(現在是方便閱讀) 全用單引號 每次shutdown清掉對應userid後的資料 不用tree改用dict了，用hash更快
            i.source.userId 'now_state':int 'state':[
                    {
                        'state_flag':{
                            'shutdown':Boolen,
                            'server_flag':Boolen,
                            'name':Boolen,
                            'rid':Boolen,
                            'research':Boolen
                        },


                    },
                    {
                        'state_flag':{
                            'shutdown':Boolen,
                            'server_flag':Boolen,
                            'name':Boolen,
                            'rid':Boolen,
                            'research':Boolen
                        },
                        'action':'start'
                    },
                    ...

                ]\n
        '''
        session_str = ''
        session_ids = list(session.keys())
        for session_id in session_ids:
            #每一個session id
            #取出now_state
            now_state = session[session_id].get('now_state')
            #取出state
            state = session[session_id].get('state')
            #處理state
            if state != None:
                state = str(state)
                print('writing...\nnow_state:{}'.format(now_state))
                print(state)
                state = re.sub(r'\s','',state)
            #把一整行資料串起來
            session_str = session_str + f'{session_id}'
            if now_state != None: session_str += ' {}'.format(now_state)
            if state != None: session_str += ' {}'.format(state)
            session_str += '\n'
        session_str = session_str[:-1]
        paper = open('session.txt','w')
        paper.write(session_str)
        paper.close()

    def read_session_from_txt():
        try:
            file = open('session.txt','r')
        except:
            file = open('session.txt','w')
            file.write('')
            file.close()
            return False
        #return 'file type : '+str(type(file))
        if file == None:
            return 'addr error?'
        #讀出每一行資料
        session_list = []
        while True:
            line = file.readline()
            if line == '' or line == None:
                break
            session_list.append(line)
        #製作成資料(以後有時間在建樹(hash更快))
        session = {}
        for i in range(len(session_list)):
            #如果session_list沒東西就會直接跳過for
            #透過re篩出資料
            session_id = re.findall(r'(^\w+)',session_list[i])
            if len(session_id) == 0:
                return 'type error!!check session.txt!!'
            session_id = session_id[0]
            now_state = re.findall(r'^\w+\s(\d)',session_list[i])
            session[session_id] = {}
            if len(now_state) == 0:
                continue
            now_state = int(now_state[0])
            state = []
            state_data = re.findall(r'\[(.+)\]',session_list[i])
            if len(state_data) == 0:
                #已經被清空資料
                continue
            state = str_to_state(state_data[0])

            #建立dict
            session[session_id] = {
                    'now_state':now_state,
                    'state':state,
            }
        return session

    def clean_session():
        #把session.txt清空
        paper = open('session.txt','w')
        paper.write('')
        paper.close()