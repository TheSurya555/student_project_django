from .views import admin_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect ,get_object_or_404


@login_required
@admin_required
def profile(request):
    return render(request, 'admin_customization/profile/profile.html')