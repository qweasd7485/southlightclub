from django.shortcuts import render, get_object_or_404, redirect

from main.constants import LIST, APP
from main.models import Page, ListItem, MainItem


def main(request, pageId=''):
    menuTop, menuLeft, menuBottom = makeMenus()
    presidentIntro = get_object_or_404(MainItem, id=1)
    words = get_object_or_404(MainItem, id=2)
    target = get_object_or_404(MainItem, id=3)
    regularMeeting = get_object_or_404(MainItem, id=4)    
    context = {'menuTop':menuTop, 'menuLeft':menuLeft, 'menuBottom':menuBottom, 'presidentIntro':presidentIntro, 'words':words, 'target':target, 'regularMeeting':regularMeeting}
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

    
    
    
    
    
