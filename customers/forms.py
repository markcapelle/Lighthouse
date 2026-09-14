from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer

        fields = [
            "customername",
            "address",
            "maincontactname",
            "maincontactemail",
            "countrycode",
            "phonenumber",
            "notes",
        ]

        widgets = {
            "customername": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "address": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "maincontactname": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "maincontactemail": forms.EmailInput(
                attrs={"class": "form-control"}
            ),
            "countrycode": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "phonenumber": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "notes": forms.Textarea(
                attrs={"class": "form-control", "rows": 5}
            ),
        }