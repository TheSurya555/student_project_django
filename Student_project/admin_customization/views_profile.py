from .views import admin_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from profiles.models import *
from .specific_forms.forms_profiles import *
from notifications.models import Notification

@login_required
@admin_required
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None        
    
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')[:5]
    context ={
        'user_profile': user_profile,
        'profile_image_url': profile_image_url,
        'notifications': notifications,
    }
    return render(request, 'admin_customization/profile/profile.html',context)


@login_required
@admin_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')  # Redirect to profile view after update
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_profile': user_profile,
    }
    return render(request, 'admin_customization/profile/edit_profile.html', context)
