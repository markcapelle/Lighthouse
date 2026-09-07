from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from .models import Company, UserProfile
from .forms import RegistrationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django import forms



from django.contrib.auth.decorators import permission_required

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


class ProfileForm(forms.Form):
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )

    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control"}
        )
    )

    countrycode = forms.CharField(
        max_length=10,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )

    phonenumber = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
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


def edit_profile_common(request, profile):
    if request.method == "POST":

        form = ProfileForm(request.POST)

        if form.is_valid():

            user = profile.user

            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.username = form.cleaned_data["email"]

            profile.countrycode = (
                form.cleaned_data["countrycode"]
            )

            profile.phonenumber = (
                form.cleaned_data["phonenumber"]
            )

            user.save()
            profile.save()

            return redirect("profile")

    else:

        form = ProfileForm(
            initial={
                "first_name": profile.user.first_name,
                "last_name": profile.user.last_name,
                "email": profile.user.email,
                "countrycode": profile.countrycode,
                "phonenumber": profile.phonenumber,
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

    return edit_profile_common(
        request,
        request.user.profile
    )



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
    profile = get_object_or_404(
        UserProfile,
        id=profile_id,
        company=request.user.profile.company
    )

    return edit_profile_common(
        request,
        profile
    )


# DELETE USER
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