from django import forms

class EnquiryForm(forms.Form):
    product_name = forms.CharField(widget=forms.HiddenInput())
    product_price = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea)
    contact_number = forms.CharField(max_length=15)
    email_address = forms.EmailField()
    grind = forms.ChoiceField(choices=[('Coarse', 'Coarse'), ('Medium', 'Medium'), ('Fine', 'Fine')])