from django import forms
from .models import Product,Order


class ProductCreateForm(forms.ModelForm):
  class Meta:
    model = Product
    fields = ['category','item_name', 'quantity']
  def clean_category(self):
	  category = self.cleaned_data.get('category')
	  if not category:
		  raise forms.ValidationError('This field is required')
	  return category

  def clean_item_name(self):
	  item_name = self.cleaned_data.get('item_name')
	  if not item_name:
		  raise forms.ValidationError('This field is required')
	  return item_name
  

class OrderCreateForm(forms.ModelForm):
    class Meta:
      model = Order
      fields = ['category', 'item_name', 'quantity','delivery_date']

class SearchForm(forms.Form):
  name = forms.CharField(max_length=20, required=False)


class ProductUpdateForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ['category', 'item_name', 'quantity']

class OrderUpdateForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ['category', 'item_name', 'quantity', 'delivery_date']

