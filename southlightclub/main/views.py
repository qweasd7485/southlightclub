from django.shortcuts import render, get_object_or_404, redirect

from main.constants import LIST, APP
from main.models import Page, ListItem


def main(request, pageId=''):
    menuTop, menuLeft, menuBottom = makeMenus()
    context = {'menuTop':menuTop, 'menuLeft':menuLeft, 'menuBottom':menuBottom}
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
