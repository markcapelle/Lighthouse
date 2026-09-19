from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Customer
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


@login_required
def customer_view(request, customer_id):
    customer = get_object_or_404(
        Customer,
        id=customer_id,
        company=request.user.profile.company
    )
    return render(request, "customer-view.html", {"customer": customer})



@login_required
def customer_edit(request, customer_id):
    customer = get_object_or_404(
        Customer,
        id=customer_id,
        company=request.user.profile.company
    )

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"saved": True})
            return redirect("customer_view", customer.id)
    else:
        form = CustomerForm(instance=customer)

    return render(
        request,
        "customer-edit.html",
        {"form": form, "customer": customer}
    )


@login_required
def customer_delete(request, customer_id):
    customer = get_object_or_404(
        Customer,
        id=customer_id,
        company=request.user.profile.company
    )

    if request.method == "POST":
        customer.delete()
        return redirect("customers")

    return render(
        request,
        "customer-delete.html",
        {"customer": customer}
    )
