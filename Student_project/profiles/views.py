from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import ProjectExperienceForm ,EditUserForm ,CustomPasswordChangeForm ,UserProfileForm
from .models import UserProfile ,ProjectExperience
from signUp.models import CustomUser ,RecruiterProfile ,CandidateProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

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


@login_required
def settings_View(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    profile = None
    if request.user.role == CustomUser.RECRUITER:
        profile = get_object_or_404(RecruiterProfile, user=request.user)
    elif request.user.role == CustomUser.CANDIDATE:
        profile = get_object_or_404(CandidateProfile, user=request.user)

    if request.method == 'POST':
        if 'save_changes' in request.POST:
            form = EditUserForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Settings updated successfully.')
                return redirect('settings')
            else:
                messages.error(request, 'Error updating settings. Please check the form and try again.')
        elif 'change_password' in request.POST:
            change_passform = CustomPasswordChangeForm(request.user, request.POST)
            if change_passform.is_valid():
                change_passform.save()
                update_session_auth_hash(request, request.user)  # Update the session with the new password hash
                messages.success(request, 'Your password has been changed successfully!')
                return redirect('settings')
            else:
                messages.error(request, 'Please correct the error below.')
    else:
        form = EditUserForm(instance=request.user)
        change_passform = CustomPasswordChangeForm(request.user)

    context = {
        'custom_user': request.user,
        'form': form,
        'profile': profile,
        'change_passform': change_passform,
    }

    return render(request, 'profiles/settings.html', context)



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


def privacy_policy_view(request):
    return render(request, 'profiles/privacy_policy.html')