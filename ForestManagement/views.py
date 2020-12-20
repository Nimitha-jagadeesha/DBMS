from django.shortcuts import render, redirect
from ForestManagement.models import *
from ForestManagement.forms import ProductCreateForm, OrderCreateForm
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

def add_items(request):
	form =OrderCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('/list')
	context = {
		"form": form,
		"title": "Add Item",
	}
	return render(request, "add_items.html", context)

def add_orders(request):
	form = OrderCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('/list')
	context = {
		"form": form,
		"title": "Add Item",
	}
	return render(request, "add_items.html", context)