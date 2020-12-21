from django.shortcuts import render, redirect
from ForestManagement.models import *
from ForestManagement.forms import ProductCreateForm, OrderCreateForm, SearchForm, ProductUpdateForm, OrderUpdateForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
	title = 'Forest Management System'
	context = {
	    "title": title,
	
	}
	return render(request, "home.html",context)

@login_required
def list_products(request):
	form = SearchForm(request.POST or None)
	title = 'Products'
	queryset = Product.objects.all()
	context = {
	    "title": title,
		"queryset":queryset,
		"okay":True,
		"form":form
	}
	if request.method == 'POST':
		if form.is_valid():
			cd = form.cleaned_data
			a= cd.get('name')
		if(a):
			queryset = Product.objects.filter(item_name__icontains=a) | Product.objects.filter(category__icontains=a)
		else:
			queryset = Product.objects.all()			
	context = {
	    "title": title,
		"queryset":queryset,
		"okay":True,
		"form":form
	}
	
	return render(request, "listitems.html",context)

@login_required
def list_orders(request):
	form = SearchForm(request.POST or None)
	title = 'Orders'
	queryset = Order.objects.all()
	context = {
	    "title": title,
		"queryset":queryset,
		"okay":True,
		"form":form
	}
	if request.method == 'POST':
		if form.is_valid():
			cd = form.cleaned_data
			a= cd.get('name')
		if(a):
			queryset = Order.objects.filter(item_name__icontains=a) | Order.objects.filter(category__icontains=a)
		else:
			queryset = Order.objects.all()			
	context = {
	    "title": title,
		"queryset":queryset,
		"okay":True,
		"form":form
	}
	return render(request, "list_orders.html",context)

@login_required
def add_products(request):
	form =ProductCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('/list')
	context = {
		"form": form,
		"title": "Add Products",
	}
	return render(request, "add_items.html", context)

@login_required
def add_orders(request):
	form = OrderCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('/list')
	context = {
		"form": form,
		"title": "Add Item",
		"okay":True
	}
	return render(request, "add_items.html", context)

@login_required
def update_products(request, pk):
	queryset = Product.objects.get(id=pk)
	form = ProductUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = ProductUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			return redirect('/list')

	context = {
		'form':form
	}
	return render(request, 'add_items.html', context)

@login_required
def update_orders(request, pk):
	queryset = Order.objects.get(id=pk)
	form = OrderUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = ProductUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			return redirect('/list')

	context = {
		'form':form
	}
	return render(request, 'add_items.html', context)

@login_required
def delete_products(request, pk):
		queryset = Product.objects.get(id=pk)
		if request.method == 'POST':
			queryset.delete()
			return redirect('/list')
		return render(request, 'delete_products.html')

	