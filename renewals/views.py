from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse

from .models import Renewal, RenewalStatus, RenewalArchive
from .forms import RenewalForm

# RENEWAL LIST
@login_required
@permission_required("renewals.view_renewal", raise_exception=True)
def renewal_list(request):
    company = request.user.profile.company

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


# RENEWAL CREATE
@login_required
@permission_required("renewals.add_renewal", raise_exception=True)
def renewal_create(request):
    company = request.user.profile.company

    if request.method == "POST":
        form = RenewalForm(request.POST, company=company)
        if form.is_valid():
            renewal = form.save(commit=False)
            renewal.createdbyuser = request.user
            renewal.updatedbyuser = request.user
            renewal.save()  # auto-calculates customerprice
            return redirect("renewals")
    else:
        form = RenewalForm(company=company)

    return render(request, "renewal-form.html", {"form": form, "title": "New Renewal"})


# RENEWAL VIEW
@login_required
@permission_required("renewals.view_renewal", raise_exception=True)
def renewal_view(request, renewal_id):
    renewal = get_object_or_404(
        Renewal,
        id=renewal_id,
        customer__company=request.user.profile.company
    )
    return render(request, "renewal-view.html", {"renewal": renewal})


# RENEWAL EDIT
@login_required
@permission_required("renewals.change_renewal", raise_exception=True)
def renewal_edit(request, renewal_id):
    company = request.user.profile.company
    renewal = get_object_or_404(
        Renewal,
        id=renewal_id,
        customer__company=company
    )

    if request.method == "POST":
        form = RenewalForm(request.POST, instance=renewal, company=company)
        if form.is_valid():
            renewal = form.save(commit=False)
            renewal.updatedbyuser = request.user

            rollover_happened = False

            # --- HANDLE CLOSING / ARCHIVING / ROLLOVER ---
            if renewal.status.name.lower() == "closed":
                from renewals.models import RenewalArchive
                from django.utils import timezone

                # Archive snapshot
                RenewalArchive.objects.create(
                    renewalname=renewal.renewalname,
                    customer=renewal.customer,
                    product=renewal.product,
                    status=renewal.status,
                    count=renewal.count,
                    customerprice=renewal.customerprice,
                    startdate=renewal.startdate,
                    next_renewal_date=renewal.next_renewal_date,
                    frequency=renewal.frequency,
                )

                # Reset renewal for next cycle
                today = timezone.now().date()
                renewal.startdate = today

                if renewal.frequency != "custom":
                    renewal.next_renewal_date = renewal.calculate_next_renewal()
                else:
                    renewal.next_renewal_date = None

                # Set status back to Open
                active_status = RenewalStatus.objects.get(name="Open")
                renewal.status = active_status

                rollover_happened = True

            # Save renewal
            renewal.save()

            # AJAX autosave support
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"saved": True})

            # Redirect logic
            if rollover_happened:
                # After closing → go back to edit
                return redirect("renewal_edit", renewal.id)
            else:
                # Normal save → go to view page
                return redirect("renewal_view", renewal.id)

    else:
        form = RenewalForm(instance=renewal, company=company)

    return render(request, "renewal-edit.html", {"form": form, "renewal": renewal})




# RENEWAL DELETE
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


#VIEW ARCHIVE
@login_required
@permission_required("renewals.view_renewalarchive", raise_exception=True)
def renewal_archive_list(request):
    archives = RenewalArchive.objects.filter(
        customer__company=request.user.profile.company
    ).select_related("customer", "product", "status")

    return render(request, "archive.html", {"archives": archives})
