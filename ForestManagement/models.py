from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
from datetime import date
frequency_choice = (
		('Monthly', 'Monthly'),
		('Yearly', 'Yearly'),
	)

class Product(models.Model):
	category = models.CharField(max_length=50, blank=True, null=True)
	item_name = models.CharField(max_length=50, blank=True, null=True)
	quantity = models.IntegerField(default='0', blank=False, null=True)
	price = models.IntegerField(default=0, blank=False, null=True)


	def __str__(self):
		return self.item_name

class Order(models.Model):
	item = models.ForeignKey(Product, on_delete = models.CASCADE)
	ordered_quantity = models.IntegerField(default=0, blank=False, null=True)
	ordered_date = models.DateField(auto_now=True)
	delivery_date =  models.DateField()
	user_name = models.ForeignKey(User, on_delete=models.CASCADE)
	price = models.IntegerField(default=0, blank=False, null=True)
	def __str__(self):
		return self.item.item_name

class Contract(models.Model):
	item = models.ForeignKey(Product, on_delete = models.CASCADE)
	ordered_quantity = models.IntegerField(default=0, blank=False, null=True)
	ordered_date = models.DateField(auto_now=True)
	user_name = models.ForeignKey(User, on_delete=models.CASCADE)
	last_created_date = models.DateField(default='2000-1-1' , blank=False, null=True)
	frequency = models.CharField(max_length=50, blank=True, null=True,choices = frequency_choice)
	price = models.IntegerField(default=0, blank=False, null=True)

	def __str__(self):
		return self.item.item_name

class History(models.Model):
	item = models.ForeignKey(Product, on_delete = models.CASCADE)
	ordered_quantity = models.IntegerField(default=0, blank=False, null=True)
	ordered_date = models.DateField()
	delivery_date =  models.DateField()
	user_name = models.ForeignKey(User, on_delete=models.CASCADE)
	price = models.IntegerField(default=0, blank=False, null=True)
