from django.test import TestCase
from .image2flex import image2flex
# Create your tests here.
ngrok = 'https://2d13-211-20-239-187.jp.ngrok.io'
a_list = [None, 'C:\\Users\\RaySu\\Desktop\\python課程\\找樂譜\\finemusic\\static\\media\\sheet\\chord\\backgrand.jpg', None]
img = image2flex(ngrok=ngrok,img_path=a_list)
print(img)
