import boto3

import os
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms.utils import ErrorList
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from admin.forms import PageForm, ItemForm
from main.constants import PAGE, LIST, APP
from main.models import Page, ListItem
from southlightclub.settings import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_BUCKET_NAME, AWS_URL


@login_required
def admin(request):
    return render(request, 'admin/admin.html')


@login_required
def page(request):
    pages = Page.objects.all()
    menus, subMenu = [], []
    thirdMenu = []
    for page in list(pages):
        if page.thirdMenuOrder >= 1:
            thirdMenu.append(page)
    for page in list(pages):
        if page.subMenuOrder == 0:    # Main menu
            if subMenu:
                menus.append(subMenu)          
            subMenu = []        
        subMenu.append(page)
    menus.append(subMenu)
    
    return render(request, 'admin/page.html', {'menus':menus, 'thirdMenu':thirdMenu})


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
            page.thirdMenuOrder = 0             
                                          
            page.save()
            
        
    return HttpResponse('success')

@login_required
@transaction.atomic
def test(request):
    if request.method=='POST':
        changeOrders = request.POST.get('changeOrders')
        changeOrders = changeOrders.split(', ')
        
        for changeOrder in changeOrders:
            if changeOrder=='':
                continue
            pageOrder = changeOrder.split('-')
            pageID = pageOrder[0]
            page = get_object_or_404(Page, id=pageID)
            page.thirdMenuOrder = page.thirdMenuOrder +2
            
            idpre = int(pageID) - 1
            idpre = str(idpre)
            prepage = get_object_or_404(Page, id=idpre)
            prepage.thirdMenuOrder = prepage.thirdMenuOrder +1
            page.save()
            prepage.save();
        
    return HttpResponse('success')

def test2(request):
    if request.method=='POST':
        changeOrders = request.POST.get('changeOrders')
        changeOrders = changeOrders.split(', ')
        
        for changeOrder in changeOrders:
            if changeOrder=='':
                continue
            pageOrder = changeOrder.split('-')
            pageID = pageOrder[0]   
            
            
            idpre = int(pageID) - 1
            idpre = str(idpre)
            prepage = get_object_or_404(Page, id=idpre)
            prepage.thirdMenuOrder = prepage.thirdMenuOrder +1            
            prepage.save();
        
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
