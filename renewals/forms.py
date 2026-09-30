from django import forms
from .models import Renewal
from products.models import Product
from customers.models import Customer


class RenewalForm(forms.ModelForm):
    class Meta:
        model = Renewal
        # Field order here is the order the form is displayed in
        fields = [
            "renewalname",
            "status",
            "customer",
            "product",
            "customerprice",
            "startdate",
            "frequency",
            "next_renewal_date",
        ]
        labels = {
            "next_renewal_date": "Renewal Date",
        }
        widgets = {
            "renewalname": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "customer": forms.Select(attrs={"class": "form-select"}),
            "product": forms.Select(attrs={"class": "form-select"}),
            "customerprice": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "startdate": forms.DateInput(attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"),
            "frequency": forms.Select(attrs={"class": "form-select"}),
            "next_renewal_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["next_renewal_date"].required = False

        # Only offer this company's customers/products
        if company is not None:
            self.fields["product"].queryset = Product.objects.filter(company=company)
            self.fields["customer"].queryset = Customer.objects.filter(company=company)

    @property
    def product_data(self):
        """Details shown under the product dropdown once a product is picked."""
        return {
            str(p.pk): {
                "description": p.productdescription or "",
                "costprice": f"{p.costprice:.2f}",
                "rrp": f"{p.rrp:.2f}",
            }
            for p in self.fields["product"].queryset
        }

    def clean(self):
        cleaned = super().clean()
        freq = cleaned.get("frequency")
        if freq == "custom":
            if not cleaned.get("next_renewal_date"):
                self.add_error("next_renewal_date", "Please set a renewal date for a custom frequency.")
        else:
            cleaned["next_renewal_date"] = None  # auto-calculated in model save()
        return cleaned