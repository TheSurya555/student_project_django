from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .forms import UserProfileForm
from .models import UserProfile
from django.core.exceptions import ValidationError


def profiles_View(request):
    if request.user.is_authenticated:
        user = request.user
        user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'profiles/profiles.html', {'user_profile': user_profile , 'user': user})


def settings_View(request):
    return render(request, 'profiles/settings.html')

def messages_View(request):
    return render(request, 'profiles/messages.html')


def edit_profile_View(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)
        
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            # Check if a file is uploaded for the profile image
            if 'profile_image' in request.FILES:
                profile_image = request.FILES['profile_image']
                # Truncate or rename the filename if it exceeds the limit
                max_filename_length = 1000
                if len(profile_image.name) > max_filename_length:
                    profile_image.name = profile_image.name[:max_filename_length]
            try:
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('profiles')  # Redirect to the profile view after successful update
            except ValidationError as e:
                error_messages = e.message_dict
                form = UserProfileForm(instance=user_profile)
                return render(request, 'profiles/edit_profile.html', {'form': form, 'error_messages': error_messages})
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'profiles/edit_profile.html', {'form': form})