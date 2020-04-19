from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import User, UserProfile, Item, Category
from django import forms
from django.contrib.admin import widgets                                       

class EventForm(forms.ModelForm):
	category = forms.ModelChoiceField(queryset=Category.objects.all())

	def __init__(self, *args, **kwargs):
		super(EventForm, self).__init__(*args, **kwargs)
		self.fields['name'].required = True
		self.fields['quantity'].required = True
		self.fields['pic'].required = True
		self.fields['unit_price'].required = True
		self.fields['specs'].required = True
		self.fields['category'].required = True


	class Meta:
		model = Item
		exclude = ['item_id']

		labels = {
            "name": "Name of product:",
            "specs": "Description:",
            "quantity": "Stock Quantity:",
            "unit_price": "Cost:",
            "pic": "Image:",
        }


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

