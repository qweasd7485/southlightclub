from populate import base
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from main.models import Page, ListItem
from main.constants import LIST, PAGE


def populate():
    print('Populating... ', end='')
    menus = [['產品', '產品1', '產品2'], ['最新消息'], ['活動花絮', '活動花絮1', '活動花絮2', '活動花絮3', '活動花絮4', '活動花絮5', '活動花絮6'],
             ['公司簡介'], ['聯絡我們', '聯絡我們1', '聯絡我們2']]
    User.objects.all().delete()
    User.objects.create_superuser(username='admin', password='admin', email=None)
    Page.objects.all().delete()
    ListItem.objects.all().delete()
    for i in range(len(menus)):
        for j in range(len(menus[i])):
            menu = Page()
            menu.name = menus[i][j]
            if menu.name == '最新消息':
                menu.pageType = LIST
            else:
                menu.pageType = PAGE
            menu.content = menu.name + '--abcd'
            menu.mainMenuOrder = i+1
            if j == 0:  # Main menu
                menu.subMenuOrder = 0
            else:       # Sub menu
                menu.subMenuOrder = j
            menu.showTop, menu.showLeft, menu.showBottom = True, True, True
            menu.save()
    for i in range(5):
        ListItem.objects.create(page=get_object_or_404(Page, name='最新消息'),
                                name='消息'+str(i), content=i)
    print('done.')

if __name__ == '__main__':
    populate()








