from django.db import models
from users.models import Company

class Product(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="products"
    )

    productname = models.CharField(max_length=255)
    productcode = models.CharField(max_length=100, blank=True, null=True)
    productdescription = models.TextField(blank=True, null=True)

    costprice = models.DecimalField(max_digits=10, decimal_places=2)
    rrp = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.productname
