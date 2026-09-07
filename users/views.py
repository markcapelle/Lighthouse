from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from .models import Company, UserProfile
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required, user_passes_test




from django.contrib.auth.decorators import permission_required

@login_required
@permission_required("users.view_userprofile", raise_exception=True)
def user_management(request):
    users = UserProfile.objects.filter(
        company=request.user.profile.company
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