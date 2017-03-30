from populate import base
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from main.models import Page, ListItem, MainItem
from main.constants import LIST, PAGE


def populate():
    print('Populating... ', end='')
    #menus = [['關於南光', '緣由', '大事紀', '年度工作計畫'], ['例會期刊'], ['活動花絮', '活動影片', '報導', '照片'],
    #         ['社會專區', '理事會紀錄', '例會照片', '旅遊照片', '家懇照片'], ['友站連結', 'RI網站', '地區網站']]
    User.objects.all().delete()
    User.objects.create_superuser(username='admin', password='admin', email=None)
    MainItem.objects.all().delete()
    president = MainItem()
    president.name = '現任社長'
    president.content = '現任社長'
    president.save()
    words = MainItem()
    words.name = '社長的話'
    words.content = '社長的話'
    words.save()
    target = MainItem()
    target.name = '16-17目標/slogan'
    target.content = '16-17目標/slogan'
    target.save()
    regularMeeting = MainItem()
    regularMeeting.name = '當週例會預告'
    regularMeeting.content = '當週例會預告'
    regularMeeting.save()
    #Page.objects.all().delete()
    #ListItem.objects.all().delete()
    #for i in range(len(menus)):
    #    for j in range(len(menus[i])):
    #        menu = Page()
    #        menu.name = menus[i][j]
    #        if menu.name == '最新消息':
    #            menu.pageType = LIST
    #        else:
    #            menu.pageType = PAGE
    #        menu.content = menu.name + '--abcd'
    #        menu.mainMenuOrder = i+1
    #        if j == 0:  # Main menu
    #            menu.subMenuOrder = 0
    #        else:       # Sub menu
    #            menu.subMenuOrder = j
    #        menu.showTop, menu.showLeft, menu.showBottom = True, True, True
    #        menu.save()
    #for i in range(5):
    #    ListItem.objects.create(page=get_object_or_404(Page, name='最新消息'),
    #                            name='消息'+str(i), content=i)
    print('done.')

if __name__ == '__main__':
    populate()








