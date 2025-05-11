from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "shipping_full_name"}), required=True)
    shipping_email = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "shipping_email"}), required=True)
    shipping_address1 = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "shipping_address1"}), required=True)
    shipping_address2 = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "shipping_address2"}), required=True)
    shipping_city = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "shipping_city"}), required=True)
    shipping_state = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "shipping_state"}), required=False)
    shipping_zipcode = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "shipping_zipcode"}), required=False)
    shipping_country = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "shipping_country"}), required=True)

    class Meta:
        model= ShippingAddress
        fields = ["", "", "", "", "", "", "","", "", ""]
        exclude = ["user", ]
