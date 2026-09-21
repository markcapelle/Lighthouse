from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Product

@login_required
@permission_required("products.view_product", raise_exception=True)
def product_list(request):
    products = Product.objects.filter(company=request.user.profile.company)
    return render(request, "products.html", {"products": products})

@login_required
@permission_required("products.add_product", raise_exception=True)
def product_create(request):
    return render(request, "product-form.html")

@login_required
@permission_required("products.view_product", raise_exception=True)
def product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id, company=request.user.profile.company)
    return render(request, "product-view.html", {"product": product})

@login_required
@permission_required("products.change_product", raise_exception=True)
def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id, company=request.user.profile.company)
    return render(request, "product-edit.html", {"product": product})

@login_required
@permission_required("products.delete_product", raise_exception=True)
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id, company=request.user.profile.company)
    return render(request, "product-delete.html", {"product": product})
