from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from .models import Renewal
from .forms import RenewalForm

@login_required
@permission_required("renewals.view_renewal", raise_exception=True)
def renewal_list(request):
    renewals = Renewal.objects.filter(
        customer__company=request.user.profile.company
    ).select_related("product", "customer", "status")

    return render(request, "renewals.html", {"renewals": renewals})


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


@login_required
@permission_required("renewals.view_renewal", raise_exception=True)
def renewal_view(request, renewal_id):
    renewal = get_object_or_404(
        Renewal,
        id=renewal_id,
        customer__company=request.user.profile.company
    )

    return render(request, "renewal-view.html", {"renewal": renewal})



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

