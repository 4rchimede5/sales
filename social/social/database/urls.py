from django.urls import path
from . import views

urlpatterns=[
	path('',views.home) # goes to views.home when referring to root directory
]
