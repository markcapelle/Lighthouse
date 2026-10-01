from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date

from users.models import Company, UserProfile
from customers.models import Customer
from products.models import Product
from renewals.models import Renewal, RenewalStatus


class RenewalCascadeTests(TestCase):

    def setUp(self):
        # Company
        self.company = Company.objects.create(name="TestCorp")

        # User + profile
        self.user = User.objects.create(username="tester")
        UserProfile.objects.create(user=self.user, company=self.company)

        # Status
        self.status_open = RenewalStatus.objects.create(name="Open")

    def create_customer(self):
        return Customer.objects.create(
            company=self.company,
            customername="Acme Ltd",
            address="123 Road",
            maincontactname="John",
            maincontactemail="john@example.com",
            countrycode="+353",
            phonenumber="871234567",
        )

    def create_product(self):
        return Product.objects.create(
            company=self.company,
            productname="Widget Pro",
            productcode="WP-100",
            productdescription="High-end widget",
            costprice=Decimal("50.00"),
            rrp=Decimal("100.00"),
        )

    def create_renewal(self, customer, product):
        return Renewal.objects.create(
            renewalname="Acme Annual",
            customer=customer,
            product=product,
            status=self.status_open,
            count=5,
            startdate=date(2024, 1, 1),   # IMPORTANT: must be a real date object
            frequency="annual",
            createdbyuser=self.user,
            updatedbyuser=self.user,
        )

    def test_full_cascade_sequence(self):
        # Create customer, product, renewal
        customer = self.create_customer()
        product = self.create_product()
        renewal = self.create_renewal(customer, product)

        self.assertEqual(Renewal.objects.count(), 1)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Product.objects.count(), 1)

        # Test 2: Delete renewal → customer & product should remain
        renewal.delete()

        self.assertEqual(Renewal.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Product.objects.count(), 1)

        # Recreate renewal
        renewal = self.create_renewal(customer, product)
        
        # Test 2: Delete product → renewal should also be deleted, customer should remain
        product.delete()

        self.assertEqual(Product.objects.count(), 0)
        self.assertEqual(Renewal.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 1)

        # Recreate product and renewal
        product = self.create_product()
        renewal = self.create_renewal(customer, product)

        # Test 3: Delete customer → renewal should also be deleted, product should remain
        customer.delete()

        self.assertEqual(Customer.objects.count(), 0)
        self.assertEqual(Renewal.objects.count(), 0)
        self.assertEqual(Product.objects.count(), 1)
