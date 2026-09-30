from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from .models import Company, UserProfile
from .forms import RegistrationForm, ProfileForm, PasswordChangeForm, AdminPasswordChangeForm, ForcedPasswordChangeForm
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from anymail.message import AnymailMessage
import cloudinary.uploader
from django.utils import timezone
from datetime import timedelta
import random

from users.services.weather import get_weekend_forecast, describe
from users.services.ireland_locations import COUNTY_COORDS

@login_required
@permission_required("users.view_userprofile", raise_exception=True)
def user_management(request):
    users = (
        UserProfile.objects
        .filter(
            company=request.user.profile.company
        )
        .select_related("user")
    )

    return render(
        request,
        "user-management.html",
        {"users": users}
    )



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:

            # --- MFA CHECK ---
            if user.profile.mfa_enabled:
                code = f"{random.randint(100000, 999999)}"
                user.profile.mfa_code = code
                user.profile.mfa_expires = timezone.now() + timedelta(minutes=10)
                user.profile.save()

                # Email the code
                msg = AnymailMessage(
                    subject="Your Lighthouse Login Code",
                    body=f"Your verification code is: {code}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user.email],
                )
                msg.send()

                # Store MFA session flags
                request.session["mfa_user_id"] = user.id
                request.session["mfa_pending"] = True

                return redirect("mfa_verify")

            # --- NORMAL LOGIN ---
            login(request, user)

            # Forced password change check
            if user.profile.force_password_change:
                return redirect("forced_password_change")

            return redirect("dashboard")

        # Invalid login
        return render(request, "login.html", {"error": "Invalid username or password"})

    return render(request, "login.html")




def logout_view(request):
    logout(request)
    return redirect("/")



@login_required
def dashboard_view(request):
    from renewals.models import Renewal
    from django.utils import timezone
    from datetime import timedelta

    company = request.user.profile.company

    # Handle county selection
    selected_county = request.POST.get("county", "Dublin")
    lat, lon = COUNTY_COORDS[selected_county]

    weekend_weather = get_weekend_forecast(lat, lon)

    if weekend_weather:
        for day in weekend_weather.values():
            day["description"] = describe(day["code"])

    # Renewals
    today = timezone.now().date()
    seven_days = today + timedelta(days=7)

    renewals = Renewal.objects.filter(
        customer__company=company,
        product__company=company,
        next_renewal_date__lte=seven_days
    )

    return render(request, "dashboard.html", {
        "renewals": renewals,
        "weekend_weather": weekend_weather,
        "counties": COUNTY_COORDS.keys(),
        "selected_county": selected_county,
    })





def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]

            user = User.objects.create_user(
                username=email,
                email=email,
                password=form.cleaned_data["password1"]
            )

            registration_type = form.cleaned_data["register_type"]

            if registration_type == "new":
                company = Company.objects.create(
                    name=form.cleaned_data["company_name"]
                )

                user.is_active = True
                user.save()

                admin_group, _ = Group.objects.get_or_create(
                    name="Administrator"
                )

                user.groups.add(admin_group)

                approved = True

            else:
                company = form.cleaned_data["existing_company"]

                user.is_active = False
                user.save()

                approved = False

            UserProfile.objects.create(
                user=user,
                company=company,
                countrycode=form.cleaned_data["countrycode"],
                phonenumber=form.cleaned_data["phonenumber"],
                approved=approved
            )

            if registration_type == "new":
                return redirect("/login")

            return render(
                request,
                "registration-pending.html"
            )

    else:
        form = RegistrationForm()

    return render(
        request,
        "register.html",
        {"form": form}
    )



@login_required
def profile_view(request):

    return render(
        request,
        "profile-view.html",
        {
            "profile": request.user.profile
        }
    )



def edit_profile_common(request, profile, redirect_to_view=True):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user = profile.user
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.username = form.cleaned_data["email"]

            profile.countrycode = form.cleaned_data["countrycode"]
            profile.phonenumber = form.cleaned_data["phonenumber"]
            profile.mfa_enabled = form.cleaned_data.get("mfa_enabled", False)

            user.is_active = form.cleaned_data.get("is_active", True)

            # Clear avatar
            if form.cleaned_data.get("clear_avatar"):
                profile.avatar_url = None

            # Upload avatar
            if form.cleaned_data.get("avatar"):
                upload = cloudinary.uploader.upload(
                    form.cleaned_data["avatar"],
                    folder="avatars"
                )
                profile.avatar_url = upload["secure_url"]

            # Update user group
            new_group = form.cleaned_data.get("group")
            user.groups.clear()
            if new_group:
                user.groups.add(new_group)

            user.save()
            profile.save()

            return redirect("view_user", profile.id) if redirect_to_view else redirect("profile")


        return render(
            request,
            "profile-edit.html",
            {
                "form": form,
                "profile": profile,
            }
        )

    else:
        form = ProfileForm(
            initial={
                "first_name": profile.user.first_name,
                "last_name": profile.user.last_name,
                "email": profile.user.email,
                "countrycode": profile.countrycode,
                "phonenumber": profile.phonenumber,
                "mfa_enabled": profile.mfa_enabled,
                "is_active": profile.user.is_active,
                "group": profile.user.groups.first(),
            }
        )

        return render(
            request,
            "profile-edit.html",
            {
                "form": form,
                "profile": profile,
            }
        )



