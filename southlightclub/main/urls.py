from django.conf.urls import url
from main import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^about/$', views.about, name='about'),
    url(r'^president/$', views.president, name='president'),
    url(r'^words/$', views.words, name='words'),
    url(r'^target/$', views.target, name='target'),    
]