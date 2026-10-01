from django.test import TestCase
from django.contrib.auth.models import User
from users.forms import RegistrationForm
from users.models import Company


class RegistrationFormTests(TestCase):

    def setUp(self):
        # Create a company for "existing" registration tests
        self.company = Company.objects.create(name="TestCorp")

        # Create a user to test duplicate email validation
        User.objects.create(username="existing@example.com")

    def test_passwords_must_match(self):
        form = RegistrationForm(data={
            "email": "new@example.com",
            "password1": "abc123",
            "password2": "different",
            "countrycode": "+353",
            "phonenumber": "0871234567",
            "register_type": "new",
            "company_name": "MyCo"
        })

        self.assertFalse(form.is_valid())
        self.assertIn("Passwords do not match.", form.errors["__all__"])

    def test_duplicate_email_fails(self):
        form = RegistrationForm(data={
            "email": "existing@example.com",
            "password1": "abc123",
            "password2": "abc123",
            "countrycode": "+353",
            "phonenumber": "0871234567",
            "register_type": "new",
            "company_name": "MyCo"
        })

        self.assertFalse(form.is_valid())
        self.assertIn("Email already exists.", form.errors["__all__"])

    def test_new_company_requires_company_name(self):
        form = RegistrationForm(data={
            "email": "new@example.com",
            "password1": "abc123",
            "password2": "abc123",
            "countrycode": "+353",
            "phonenumber": "0871234567",
            "register_type": "new",
            "company_name": ""  # Missing
        })

        self.assertFalse(form.is_valid())
        self.assertIn("Please enter a company name.", form.errors["__all__"])

    def test_existing_company_requires_selection(self):
        form = RegistrationForm(data={
            "email": "new@example.com",
            "password1": "abc123",
            "password2": "abc123",
            "countrycode": "+353",
            "phonenumber": "0871234567",
            "register_type": "existing",
            "existing_company": None  # Missing
        })

        self.assertFalse(form.is_valid())
        self.assertIn("Please select an existing company.", form.errors["__all__"])

    def test_phonenumber_strips_leading_zero(self):
        form = RegistrationForm(data={
            "email": "new@example.com",
            "password1": "abc123",
            "password2": "abc123",
            "countrycode": "+353",
            "phonenumber": "0871234567",
            "register_type": "new",
            "company_name": "MyCo"
        })

        self.assertTrue(form.is_valid())
        cleaned = form.clean_phonenumber()
        self.assertEqual(cleaned, "871234567")
