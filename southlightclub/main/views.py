from django.shortcuts import render, get_object_or_404, redirect

from main.constants import LIST, APP
from main.models import Page, ListItem, MainItem


def main(request, pageId=''):
    menuTop, menuLeft, menuBottom = makeMenus()
    mainItems = MainItem.objects.exclude(id__in=[4])   #取出資料庫首頁內容前三個(現任社長、社長的話、16-17目標/slogan)
    regular = MainItem.objects.filter(id=4)            #取出資料庫首頁內容第四個(當週例會預告)
    if regular:#filter取出來會是一個list   所以判斷他有存在時，它就是list中的第一筆
        regular = regular[0] 
    context = {'menuTop':menuTop, 'menuLeft':menuLeft, 'menuBottom':menuBottom, 'mainItems':mainItems, 'regular':regular}
    if not pageId:
        return render(request, 'main/main.html', context)    
    path = request.get_full_path()
    if path.startswith('/showPage'):
        page = get_object_or_404(Page, id=pageId)
        if page.pageType==LIST:
            context.update({'listItems':ListItem.objects.filter(page=page)})
        elif page.pageType==APP:
            return redirect(page.appPath)
    else:
        page = get_object_or_404(ListItem, id=pageId)
    context.update({'page':page})   
    return render(request, 'main/main.html', context)


def makeMenus():
    pages = list(Page.objects.all())
    if not pages:
        return [], [], []
    menuTop, menuLeft, menuBottom = [], [], []
    length = len(pages)
    i = 0;
    while i<length:
        mainMenuOrder = pages[i].mainMenuOrder    # Starts with a main menu
        showTop, showLeft, showBottom = pages[i].showTop, pages[i].showLeft, pages[i].showBottom
        menuTopList, menuLeftList, menuBottomList = [], [], []
        while i<length and pages[i].mainMenuOrder==mainMenuOrder:  # Collect submenu    
            if showTop:
                menuTopList.append(pages[i])                                            
            if showLeft:
                menuLeftList.append(pages[i])
            if showBottom:
                menuBottomList.append(pages[i])
            i += 1
        if showTop:
            menuTop.append(menuTopList)        
        if showLeft:
            menuLeft.append(menuLeftList)
        if showBottom:
            menuBottom.append(menuBottomList)
    return menuTop, menuLeft, menuBottom

def about(request):
    menuTop, menuLeft, menuBottom = makeMenus()
    context = {'menuTop':menuTop, 'menuLeft':menuLeft, 'menuBottom':menuBottom}
    return render(request, 'main/about.html', context)

def president(request):
    menuTop, menuLeft, menuBottom = makeMenus()
    presidentIntro = get_object_or_404(MainItem, id=1)
    context = {'menuTop':menuTop, 'menuLeft':menuLeft, 'menuBottom':menuBottom, 'presidentIntro':presidentIntro}
    return render(request, 'main/president.html',context)

def words(request):
    menuTop, menuLeft, menuBottom = makeMenus()
    words = get_object_or_404(MainItem, id=2)
    context = {'menuTop':menuTop, 'menuLeft':menuLeft, 'menuBottom':menuBottom, 'words':words}
    return render(request, 'main/words.html', context)

def target(request):
    menuTop, menuLeft, menuBottom = makeMenus()
    target = get_object_or_404(MainItem, id=3)
    context = {'menuTop':menuTop, 'menuLeft':menuLeft, 'menuBottom':menuBottom, 'target':target}
    return render(request, 'main/target.html', context)

    
    
    
    
    
