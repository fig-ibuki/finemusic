import requests
import re
import time
import datetime
'''
    
'''
def yoopubugy(sname:str,sheetType:str='chord',sband:str='',keyword:str=''):
    #在yoopu.com爬蟲
    url_search = 'https://yoopu.me/explore#q={}'.format(sname)
    page = requests.get(url_search)
    #爬資料

    #包成字典
    
    return None