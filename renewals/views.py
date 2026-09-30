from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from .models import Renewal
from .forms import RenewalForm

#RENEWAL LIST
@login_required
@permission_required("renewals.view_renewal", raise_exception=True)
def renewal_list(request):
    company = request.user.profile.company

    # Base queryset (multi-tenant safe)
    renewals = Renewal.objects.filter(
        customer__company=company,
        product__company=company
    ).select_related("product", "customer", "status")

    # --- FILTERS ---
    status_id = request.GET.get("status")
    product_id = request.GET.get("product")
    customer_id = request.GET.get("customer")

    if status_id:
        renewals = renewals.filter(status_id=status_id)

    if product_id:
        renewals = renewals.filter(product_id=product_id)

    if customer_id:
        renewals = renewals.filter(customer_id=customer_id)

    # Dropdown data
    from .models import RenewalStatus
    from products.models import Product
    from customers.models import Customer

    statuses = RenewalStatus.objects.all()
    products = Product.objects.filter(company=company)
    customers = Customer.objects.filter(company=company)

    return render(request, "renewals.html", {
        "renewals": renewals,
        "statuses": statuses,
        "products": products,
        "customers": customers,
    })


#RENEWAL CREATE
@login_required
@permission_required("renewals.add_renewal", raise_exception=True)
def renewal_create(request):
    if request.method == "POST":
        form = RenewalForm(request.POST)
        if form.is_valid():
            renewal = form.save(commit=False)
            renewal.createdbyuser = request.user
            renewal.updatedbyuser = request.user
            renewal.save()
            return redirect("renewals")
    else:
        form = RenewalForm()

    return render(request, "renewal-form.html", {"form": form, "title": "New Renewal"})


#RENEWAL VIEW
@login_required
@permission_required("renewals.view_renewal", raise_exception=True)
def renewal_view(request, renewal_id):
    renewal = get_object_or_404(
        Renewal,
        id=renewal_id,
        customer__company=request.user.profile.company
    )

    return render(request, "renewal-view.html", {"renewal": renewal})


#RENEWAL EDIT
@login_required
@permission_required("renewals.change_renewal", raise_exception=True)
def renewal_edit(request, renewal_id):
    renewal = get_object_or_404(
        Renewal,
        id=renewal_id,
        customer__company=request.user.profile.company
    )

    if request.method == "POST":
        form = RenewalForm(request.POST, instance=renewal)
        if form.is_valid():
            renewal = form.save(commit=False)
            renewal.updatedbyuser = request.user
            renewal.save()

            # AJAX autosave support
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"saved": True})

            return redirect("renewal_view", renewal.id)
    else:
        form = RenewalForm(instance=renewal)

    return render(request, "renewal-edit.html", {"form": form, "renewal": renewal})


#RENEWAL DELETE
@login_required
@permission_required("renewals.delete_renewal", raise_exception=True)
def renewal_delete(request, renewal_id):
    renewal = get_object_or_404(
        Renewal,
        id=renewal_id,
        customer__company=request.user.profile.company
    )

    if request.method == "POST":
        renewal.delete()
        return redirect("renewals")

    return render(request, "renewal-delete.html", {"renewal": renewal})

