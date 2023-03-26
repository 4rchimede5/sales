from django.shortcuts import render
from .models import follow
from django.views.generic import ListView
# Create your views here.

def home(request)
	follow_list=follow.objects.all()
	data = {
		'title':'Profile Indicators',
		'followers':follow_list
		}
	return render(request, "profile_indicator.html", data)
