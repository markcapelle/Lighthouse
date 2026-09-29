from django import forms
from .models import Renewal

class RenewalForm(forms.ModelForm):
    class Meta:
        model = Renewal
        fields = [
            "renewalname",
            "product",
            "customer",
            "status",
            "customerprice",
            "startdate",
            "frequency",
            "next_renewal_date",
        ]
        widgets = {
            "renewalname": forms.TextInput(attrs={"class": "form-control"}),
            "product": forms.Select(attrs={"class": "form-control"}),
            "customer": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "customerprice": forms.NumberInput(attrs={"class": "form-control"}),
            "startdate": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "frequency": forms.Select(attrs={"class": "form-control"}),
            "next_renewal_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def clean(self):
        cleaned = super().clean()
        freq = cleaned.get("frequency")

        if freq != "custom":
            cleaned["next_renewal_date"] = None  # auto-calculated in model save()

        return cleaned
