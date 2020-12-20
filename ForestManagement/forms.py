from django import forms
from .models import Product,Order


class ProductCreateForm(forms.ModelForm):
   class Meta:
     model = Product
     fields = ['category','item_name', 'quantity']

class OrderCreateForm(forms.ModelForm):
    class Meta:
      model = Order
      fields = ['category', 'item_name', 'quantity']