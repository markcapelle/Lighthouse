from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from .models import Company



class RegistrationForm(forms.Form):
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    countrycode = forms.CharField(max_length=10)
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

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords do not match.")

        email = cleaned_data.get("email")

        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Email already exists.")

        register_type = cleaned_data.get("register_type")

        if register_type == "new":
            if not cleaned_data.get("company_name"):
                raise forms.ValidationError(
                    "Please enter a company name."
                )

        elif register_type == "existing":
            if not cleaned_data.get("existing_company"):
                raise forms.ValidationError(
                    "Please select an existing company."
                )

        return cleaned_data



class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    countrycode = forms.CharField(max_length=10)
    phonenumber = forms.CharField(max_length=50)
    mfa_enabled = forms.BooleanField(required=False)
    is_active = forms.BooleanField(required=False)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)

    avatar = forms.ImageField(required=False)
    clear_avatar = forms.BooleanField(required=False)



#SELF SERVICE PASSWORD CHANGE
class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()

        # Validate old password
        old_pw = cleaned.get("old_password")
        if not self.user.check_password(old_pw):
            raise forms.ValidationError("Old password is incorrect.")

        # Validate new passwords match
        if cleaned.get("password1") != cleaned.get("password2"):
            raise forms.ValidationError("New passwords do not match.")

        return cleaned


#ADMIN ASSISTED PASSWORD CHANGE
class AdminPasswordChangeForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    force_change = forms.BooleanField(required=False, label="Force user to change password on next login")

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned


#ADMIN FORCED PASSWORD CHANGE
class ForcedPasswordChangeForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned
