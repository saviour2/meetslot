"""
URL configuration for meetslot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('booking/', views.booking, name='booking'),
    path('status/', views.status, name='status'),
    path('booking/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('booking/accept/<int:booking_id>/', views.accept_reschedule, name='accept_reschedule'),
    path('booking/edit/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('logout/', views.logout_view, name='logout'),
]
