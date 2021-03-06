import boto3

import os
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms.utils import ErrorList
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from admin.forms import PageForm, ItemForm, MainItemForm
from main.constants import PAGE, LIST, APP
from main.models import Page, ListItem, MainItem
from southlightclub.settings import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_BUCKET_NAME, AWS_URL


@login_required
def admin(request):
    return render(request, 'admin/admin.html')


@login_required
def page(request):
    pages = Page.objects.all()
    presidentIntro = MainItem.objects.filter(id=1)     #取出資料庫首頁內容第一個(現任社長)
    words = MainItem.objects.filter(id=2)              #取出資料庫首頁內容第二個(社長的話)
    target = MainItem.objects.filter(id=3)             #取出資料庫首頁內容第三個(16-17目標/slogan)
    regular = MainItem.objects.filter(id=4)            #取出資料庫首頁內容第四個(當週例會預告)
    if presidentIntro:                               #filter取出來會是一個list   所以判斷他有存在時，它就是list中的第一筆
        presidentIntro = presidentIntro[0]
    if words:
        words = words[0]
    if target:
        target = target[0]
    if regular: 
        regular = regular[0] 
    menus, subMenu = [], []   
    for page in list(pages):
        if page.subMenuOrder == 0:    # Main menu
            if subMenu:
                menus.append(subMenu)          
            subMenu = []        
        subMenu.append(page)
    menus.append(subMenu)
    
    return render(request, 'admin/page.html', {'menus':menus, 'presidentIntro':presidentIntro, 'words':words, 'target':target, 'regular':regular})


@login_required
def pageCreate(request):
    if request.method=='GET':
        pageType = request.GET.get('pageType')
        return render(request, 'admin/pageOrItemCreate.html', {'pageType':pageType, 
                                                               'pageForm':PageForm(initial={'pageType':pageType}),
                                                               'folderName':'pages'})
    #POST
    pageForm = PageForm(request.POST, error_class=ErrorMessage)
    
    if not pageForm.is_valid():
        messages.error(request, '請修正下面錯誤')
        return render(request, 'admin/pageOrItemCreate.html', {'pageForm':pageForm, 'pageType':pageForm.cleaned_data['pageType']})
    pageForm = pageForm.save(commit=False)
    pageForm.mainMenuOrder = mainMenuOrder()
    pageForm.save()
    
    messages.success(request, '{0} {1} 已成功新增'.format(PAGE, pageForm.name))
    return redirect('admin:page')
    
    
@transaction.atomic
def mainMenuOrder():
    pages = Page.objects.all().order_by('-mainMenuOrder')
    
    if pages:
        return pages[0].mainMenuOrder+1
    else:
        return 1
    
    
@login_required
def pageDetail(request, pageID):
    page = get_object_or_404(Page, id=pageID)
    
    if page.pageType==PAGE or page.pageType==APP:
        pageForm = hiddenField(PageForm(instance=page))
        return render(request, 'admin/pageOrItemDetail.html', {'page':page, 'pageForm':pageForm,
                                                               'folderName':'pages'})
    
    elif page.pageType==LIST:
        return redirect('admin:listItem', pageID=pageID)
    

@login_required
def pageUpdate(request, pageID):
    if request.method=='GET':
        return redirect('admin:page')
    
    page = get_object_or_404(Page, id=pageID)
    pageForm = PageForm(request.POST, instance=page, error_class=ErrorMessage)
    if not pageForm.is_valid():
        messages.error(request, '請修正下面錯誤')
        pageForm = hiddenField(pageForm)
        return render(request, 'admin/pageOrItemDetail.html', {'page':page, 'pageForm':pageForm,
                                                               'folderName':'pages'})
    
    pageForm.save()
    messages.success(request, '{0} {1} 修改成功'.format(PAGE, page.name))
    return redirect('admin:page')