@login_required
def edit_profile(request):
    return edit_profile_common(request, request.user.profile, redirect_to_view=False)




@login_required
@permission_required("users.view_userprofile", raise_exception=True)
def view_user(request, profile_id):
    profile = get_object_or_404(
        UserProfile,
        id=profile_id,
        company=request.user.profile.company
    )

    return render(
        request,
        "profile-view.html",
        {
            "profile": profile
        }
    )


@login_required
@permission_required("users.change_userprofile", raise_exception=True)
def edit_user(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id, company=request.user.profile.company)
    return edit_profile_common(request, profile, redirect_to_view=True)



#DELETE USER
@login_required
@permission_required("users.delete_userprofile", raise_exception=True)
def delete_user(request, profile_id):
    profile = get_object_or_404(
        UserProfile,
        id=profile_id,
        company=request.user.profile.company
    )

    if profile.user == request.user:

        return redirect(
            "manage_users"
        )

    if request.method == "POST":

        profile.user.delete()

        return redirect(
            "manage_users"
        )

    return render(
        request,
        "delete-user.html",
        {
            "profile": profile
        }
    )


#SELF SERVICE CHANGE PASSWORD
@login_required
def change_password(request):
    profile = request.user.profile

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            new_pw = form.cleaned_data["password1"]
            request.user.set_password(new_pw)
            request.user.save()

            # NEW: clear forced password change flag
            profile.force_password_change = False
            profile.save()

            return redirect("login")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "password-change.html", {"form": form, "profile": profile})




#ADMIN CHANGE USER PASSWORD
@login_required
@permission_required("users.change_userprofile", raise_exception=True)
def change_user_password(request, profile_id):
    profile = get_object_or_404(
        UserProfile,
        id=profile_id,
        company=request.user.profile.company
    )

    if request.method == "POST":
        form = AdminPasswordChangeForm(request.POST)
        if form.is_valid():
            new_pw = form.cleaned_data["password1"]
            profile.user.set_password(new_pw)
            profile.user.save()

            # NEW: force password change flag
            if form.cleaned_data.get("force_change"):
                profile.force_password_change = True
                profile.save()

            return redirect("view_user", profile.id)
    else:
        form = AdminPasswordChangeForm()

    return render(request, "password-change.html", {"form": form, "profile": profile})



# REQUEST ADMIN HELP FOR PASSWORD RESET
def password_reset_contact_admin(request):
    if request.method == "POST":
        email = request.POST.get("email")

        # If no email entered, just show success page (no info leak)
        if not email:
            return render(request, "password-reset-admin-done.html")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Do NOT reveal that the email doesn't exist
            return render(request, "password-reset-admin-done.html")

        # Find administrators in the same company
        company = user.profile.company
        admin_group = Group.objects.get(name="Administrator")

        admins = User.objects.filter(
            groups=admin_group,
            profile__company=company
        )

        admin_emails = [a.email for a in admins if a.email]

        if admin_emails:
            msg = AnymailMessage(
                subject="Password Reset Assistance Requested",
                body=f"The user {user.email} requires help resetting their password.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=admin_emails,   # Brevo will now send to ALL recipients
            )

            msg.send()

        return render(request, "password-reset-admin-done.html")

    # Fallback: show normal reset page
    return render(request, "password-reset.html")


#FORCE PASSWORD CHANGE
@login_required
def forced_password_change(request):
    profile = request.user.profile

    if not profile.force_password_change:
        return redirect("dashboard")

    if request.method == "POST":
        form = ForcedPasswordChangeForm(request.POST)
        if form.is_valid():
            new_pw = form.cleaned_data["password1"]
            request.user.set_password(new_pw)
            request.user.save()

            profile.force_password_change = False
            profile.save()

            # Re-authenticate user so they don't get logged out
            user = authenticate(username=request.user.username, password=new_pw)
            login(request, user)

            return redirect("dashboard")
    else:
        form = ForcedPasswordChangeForm()

    return render(request, "password-change-forced.html", {"form": form})


#MFA VERIFICATION
def mfa_verify(request):
    user_id = request.session.get("mfa_user_id")
    if not user_id:
        return redirect("login")

    user = User.objects.get(id=user_id)
    profile = user.profile

    if request.method == "POST":
        code = request.POST.get("code")

        if (
            profile.mfa_code == code
            and profile.mfa_expires
            and profile.mfa_expires > timezone.now()
        ):
            # Clear MFA code
            profile.mfa_code = None
            profile.mfa_expires = None
            profile.save()

            # COMPLETE MFA
            request.session["mfa_pending"] = False   # <-- REQUIRED
            request.session["mfa_user_id"] = None    # optional cleanup

            # Log the user in
            login(request, user)

            return redirect("dashboard")

        return render(request, "mfa-verify.html", {"error": "Invalid or expired code"})

    return render(request, "mfa-verify.html")
