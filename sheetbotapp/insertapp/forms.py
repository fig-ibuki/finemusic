
from django import forms

class UploadFileForm(forms.Form):
    Isheet = forms.FileField(initial='',label='iyrics')
    Csheet = forms.FileField(initial='',label='chord')
    Psheet = forms.FileField(initial='',label='piano')