@login_required
def pageDelete(request, pageID):
    page = get_object_or_404(Page, id=pageID)
    
    if request.method=="GET":
        if page.subMenuOrder==0:    #刪除主選單，找所有子選單連帶刪除
            childPages = Page.objects.filter(mainMenuOrder=page.mainMenuOrder).exclude(id=page.id)
        else:
            childPages = {}
        childItems = page.parentPage.all()  #找FK=page的所有清單項目（因為會連帶刪除）
        return render(request, 'admin/deleteConfirm.html', {'page':page, 'childPages':childPages, 'childItems':childItems})
    #POST
    page.delete()
    messages.success(request, '{0} {1} 已成功刪除'.format(PAGE, page.name))
    return redirect('admin:page')


@login_required
def listItem(request, pageID):
    page = get_object_or_404(Page, id=pageID)
    items = ListItem.objects.filter(page=page)
    
    return render(request, 'admin/page.html', {'page':page, 'items':items})


@login_required
def itemCreate(request, pageID):
    
    page = get_object_or_404(Page, id=pageID)
    if request.method=='GET':
        return render(request, 'admin/pageOrItemCreate.html', {'page':page, 'itemForm':ItemForm()})
    #POST
    itemForm = ItemForm(request.POST, error_class=ErrorMessage)
    if not itemForm.is_valid():
        messages.error(request, '請修正下面錯誤')
        return render(request, 'admin/pageOrItemCreate.html', {'page':page, 'itemForm':itemForm})
    itemForm = itemForm.save(commit=False)
    itemForm.page = page
    itemForm.save()
    
    messages.success(request, '{0}項目 {1} 已成功新增'.format(page.name, itemForm.name))
    return redirect('admin:listItem', pageID=pageID)
    
    
@login_required
def itemDetail(request, itemID):
    item = get_object_or_404(ListItem, id=itemID)
    itemForm = ItemForm(instance=item)
    return render(request, 'admin/pageOrItemDetail.html', {'item':item, 'itemForm':itemForm, 'folderName':'pages'})


@login_required
def itemUpdate(request, itemID):
    item = get_object_or_404(ListItem, id=itemID)
    
    if request.method=='GET':
        return redirect('admin:listItem', pageID=item.page.id)
    
    itemForm = ItemForm(request.POST, instance=item, error_class=ErrorMessage)
    if not itemForm.is_valid():
        messages.error(request, '請修正下面錯誤')
        return render(request, 'admin/pageOrItemDetail.html', {'item':item, 'itemForm':itemForm, 'folderName':'pages'})
    
    itemForm.save()
    messages.success(request, '{0} {1} 修改成功'.format(LIST, item.name))
    return redirect('admin:listItem', pageID=item.page.id)


@login_required
def itemDelete(request, itemID):
    item = get_object_or_404(ListItem, id=itemID)
    
    if request.method=='GET':
        return render(request, 'admin/deleteConfirm.html', {'item':item})
    #POST
    item.delete()
    messages.success(request, '{0} {1} 已成功刪除'.format(LIST, item.name))
    return redirect('admin:listItem', pageID=item.page.id)


@login_required
@transaction.atomic
def changeOrder(request):
    if request.method=='POST':
        changeOrders = request.POST.get('changeOrders')
        changeOrders = changeOrders.split(', ')
        
        for changeOrder in changeOrders:
            if changeOrder=='':
                continue
            pageOrder = changeOrder.split('-')
            pageID = pageOrder[0]
            pageMainMenuOrder = pageOrder[1]
            pageSubMenuOrder = pageOrder[2]            
            
            
            page = get_object_or_404(Page, id=pageID)
            page.mainMenuOrder = pageMainMenuOrder
            page.subMenuOrder = pageSubMenuOrder   
                        
                                          
            page.save()
            
        
    return HttpResponse('success')



def rename(subMenus, mainMenuOrder):
    print(subMenus)
    for subMenu in subMenus:
        subMenu.mainMenuOrder = mainMenuOrder
        subMenu.save()


