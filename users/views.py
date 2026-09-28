from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from .models import Company, UserProfile
from .forms import RegistrationForm, ProfileForm, PasswordChangeForm, AdminPasswordChangeForm
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from anymail.message import AnymailMessage


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
            login(request, user)
            return redirect("/dashboard")
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("/")



@login_required
def dashboard_view(request):
    return render(request, "dashboard.html")



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

        form = ProfileForm(request.POST)

        if form.is_valid():

            user = profile.user

            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.username = form.cleaned_data["email"]

            profile.countrycode = (form.cleaned_data["countrycode"])
            profile.phonenumber = (form.cleaned_data["phonenumber"])

            profile.mfa_enabled = form.cleaned_data.get("mfa_enabled", False)
            if request.user.groups.filter(name="Administrator").exists():
                user.is_active = form.cleaned_data.get("is_active", True)

            if request.user.groups.filter(name="Administrator").exists():
                selected_group = form.cleaned_data.get("group")
                profile.user.groups.clear()
                if selected_group:  
                    profile.user.groups.add(selected_group)

            user.save()
            profile.save()

            if redirect_to_view:
                # Admin editing another user → go to that user's profile
                return redirect("view_user", profile.id)
            else:
                # User editing self → go to their own profile
                return redirect("profile")


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
