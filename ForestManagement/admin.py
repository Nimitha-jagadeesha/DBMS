from django.contrib import admin
from ForestManagement.forms import ProductCreateForm, OrderCreateForm
from .models import Product,Order,Contract,History


class ProductCreateAdmin(admin.ModelAdmin):
   list_display = ['category', 'item_name', 'quantity']
   form = ProductCreateForm
   list_filter = ['category']
   search_fields =  ['category','item_name']

admin.site.register(Product, ProductCreateAdmin)

admin.site.register(Order)
admin.site.register(Contract)
admin.site.register(History)