def hiddenField(pageForm):
    #判斷是不是主選單，主選單才讓使用者選擇是否顯示在上、左、下選單
    if pageForm.instance.subMenuOrder!=0:
        pageForm.fields['showTop'].widget = forms.HiddenInput()
        pageForm.fields['showLeft'].widget = forms.HiddenInput()
        pageForm.fields['showBottom'].widget = forms.HiddenInput()
    
    #如果頁面類型不是APP 隱藏導向欄位
    if pageForm.instance.pageType!=APP:
        pageForm.fields['appPath'].widget = forms.HiddenInput()
        
    #如果是APP 隱藏內容欄位
    if pageForm.instance.pageType==APP:
        pageForm.fields['content'].widget = forms.HiddenInput()
    
    return pageForm


class ErrorMessage(ErrorList):
    def __str__(self):
        return ', '.join([e for e in self])


@login_required
def upload(request):
    if request.method=='GET':
        return HttpResponse('upload fail')
    # POST
    fileToUpload = request.FILES.get('fileToUpload')
    folderName = request.POST.get('folderName')
    cloudFilePath = os.path.join(folderName, fileToUpload.name)
    session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY,
                                    aws_secret_access_key=AWS_SECRET_KEY)
    s3 = session.resource('s3')
    s3.Bucket(AWS_BUCKET_NAME).put_object(Key=cloudFilePath, Body=fileToUpload)
    return HttpResponse(AWS_URL + cloudFilePath)

@login_required
def presidentDetail(request):
    presidentToUpdate = get_object_or_404(MainItem, id=1)
    template = 'admin/presidentDetail.html'
    if request.method=='GET':
        mainItemForm = MainItemForm(instance=presidentToUpdate)
        return render(request, template, {'mainItemForm':mainItemForm, 'president':presidentToUpdate})
    #POST
    mainItemForm = MainItemForm(request.POST, instance=presidentToUpdate)
    if not(mainItemForm.is_valid()):
        return render(request, template, {'mainItemForm':mainItemForm, 'president':presidentToUpdate})
    
    mainItemForm.save()
    messages.success(request, '修改成功！！')
    return redirect('admin:admin')

@login_required
def wordsDetail(request):
    wordsToUpdate = get_object_or_404(MainItem, id=2)
    template = 'admin/wordsDetail.html'
    if request.method=='GET':
        mainItemForm = MainItemForm(instance=wordsToUpdate)
        return render(request, template, {'mainItemForm':mainItemForm, 'words':wordsToUpdate})
    #POST
    mainItemForm = MainItemForm(request.POST, instance=wordsToUpdate)
    if not(mainItemForm.is_valid()):
        return render(request, template, {'mainItemForm':mainItemForm, 'words':wordsToUpdate})
    
    mainItemForm.save()
    messages.success(request, '修改成功！！')
    return redirect('admin:admin')
   
@login_required  
def targetDetail(request):
    targetToUpdate = get_object_or_404(MainItem, id=3)
    template='admin/targetDetail.html'
    if request.method=='GET':
        mainItemForm = MainItemForm(instance=targetToUpdate)     
        return render(request, template,{'mainItemForm':mainItemForm, 'target':targetToUpdate})
    #POST
    mainItemForm = MainItemForm(request.POST, instance=targetToUpdate)
    if not(mainItemForm.is_valid()):
        return render(request, template,{'mainItemForm':mainItemForm, 'target':targetToUpdate})
    mainItemForm.save()
    messages.success(request, '修改成功！！')
    return redirect('admin:admin')

@login_required
def regularMeetingDetail(request):
    regularMeetingToUpdate =  get_object_or_404(MainItem, id=4)
    template='admin/regularMeetingDetail.html'
    if request.method=='GET':
        mainItemForm = MainItemForm(instance=regularMeetingToUpdate)     
        return render(request, template,{'mainItemForm':mainItemForm, 'regularMeeting':regularMeetingToUpdate})
    #POST
    mainItemForm = MainItemForm(request.POST, instance=regularMeetingToUpdate)
    if not(mainItemForm.is_valid()):
        return render(request, template,{'mainItemForm':mainItemForm, 'regularMeeting':regularMeetingToUpdate})
    mainItemForm.save()
    messages.success(request, '修改成功！！')
    return redirect('admin:admin')
    
    