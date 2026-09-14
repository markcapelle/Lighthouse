from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Customer

from django.shortcuts import render, redirect
from .forms import CustomerForm




@login_required
def customer_list(request):

    customers = Customer.objects.filter(
        company=request.user.profile.company
    )

    return render(
        request,
        "customers.html",
        {
            "customers": customers
        }
    )

@login_required
def customer_create(request):

    if request.method == "POST":

        form = CustomerForm(request.POST)

        if form.is_valid():

            customer = form.save(commit=False)

            customer.company = (
                request.user.profile.company
            )

            customer.save()

            return redirect("customers")

    else:

        form = CustomerForm()

    return render(
        request,
        "customer-form.html",
        {
            "form": form,
            "title": "New Customer"
        }
    )