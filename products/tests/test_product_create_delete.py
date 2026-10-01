from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal

from users.models import Company, UserProfile
from products.forms import ProductForm
from products.models import Product


class ProductCreateDeleteTests(TestCase):

    def setUp(self):
        # Create company
        self.company = Company.objects.create(name="TestCorp")

        # Create user + profile manually (signals don't fire in tests)
        self.user = User.objects.create(username="tester")
        UserProfile.objects.create(user=self.user, company=self.company)

    def test_create_product(self):
        form = ProductForm(data={
            "productname": "Widget Pro",
            "productcode": "WP-100",
            "productdescription": "High-end widget for enterprise clients.",
            "costprice": "49.99",
            "rrp": "99.99",
        })

        # Form should be valid
        self.assertTrue(form.is_valid(), form.errors)

        # Save product with company assignment (same as your view logic)
        product = form.save(commit=False)
        product.company = self.company
        product.save()

        # Verify product exists
        self.assertEqual(Product.objects.count(), 1)

        saved = Product.objects.first()

        # Field checks
        self.assertEqual(saved.productname, "Widget Pro")
        self.assertEqual(saved.productcode, "WP-100")
        self.assertEqual(saved.productdescription, "High-end widget for enterprise clients.")
        self.assertEqual(saved.costprice, Decimal("49.99"))
        self.assertEqual(saved.rrp, Decimal("99.99"))
        self.assertEqual(saved.company, self.company)

    def test_delete_product(self):
        # Create a product directly
        product = Product.objects.create(
            company=self.company,
            productname="DeleteMe",
            productcode="DM-01",
            productdescription="Temporary product",
            costprice=Decimal("10.00"),
            rrp=Decimal("20.00"),
        )

        self.assertEqual(Product.objects.count(), 1)

        # Delete it
        product.delete()

        # Verify deletion
        self.assertEqual(Product.objects.count(), 0)
