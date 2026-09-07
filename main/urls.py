from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from users.views import login_view, logout_view, dashboard_view, register_view

def index(request):
    return render(request, 'index.html')

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('admin/', admin.site.urls),
]