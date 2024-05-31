from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.db import transaction
from .forms import UserProfileForm ,ProjectExperienceForm
from .models import UserProfile ,ProjectExperience
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

@login_required
def profiles_View(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Handle the case where the user profile does not exist
        user_profile = UserProfile.objects.create(user=request.user)
        # Optionally, you can redirect the user to an edit profile page or display a message
    profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None

    return render(request, 'profiles/profiles.html', {'user_profile': user_profile ,'profile_image_url': profile_image_url})


def settings_View(request):
    return render(request, 'profiles/settings.html')

def messages_View(request):
    return render(request, 'profiles/messages.html')


def edit_profile_View(request):
    try:
        user_profile = get_object_or_404(UserProfile, user=request.user)
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



def project_experience_view(request):
    if request.method == 'POST':
        form = ProjectExperienceForm(request.POST)
        if form.is_valid():
            form.save()
            # Optionally, you can add success message or redirect to a different page
    else:
        form = ProjectExperienceForm()

    # Fetch all project experiences from the database
    project_experiences = ProjectExperience.objects.all()

    return render(request, 'profiles/project_experience.html', {'form': form, 'project_experiences': project_experiences})
