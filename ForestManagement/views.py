from django.shortcuts import render
from ForestManagement.models import *
# Create your views here.

def home(request):
	title = 'Welcome: This is the Home Page'
	context = {
	    "title": title,
	}
	return render(request, "home.html",context)

def list_products(request):
	title = 'Products'
	queryset = Product.objects.all()
	context = {
	    "title": title,
		"queryset":queryset,
	}
	return render(request, "listitems.html",context)