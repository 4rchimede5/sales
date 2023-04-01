from django.contrib import admin
from .models import  Follower, Following, Follower_date, Following_date, Post
# Register your models here.

admin.site.register(Follower)
admin.site.register(Follower_date)
admin.site.register(Following)
admin.site.register(Following_date)
admin.site.register(Post)
