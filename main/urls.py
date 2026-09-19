from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from users.views import login_view, logout_view, dashboard_view, register_view, profile_view, edit_profile, user_management, view_user, edit_user, delete_user
from customers.views import customer_list, customer_create, customer_view, customer_edit, customer_delete
from django.contrib.auth import views as auth_views


def index(request):
    return render(request, 'index.html')


urlpatterns = [
    path('', index, name='index'),

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

    #PASSWORD RESET
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="password-reset.html"), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="password-reset-done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="password-reset-confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="password-reset-complete.html"), name="password_reset_complete"),
]