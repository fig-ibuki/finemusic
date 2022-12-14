# Generated by Django 4.0.6 on 2022-08-18 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Real_ID',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_filed', models.BooleanField(default=False, max_length=1)),
                ('Band', models.CharField(choices=[('A', '讚美之泉'), ('B', '約書亞'), ('C', '以斯拉'), ('D', '生命河'), ('E', '有情天'), ('F', '我心旋律'), ('G', '祝瑞蓮'), ('H', '華人的讚美敬拜'), ('I', '慕主先鋒'), ('J', '小羊詩歌'), ('K', '萬國敬拜與讚美'), ('M', '其他')], default='M', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=40)),
            ],
        ),
    ]
