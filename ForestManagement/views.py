from django.shortcuts import render, redirect
from ForestManagement.models import *
from ForestManagement.forms import ProductCreateForm, OrderCreateForm, SearchForm, ProductUpdateForm, OrderUpdateForm
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import date,timedelta,datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from prettytable import PrettyTable
import xlsxwriter
# Create your views here.
d = timedelta(days=4)
mydate = datetime.now() + d
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
@csrf_exempt
def list_orders(request):
	form = SearchForm(request.POST or None)
	title = 'Orders'
	orders = Order.objects.all().order_by('delivery_date')
	# for i in orders:
	# 	print(i)
	context = {
	    "title": title,
		"orders":orders,
		"okay":False,
		"form":form
	}
	if request.method == "POST":
		order_id = request.POST.get('clear_order')
		x = Order.objects.get(pk=order_id)
		if x.item.quantity >= x.ordered_quantity:
			Product.objects.filter(pk=x.item.id).update(quantity=x.item.quantity-x.ordered_quantity)
			History.objects.create(item = x.item,
					ordered_quantity = x.ordered_quantity,
					ordered_date = x.ordered_date,
					delivery_date = x.delivery_date,
					user_name = x.user_name,
					price = (x.item.price * x.ordered_quantity))
			Order.objects.filter(pk=order_id).delete()
		else:
			messages.error(request, "Cannot clear the order as there is no sufficient quantity of "+ str(x.item))
	context = {
	    "title": title,
		"orders":orders,
		"okay":False,
		"form":form
	}
	return render(request, "list_orders.html",context)

@login_required
@csrf_exempt
def list_orders_history(request):
	form = SearchForm(request.POST or None)
	title = 'Orders'
	orders = History.objects.all().order_by('delivery_date')
	# for i in orders:
	# 	print(i)
	context = {
	    "title": title,
		"orders":orders,
		"okay":False,
		"form":form
	}
	if request.method == "POST":
		user_id = request.POST.get('history')
		x = History.objects.all()
		y = User.objects.get(pk = user_id)
		table = PrettyTable()
		workbook = xlsxwriter.Workbook('history.xlsx')
		worksheet = workbook.add_worksheet()
		worksheet.write('A1', 'SECTION')
		worksheet.write('B1', 'PRODUCT')
		worksheet.write('C1', 'QUANTITY')
		worksheet.write('D1', 'DELIVERED DATE')
		worksheet.write('E1', 'ORDERED DATE')
		worksheet.write('F1', 'PRICE')
		x1=0
		if y.is_staff:
			worksheet.write('G1', 'USERNAME')
			j=2
			for i in x:
				worksheet.write('A'+str(j),str(i.item.category) )
				worksheet.write('B'+str(j), str(i.item))
				worksheet.write('C'+str(j), str(i.ordered_quantity))
				worksheet.write('D'+str(j), str(i.delivery_date))
				worksheet.write('E'+str(j), str(i.ordered_date))
				worksheet.write('F'+str(j), str(i.price))
				worksheet.write('G'+str(j), str(i.user_name))
				x1+=i.price
				j+=1
		else:
			j=2
			for i in x:
				if i.user_name.id == y.id:
					worksheet.write('A'+str(j),i.item.category )
					worksheet.write('B'+str(j), str(i.item))
					worksheet.write('C'+str(j), str(i.ordered_quantity))
					worksheet.write('D'+str(j), str(i.delivery_date))
					worksheet.write('E'+str(j), str(i.ordered_date))
					worksheet.write('F'+str(j), str(i.price))
					x1+=i.price
					j+=1
		worksheet.write('F'+str(j),'Total = '+str(x1))
		workbook.close()
		fromaddr = "nimitha1jagadeesha@gmail.com"
		toaddr = y.email
		msg = MIMEMultipart() 
		msg['From'] = fromaddr 
		msg['To'] = toaddr 
		msg['Subject'] = "Order History"
		body = f"Hello {y}!\nOrders Report has been attached to this mail."
		msg.attach(MIMEText(body, 'plain')) 
		part = MIMEBase('application', "octet-stream")
		part.set_payload(open("history.xlsx", "rb").read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="history.xlsx"')
		msg.attach(part)
		s = smtplib.SMTP('smtp.gmail.com', 587) 
		s.starttls() 
		s.login(fromaddr, "nimithajnimi1@")
		text = msg.as_string() 
		s.sendmail(fromaddr, toaddr, text) 
		s.quit() 
			
	context = {
	    "title": title,
		"orders":orders,
		"okay":False,
		"form":form
	}
	return render(request, "history.html",context)



@login_required
@csrf_exempt
def list_contracts(request):
	form = SearchForm(request.POST or None)
	title = 'Contracts'
	orders = Contract.objects.all()
	context = {
	    "title": title,
		"orders":orders,
		"okay":False,
		"form":form
	}
	if request.method == "POST":
		contracts = Contract.objects.all()
		for row in contracts:
			frequency = row.frequency
			last_update = row.last_created_date
			present_date = date.today()
			dl = present_date - last_update
			if frequency == 'Monthly':
				if(dl.days >30):
					Order.objects.create(item = row.item,
					ordered_quantity = row.ordered_quantity,
					delivery_date = mydate,
					user_name = row.user_name,
					price = (row.item.price * row.ordered_quantity) )
					Contract.objects.filter(pk = row.id).update(last_created_date = present_date)
			else:
				if(dl.days >365):
					Order.objects.create(item = row.item,
					ordered_quantity = row.ordered_quantity,
					delivery_date = mydate,
					user_name = row.user_name)
					Contract.objects.filter(pk = row.id).update(last_created_date = present_date)
	context = {
	    "title": title,
		"orders":orders,
		"okay":False,
		"form":form
	}
	return render(request, "list_contracts.html",context)

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
def delete_products(request, pk):
		queryset = Product.objects.get(id=pk)
		if request.method == 'POST':
			queryset.delete()
			return redirect('/list')
		return render(request, 'delete_products.html')

class OrderCreateView(LoginRequiredMixin, CreateView):
	model = Order
	template_name='add_items.html'
	fields = [ 'item', 'ordered_quantity']
	success_url='/'


	def form_valid(self, form):
		form.instance.user_name = self.request.user
		form.instance.delivery_date= mydate
		form.instance.price = (form.instance.item.price * form.instance.ordered_quantity) 
		return super().form_valid(form)

class UserOrderListView(ListView):
    model = Order
    template_name = 'list_orders.html'
    context_object_name = 'orders'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Order.objects.filter(user_name=user).order_by('delivery_date')

class ContractCreateView(LoginRequiredMixin, CreateView):
	model = Contract
	template_name='add_items.html'
	fields = [ 'item', 'ordered_quantity','frequency']
	success_url='/'


	def form_valid(self, form):
		form.instance.user_name = self.request.user
		form.instance.price = (form.instance.item.price * form.instance.ordered_quantity) 
		return super().form_valid(form)

class UserContractsListView(ListView):
    model = Contract
    template_name = 'list_contracts.html'
    context_object_name = 'orders'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Contract.objects.filter(user_name=user)