from django.db import models
from users.models import Company


class Customer(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="customers"
    )

    customername = models.CharField(max_length=255)

    address = models.TextField(
        blank=True,
        null=True
    )

    maincontactname = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    maincontactemail = models.EmailField(
        blank=True,
        null=True
    )

    countrycode = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    phonenumber = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.customername