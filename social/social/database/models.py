from django.db import models
from django.contrib import admin
# Create your models here.

class follower(models.Model):
	handle = models.CharField(max_length=50, verbose_name='social handle')
	name = models.CharField(max_length=50, verbose_name='name')

	admin.ModelAdmin.list_per_page = 100

class following(models.Model):
	handle = models.CharField(max_length=50, verbose_name='social handle')
	name = models.CharField(max_length=50, verbose_name='name')
	
	admin.ModelAdmin.list_per_page = 100
