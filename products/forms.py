from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "productname",
            "productcode",
            "productdescription",
            "costprice",
            "rrp",
        ]
        widgets = {
            "productname": forms.TextInput(attrs={"class": "form-control"}),
            "productcode": forms.TextInput(attrs={"class": "form-control"}),
            "productdescription": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "costprice": forms.NumberInput(attrs={"class": "form-control"}),
            "rrp": forms.NumberInput(attrs={"class": "form-control"}),
        }
