from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from .models import Company
from .country_codes import COUNTRY_CODES
from django.contrib.auth.password_validation import validate_password


# ---------------------------------------------------------
# REGISTRATION FORM
# ---------------------------------------------------------
class RegistrationForm(forms.Form):
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    countrycode = forms.ChoiceField(choices=COUNTRY_CODES)
    phonenumber = forms.CharField(max_length=50)

    register_type = forms.ChoiceField(
        choices=[
            ("new", "Create New Company"),
            ("existing", "Join Existing Company")
        ]
    )

    company_name = forms.CharField(required=False)
    existing_company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        required=False
    )

    def clean_phonenumber(self):
        number = self.cleaned_data["phonenumber"].strip()
        if number.startswith("0"):
            number = number[1:]
        return number

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords do not match.")

        email = cleaned_data.get("email")
        pw = cleaned_data.get("password1")
        if pw:
            validate_password(pw, user=User(username=email or "", email=email or ""))

        email = cleaned_data.get("email")
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Email already exists.")

        register_type = cleaned_data.get("register_type")

        if register_type == "new":
            if not cleaned_data.get("company_name"):
                raise forms.ValidationError("Please enter a company name.")

        elif register_type == "existing":
            if not cleaned_data.get("existing_company"):
                raise forms.ValidationError("Please select an existing company.")

        return cleaned_data


# ---------------------------------------------------------
# USER SELF-SERVICE PROFILE FORM (normal users)
# ---------------------------------------------------------
class UserSelfServiceForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)

    countrycode = forms.ChoiceField(choices=COUNTRY_CODES)
    phonenumber = forms.CharField(max_length=50)

    mfa_enabled = forms.BooleanField(required=False)

    avatar = forms.ImageField(required=False)
    clear_avatar = forms.BooleanField(required=False)

    def clean_phonenumber(self):
        number = self.cleaned_data["phonenumber"].strip()
        if number.startswith("0"):
            number = number[1:]
        return number


# ---------------------------------------------------------
# ADMIN PROFILE FORM (admins only)
# ---------------------------------------------------------
class AdminProfileForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    countrycode = forms.ChoiceField(choices=COUNTRY_CODES)
    phonenumber = forms.CharField(max_length=50)

    mfa_enabled = forms.BooleanField(required=False)
    is_active = forms.BooleanField(required=False)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)

    avatar = forms.ImageField(required=False)
    clear_avatar = forms.BooleanField(required=False)

    def clean_phonenumber(self):
        number = self.cleaned_data["phonenumber"].strip()
        if number.startswith("0"):
            number = number[1:]
        return number


# ---------------------------------------------------------
# SELF SERVICE PASSWORD CHANGE
# ---------------------------------------------------------
class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()

        if not self.user.check_password(cleaned.get("old_password")):
            raise forms.ValidationError("Old password is incorrect.")

        if cleaned.get("password1") != cleaned.get("password2"):
            raise forms.ValidationError("New passwords do not match.")
        
        if cleaned.get("password1"):
            validate_password(cleaned["password1"], self.user)

        return cleaned


# ---------------------------------------------------------
# ADMIN ASSISTED PASSWORD CHANGE
# ---------------------------------------------------------
class AdminPasswordChangeForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    force_change = forms.BooleanField(required=False, label="Force user to change password on next login")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            raise forms.ValidationError("Passwords do not match.")
        if cleaned.get("password1"):
            validate_password(cleaned["password1"], self.user)
        return cleaned


# ---------------------------------------------------------
# ADMIN FORCED PASSWORD CHANGE
# ---------------------------------------------------------
class ForcedPasswordChangeForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            raise forms.ValidationError("Passwords do not match.")
        if cleaned.get("password1"):
            validate_password(cleaned["password1"], self.user)
        return cleaned
    
