import re
from django import forms
from .models import Product, GRIND_CHOICES


class PurchaseEnquiryForm(forms.Form):
    product_name = forms.CharField(widget=forms.HiddenInput())
    product_price = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255)
    contact_number = forms.CharField(max_length=15)
    email_address = forms.EmailField()
    grind = forms.ChoiceField(choices=GRIND_CHOICES)

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if not re.match(r'^\+?\d{10,15}$', contact_number):
            raise forms.ValidationError('Invalid contact number.')
        return contact_number


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'origin_id', 'grind_id', 'size_id', 'manufacturer',
            'name', 'description', 'price', 'currency', 'image'
        ]

    def clean_price(self):
        price = self.cleaned_data.get('price')
        try:
            price = float(price)
        except ValueError:
            raise forms.ValidationError('Invalid price.')
        return price
