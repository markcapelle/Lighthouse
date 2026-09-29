from django.db import models
from django.contrib.auth.models import User
from customers.models import Customer
from products.models import Product
from users.models import UserProfile


class RenewalStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Renewals(models.Model):
    renewalname = models.CharField(max_length=255)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="renewals"
    )

    status = models.ForeignKey(
        RenewalStatus,
        on_delete=models.CASCADE,
        related_name="renewals"
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="renewals"
    )

    customerprice = models.DecimalField(max_digits=10, decimal_places=2)

    startdate = models.DateField()
    enddate = models.DateField()
    reminderdate = models.DateField(blank=True, null=True)

    frequency = models.CharField(max_length=50)  # monthly / annual / custom

    createdbyuser = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="renewals_created"
    )

    updatedbyuser = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="renewals_updated"
    )

    createdat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.renewalname


class RenewalArchive(models.Model):
    renewal = models.ForeignKey(
        Renewals,
        on_delete=models.CASCADE,
        related_name="archive_entries"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    previous_startdate = models.DateField()
    previous_enddate = models.DateField()
    previous_price = models.DecimalField(max_digits=10, decimal_places=2)

    closedat = models.DateTimeField(auto_now_add=True)

    archived_by_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="renewal_archives"
    )

    def __str__(self):
        return f"Archive for {self.renewal.renewalname}"
