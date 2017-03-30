from django.utils import timezone

from django.db import models


class Page(models.Model):
    name = models.CharField(max_length=128)
    pageType = models.CharField(max_length=10)        # LIST or PAGE or APP
    content = models.TextField(null=True, blank=True)
    appPath = models.CharField(max_length=255, null=True, blank=True)   #如果是APP，該欄存放要導向的路徑
    mainMenuOrder = models.IntegerField()
    subMenuOrder = models.IntegerField(default=0)
    thirdMenuOrder = models.IntegerField(default=0) 
    showTop = models.BooleanField(default=True)
    showLeft = models.BooleanField(default=True)
    showBottom = models.BooleanField(default=True)
    

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['mainMenuOrder', 'subMenuOrder', 'thirdMenuOrder']
        

class ListItem(models.Model):
    page = models.ForeignKey(Page, related_name='parentPage')
    name = models.CharField(max_length=128)
    content = models.TextField()
    createTime = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-createTime']
        
    def __str__(self):
        return self.name
    
class MainItem(models.Model):                #儲存首頁內容(現任社長、社長的話、目標/slogan與當週例會預告)
    name = models.CharField(max_length=128)
    content = models.TextField()
    createTime = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['createTime']
    
    def __str__(self):
        return self.name
    
    
    