from django.shortcuts import render
from .models import Follower
#from django.views.generic import ListView
# Create your views here.

def home(request):

	follow_list=Follower.objects.all()
	#data = {
	#	'title':'Profile Indicators',
	#	'followers':follow_list
	#	}

	return render(request, 'profiles.html',{"followers":follow_list})

	
