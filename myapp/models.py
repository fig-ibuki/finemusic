from django.db import models

# Create your models here.
class Real_ID(models.Model):
    '''
        RID(str(9)) : 紀錄每首歌的歸檔編號，為避免
        跟實體混淆，所以如果要新增都會預設在未歸檔。
        若已經有實體歸檔，則會記錄實體歸檔編號。
        唯一，且不得為NULL。
        如果未歸檔的歌曲實體歸檔了，更新需要重新建檔，
        需要對應功能
            RID = infiled + band + word lens + ID
            ex:
                not in filed = 0
                band = 讚美之泉
                name = 我要向高山舉目
                ID = 0001
                RID = 0A0070001
        Band(str(1)) : 每首曲子的創作者，用單個字母取代。
        不得為NULL。
        name(str(40)) : 每首曲子的名字，需要計算長度計入
        RID。不得為NULL。
        ID(int(4)) : 流水號，不得為NULL。
        in_filed(boolen) : 紀錄是否歸檔。不得為NULL。
    '''
    #RID = 
    in_filed = models.BooleanField(
        max_length=1,
        default=False,
        null=False,
    )
    BAND_CHOICES = [
        ('A','讚美之泉'),
        ('B','約書亞'),
        ('C','以斯拉'),
        ('D','生命河'),
        ('E','有情天'),
        ('F','我心旋律'),
        ('G','祝瑞蓮'),
        ('H','華人的讚美敬拜'),
        ('I','慕主先鋒'),
        ('J','小羊詩歌'),
        ('K','萬國敬拜與讚美'),
        ('M','其他'),
    ]
    Band = models.CharField(
        max_length=1,
        choices=BAND_CHOICES,
        default='M',
        null=False
    )
    #name = 
class song(models.Model):
    
    #ID = models.

    Name = models.CharField(max_length=40, null=False)
