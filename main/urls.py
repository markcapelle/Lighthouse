from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from users.views import login_view, logout_view, dashboard_view, register_view, profile_view, edit_profile, user_management, view_user, edit_user, delete_user


def index(request):
    return render(request, 'index.html')

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('admin/', admin.site.urls),
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("manage-users/", user_management, name="manage_users"),
    path("users/<int:profile_id>/",  view_user, name="view_user"),
    path( "users/<int:profile_id>/edit/", edit_user, name="edit_user"),
    path("users/<int:profile_id>/delete/", delete_user, name="delete_user"),
]