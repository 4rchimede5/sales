from django.db import models
from django.contrib import admin
# Create your models here.

class Follower_date(models.Model):
	date=models.DateTimeField()
	time=models.TimeField()

class Follower(models.Model):
	handle = models.CharField(max_length=50, verbose_name='social handle')
	name = models.CharField(max_length=50, verbose_name='name')
	date = models.ForeignKey(Follower_date, on_delete=models.CASCADE)
	admin.ModelAdmin.list_per_page = 100

class Following_date(models.Model):
	date=models.DateTimeField()
	time=models.DateTimeField()

class Following(models.Model):
	handle = models.CharField(max_length=50, verbose_name='social handle')
	name = models.CharField(max_length=50, verbose_name='name')
	date = models.ForeignKey(Following_date, related_name='pull_date',null=True,blank=True, on_delete=models.CASCADE)
	time = models.ForeignKey(Following_date, related_name='pull_time',null=True,blank=True, on_delete=models.CASCADE)
	admin.ModelAdmin.list_per_page = 100

class Post(models.Model):
	post = models.ImageField(verbose_name='Post image')
	caption_text = models.CharField(default='',max_length=100, verbose_name='caption')
	likes = models.IntegerField(default=0,verbose_name='likes')
	likers = models.CharField(default='',max_length=50,verbose_name='likers')
	admin.ModelAdmin.list_per_page = 100
