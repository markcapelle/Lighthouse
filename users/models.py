from django.db import models
from django.contrib.auth.models import User, Group


class Company(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """
    Extends Django's built-in User model.
    Stores tenant/company info and additional user metadata.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="users"
    )

    countrycode = models.CharField(max_length=10, blank=True, null=True)
    phonenumber = models.CharField(max_length=50, blank=True, null=True)

    approved = models.BooleanField(default=False)

    mfa_enabled = models.BooleanField(default=False)
    avatar_url = models.CharField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
