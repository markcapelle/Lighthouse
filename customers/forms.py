from django import forms
from .models import Customer
from users.country_codes import COUNTRY_CODES


class CustomerForm(forms.ModelForm):

    countrycode = forms.ChoiceField(choices=COUNTRY_CODES)
    phonenumber = forms.CharField(required=True)

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

        error_messages = {
            "phonenumber": {
                "required": "Please enter a phone number."
            }
        }

        widgets = {
            "customername": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "maincontactname": forms.TextInput(attrs={"class": "form-control"}),
            "maincontactemail": forms.EmailInput(attrs={"class": "form-control"}),
            # REMOVE countrycode from widgets completely
            "phonenumber": forms.TextInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }

    def clean_phonenumber(self):
        number = self.cleaned_data["phonenumber"].strip()
        if number.startswith("0"):
            number = number[1:]
        return number
