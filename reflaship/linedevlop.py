#更新ngrok的網址並抓下來後，去Line Develope網頁更新
from getip import getip
#爬蟲
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions as Sce #selenium錯誤中斷 ex: Sce.NoSuchElementException()
from selenium.webdriver.support.ui import Select
import time
from datetime import datetime




#設定Options
    #way1
options = Options()
        #禁止圖片加載,禁止css加載,解除自動控制字眼
prefs = {"profile.managed_default_content_settings.images": 2,"permissions.default.stylesheet":2,\
        "profile.password_manager_enabled": False, "credentials_enable_service": False}
options.add_experimental_option("prefs", prefs)

    #way2
        #不顯示視窗，背景抓資料
#options.add_argument("--headless")
    #跳過安全性檢查
#options.add_argument("--start-maximized") #open Browser in maximized mode
options.add_argument("--no-sandbox")#bypass OS security model跳過安全性檢查
options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems 阻擋廣告
#解除自動控制字眼
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
# 啟動driver
s = Service(r"C:/Users/RaySu/Desktop/python課程/基礎code/爬蟲蟲/chromedriver_win32/chromedriver.exe")
driver = webdriver.Chrome(service=s,chrome_options=options)
#設定座標
#window's size
driver.set_window_size(780,1080)
#window's 座標
driver.set_window_position(760,0)

url = 'https://developers.line.biz/console/channel/1657395686/messaging-api'

driver.get(url)
time.sleep(0.2)

#login
#line的帳密，以後需要修掉
myemail = '0827ray8@gmail.com'
mypw = 'Sola0404'
#ngrok_ip = #呼叫bat並擷取發配ip
ngtok_ip = getip()
driver.find_element(By.XPATH,'/html/body/div[2]/div/div[3]/div/form/div/input').click()
time.sleep(0.2)
insert_element = driver.find_element(By.XPATH,'//*[@id="app"]/div/div/div/div[2]/div/form/fieldset/div[1]/input')
insert_element.send_keys(myemail)
time.sleep(0.2)
insert_element = driver.find_element(By.XPATH,'//*[@id="app"]/div/div/div/div[2]/div/form/fieldset/div[2]/input')
insert_element.send_keys(mypw)
time.sleep(0.2)

#更新Webhook URL
driver.find_element(By.XPATH,'//*[@id="app"]/div/div/div/div[2]/div/form/fieldset/div[3]/button').click()
time.sleep(10)
edit = driver.find_element(By.XPATH,'//*[@id="app"]/section/div/div/section/div/section[2]/div[1]/aside/div/div[2]/button[2]')
ActionChains(driver).click(edit).perform()
time.sleep(0.5)
insert_element = driver.find_element(By.XPATH,'//*[@id="app"]/section/div/div/section/div/section[2]/div[1]/section/div/div/textarea')
insert_element.send_keys(ngtok_ip+'/sheetBot/search/callback')
time.sleep(0.5)
save = driver.find_element(By.XPATH,'//*[@id="app"]/section/div/div/section/div/section[2]/div[1]/aside/div/div[2]/button[1]')
ActionChains(driver).click(save).perform()
temp = input()
# 關閉正在active的瀏覽器
driver.close()