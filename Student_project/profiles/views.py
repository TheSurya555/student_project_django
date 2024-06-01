from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.db import transaction
from .forms import UserProfileForm ,ProjectExperienceForm
from .models import UserProfile ,ProjectExperience
from signUp.models import CustomUser ,RecruiterProfile ,CandidateProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

# profile view
@login_required
def profiles_View(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        print(user_profile)
    except UserProfile.DoesNotExist:
        # Handle the case where the user profile does not exist
        user_profile = UserProfile.objects.create(user=request.user)
        # Optionally, you can redirect the user to an edit profile page or display a message
    profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
    project_experiences = ProjectExperience.objects.filter(user_profile=user_profile)

    return render(request, 'profiles/profiles.html', {'user_profile': user_profile ,'profile_image_url': profile_image_url ,'project_experiences': project_experiences,})

# setting view
@login_required
def settings_View(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully.')
            return redirect('settings')
        else:
            messages.error(request, 'Error updating settings. Please check the form and try again.')
    else:
        form = UserProfileForm(instance=user_profile)
    
    profile = None
    if request.user.role == CustomUser.RECRUITER:
        profile = get_object_or_404(RecruiterProfile, user=request.user)
    elif request.user.role == CustomUser.CANDIDATE:
        profile = get_object_or_404(CandidateProfile, user=request.user)

    context = {
        'custom_user': request.user,
        'form': form,
        'profile': profile,
    }

    return render(request, 'profiles/settings.html', context)


# message view
def messages_View(request):
    return render(request, 'profiles/messages.html')



# profile view
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
                edit_messages = e.message_dict
                form = UserProfileForm(instance=user_profile)
                return render(request, 'profiles/edit_profile.html', {'form': form, 'edit_message': edit_messages })
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'profiles/edit_profile.html', {'form': form})


@login_required
def add_project(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = ProjectExperienceForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user_profile = user_profile  # Assign the current user's profile to the project
            project.save()
            messages.success(request, 'Project added successfully.')
            return redirect('profiles')
        else:
            messages.error(request, 'Error adding project. Please check the form and try again.')
    else:
        form = ProjectExperienceForm()
    return render(request, 'profiles/project_experience.html', {'form': form})
