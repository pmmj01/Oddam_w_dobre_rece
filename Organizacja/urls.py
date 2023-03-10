"""Organizacja URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from charytatywna.views import *
from django.contrib.auth import views as auth_views
from django.views.decorators.http import require_http_methods

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('admin/', AdminPanel.as_view(), name='admin_page'),
    path('', LandingPageView.as_view(), name='landing_page'),
    path('add_donation/', AddDonationView.as_view(), name='add_donation'),
    path('donation/', DonationSuccessView.as_view(), name='success'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/details/', UserDetails.as_view(), name='user_details'),
    path('user/update/', UserUpdate.as_view(), name='user_update'),
    path('user/change_password/', ChangePassword.as_view(), name='change_password'),
    path('user/list/', UserListView.as_view(), name='user_list'),
    path('user/edit/<int:id>/', UserEditView.as_view(), name='user_edit'),
    path('user/delete/<int:id>/', UserDeleteView.as_view(), name='user_delete'),
    path('user/<int:id>/delete/', UserListView.as_view(), name='user_list_delete'),
    path('user/<int:id>/edit/', UserListView.as_view(), name='user_list_edit'),
]
