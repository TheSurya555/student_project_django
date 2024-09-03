from django.contrib import admin
from django.urls import path ,include
from .views import *

urlpatterns = [
    path('', admin_login, name='admin_login'),
    path('dashboard/', dashboard, name='dashboard'),
    # path('admin/logout/', LogoutView.as_view(), name='admin_logout'),
]