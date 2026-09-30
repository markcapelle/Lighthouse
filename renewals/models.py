from django.db import models
from django.contrib.auth.models import User
from customers.models import Customer
from products.models import Product
from dateutil.relativedelta import relativedelta
from datetime import timedelta


class RenewalStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Renewal(models.Model):
    FREQUENCY_CHOICES = [
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("annual", "Annual"),
        ("custom", "Custom"),
    ]

    renewalname = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.ForeignKey(RenewalStatus, on_delete=models.CASCADE)

    # NEW FIELD: number of licences
    count = models.PositiveIntegerField(default=1)

    # Auto-calculated based on product price × count
    customerprice = models.DecimalField(max_digits=10, decimal_places=2)

    startdate = models.DateField()
    next_renewal_date = models.DateField(blank=True, null=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)

    createdbyuser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="renewals_created")
    updatedbyuser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="renewals_updated")
    createdat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now=True)

    def calculate_next_renewal(self):
        if self.frequency == "weekly":
            return self.startdate + timedelta(weeks=1)
        elif self.frequency == "monthly":
            return self.startdate + relativedelta(months=1)
        elif self.frequency == "annual":
            return self.startdate + relativedelta(years=1)
        else:
            return self.next_renewal_date  # custom → user sets manually

    def calculate_customer_price(self):
        # Uses product.costprice — change to product.rrp if needed
        return self.product.costprice * self.count

    def save(self, *args, **kwargs):
        # Auto-calc renewal date
        if self.frequency != "custom":
            self.next_renewal_date = self.calculate_next_renewal()

        # Auto-calc customer price
        self.customerprice = self.calculate_customer_price()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.renewalname
