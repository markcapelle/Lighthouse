from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect, render
from django.contrib.auth import views as auth_views
from customers.views import customer_list, customer_create, customer_view, customer_edit, customer_delete
from products.views import product_list, product_create, product_view, product_edit, product_delete
from renewals.views import renewal_list, renewal_create, renewal_view, renewal_edit, renewal_delete, renewal_archive_list

from users.views import (
    login_view, logout_view, dashboard_view, register_view, profile_view, edit_profile, user_management, 
    view_user, edit_user, delete_user, 
    change_password, change_user_password, password_reset_contact_admin, forced_password_change,
    mfa_verify
)

def index(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "index.html")


urlpatterns = [
    #INDEX
    path('', index, name='index'),
    path('index/', index, name='index_page'),

    #LOGIN/LOGOUT
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    #USERSTUFF
    path('dashboard/', dashboard_view, name='dashboard'),
    path('admin/', admin.site.urls),
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("manage-users/", user_management, name="manage_users"),
    path("users/<int:profile_id>/",  view_user, name="view_user"),
    path( "users/<int:profile_id>/edit/", edit_user, name="edit_user"),
    path("users/<int:profile_id>/delete/", delete_user, name="delete_user"),

    #CUSTOMERS
    path("customers/", customer_list, name="customers"),
    path("customers/new/", customer_create, name="customer_create"),
    path("customers/<int:customer_id>/", customer_view, name="customer_view"),
    path("customers/<int:customer_id>/edit/", customer_edit, name="customer_edit"),
    path("customers/<int:customer_id>/delete/", customer_delete, name="customer_delete"),

    #PRODUCTS
    path("products/", product_list, name="products"),
    path("products/new/", product_create, name="product_create"),
    path("products/<int:product_id>/", product_view, name="product_view"),
    path("products/<int:product_id>/edit/", product_edit, name="product_edit"),
    path("products/<int:product_id>/delete/", product_delete, name="product_delete"),

    #RENEWALS
    path("renewals/", renewal_list, name="renewals"),
    path("renewals/new/", renewal_create, name="renewal_create"),
    path("renewals/<int:renewal_id>/", renewal_view, name="renewal_view"),
    path("renewals/<int:renewal_id>/edit/", renewal_edit, name="renewal_edit"),
    path("renewals/<int:renewal_id>/delete/", renewal_delete, name="renewal_delete"),

    #PASSWORD RESET
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="password-reset.html"), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="password-reset-done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="password-reset-confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="password-reset-complete.html"), name="password_reset_complete"),
    path("password-reset/admin-request/", password_reset_contact_admin, name="password_reset_admin"),
    path("force-password-change/", forced_password_change, name="forced_password_change"),

    #PASSWORD CHANGE
    path("profile/change-password/", change_password, name="change_password"),
    path("users/<int:profile_id>/change-password/", change_user_password, name="change_user_password"),

    #MFA
    path("mfa-verify/", mfa_verify, name="mfa_verify"),

    #ARCHIVE
    path("archive/", renewal_archive_list, name="renewal_archive"),

]