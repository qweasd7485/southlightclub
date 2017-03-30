from django.conf.urls import url
from admin import views

urlpatterns = [
    url(r'^page/$', views.page, name='page'),
    url(r'^pageCreate/$', views.pageCreate, name='pageCreate'),
    url(r'^pageDetail/(?P<pageID>[0-9]+)/$', views.pageDetail, name='pageDetail'),
    url(r'^pageUpdate/(?P<pageID>[0-9]+)/$', views.pageUpdate, name='pageUpdate'),
    url(r'^pageDelete/(?P<pageID>[0-9]+)/$', views.pageDelete, name='pageDelete'),
    url(r'^listItem/(?P<pageID>[0-9]+)/$', views.listItem, name='listItem'),
    url(r'^itemCreate/(?P<pageID>[0-9]+)/$', views.itemCreate, name='itemCreate'),
    url(r'^itemDetail/(?P<itemID>[0-9]+)/$', views.itemDetail, name='itemDetail'),
    url(r'^itemUpdate/(?P<itemID>[0-9]+)/$', views.itemUpdate, name='itemUpdate'),
    url(r'^itemDelete/(?P<itemID>[0-9]+)/$', views.itemDelete, name='itemDelete'),
    url(r'^changeOrder/$', views.changeOrder, name='changeOrder'),    
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^presidentDetail/$', views.presidentDetail, name='presidentDetail'),
    url(r'^wordsDetail/$', views.wordsDetail, name='wordsDetail'),
    url(r'^targetDetail/$', views.targetDetail, name='targetDetail'),
    url(r'^regularMeetingDetail/$', views.regularMeetingDetail, name='regularMeetingDetail'), 
    url(r'^$', views.page, name='admin'),
]