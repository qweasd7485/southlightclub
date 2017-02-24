from django import forms

from main.models import Page, ListItem
from main.constants import PAGE, LIST, APP
from django.forms.widgets import HiddenInput


CHOICES = [(PAGE, PAGE),
           (LIST, LIST),
           (APP, APP)]

class PageForm(forms.ModelForm):
    pageType = forms.ChoiceField(label='文章類型', choices=CHOICES, widget=HiddenInput)
    name = forms.CharField(label='標題')
    content = forms.CharField(label='內容', widget=forms.Textarea(), required=False)
    appPath = forms.CharField(label='導向', required=False)
    showTop = forms.BooleanField(label='上方選單', required=False)
    showLeft = forms.BooleanField(label='左側選單', required=False)
    showBottom = forms.BooleanField(label='於頁尾顯示', required=False)
    

    class Meta:
        model = Page
        exclude = ['mainMenuOrder', 'subMenuOrder', 'thirdMenuOrder']
            

class ItemForm(forms.ModelForm):
    name = forms.CharField(label='標題')
    content = forms.CharField(label='內容', widget=forms.Textarea())
        
    class Meta:
        model = ListItem
        fields = ('name', 'content')
    
    
    