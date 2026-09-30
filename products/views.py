from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from .models import Product
from .forms import ProductForm
from renewals.models import Renewal


#PRODUCT LIST
@login_required
@permission_required("products.view_product", raise_exception=True)
def product_list(request):
    products = Product.objects.filter(company=request.user.profile.company)
    return render(request, "products.html", {"products": products})


#PRODUCT CREATE
@login_required
@permission_required("products.add_product", raise_exception=True)
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.company = request.user.profile.company
            product.save()
            return redirect("products")
    else:
        form = ProductForm()

    return render(request, "product-form.html", {"form": form, "title": "New Product"})


#PRODUCT VIEW
@login_required
@permission_required("products.view_product", raise_exception=True)
def product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id, company=request.user.profile.company)

    # Filter renewals for this product
    renewals = Renewal.objects.filter(
        product=product,
        customer__company=request.user.profile.company
    ).select_related("customer", "status")

    return render(request, "product-view.html", {
        "product": product,
        "renewals": renewals
    })


#PRODUCT EDIT
@login_required
@permission_required("products.change_product", raise_exception=True)
def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id, company=request.user.profile.company)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()

            # AJAX autosave
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"saved": True})

            return redirect("product_view", product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, "product-edit.html", {"form": form, "product": product})


#PRODUCT DELETE
@login_required
@permission_required("products.delete_product", raise_exception=True)
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id, company=request.user.profile.company)

    if request.method == "POST":
        product.delete()
        return redirect("products")

    return render(request, "product-delete.html", {"product": product})
