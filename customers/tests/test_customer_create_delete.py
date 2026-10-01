from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Company, UserProfile
from customers.forms import CustomerForm
from customers.models import Customer


class CustomerCreateDeleteTests(TestCase):

    def setUp(self):
        # Create company
        self.company = Company.objects.create(name="TestCorp")

        # Create user + profile manually (signals don't fire in tests)
        self.user = User.objects.create(username="tester")
        UserProfile.objects.create(user=self.user, company=self.company)

    def test_create_customer(self):
        form = CustomerForm(data={
            "customername": "Acme Ltd",
            "address": "123 Road",
            "maincontactname": "John Doe",
            "maincontactemail": "john@example.com",
            "countrycode": "+353",
            "phonenumber": "0871234567",
            "notes": "Important client"
        })

        self.assertTrue(form.is_valid(), form.errors)

        customer = form.save(commit=False)
        customer.company = self.company
        customer.save()

        self.assertEqual(Customer.objects.count(), 1)

        saved = Customer.objects.first()
        self.assertEqual(saved.customername, "Acme Ltd")
        self.assertEqual(saved.phonenumber, "871234567")  # cleaned
        self.assertEqual(saved.company, self.company)

    def test_delete_customer(self):
        customer = Customer.objects.create(
            company=self.company,
            customername="DeleteMe Ltd",
            address="Somewhere",
            maincontactname="Jane",
            maincontactemail="jane@example.com",
            countrycode="+353",
            phonenumber="871234567",
            notes="Temporary"
        )

        self.assertEqual(Customer.objects.count(), 1)

        customer.delete()

        self.assertEqual(Customer.objects.count(), 0)
