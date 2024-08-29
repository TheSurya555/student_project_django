from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import ProjectExperienceForm, EditUserForm, CustomPasswordChangeForm, UserProfileForm
from .models import UserProfile, ProjectExperience, PrivacyPolicy
from signUp.models import CustomUser, RecruiterProfile, CandidateProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from progress_tracker.models import Project
from payment.models import Payment  # Import the Payment model
from django.db.models import Sum

@login_required
def profiles_View(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
    project_experiences = ProjectExperience.objects.filter(user_profile=user_profile)

    # Fetch projects where the logged-in user is the client
    candidate_projects = Project.objects.filter(user=request.user)
    projects = Project.objects.filter(client=request.user)

    # Initialize variables for payments made and received
    total_payments_made = 0
    total_payments_received = 0

    # Handle recruiter payments made
    payments_made = Payment.objects.filter(recruiter=request.user)
    total_payments_made = payments_made.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Handle candidate payments received
    if hasattr(request.user, 'candidateprofile'):
        payments_received = Payment.objects.filter(candidate=request.user.candidateprofile)
        total_payments_received = payments_received.aggregate(Sum('amount'))['amount__sum'] or 0

    # Calculate the current balance
    current_balance = total_payments_made

    return render(request, 'profiles/profiles.html', {
        'user_profile': user_profile,
        'profile_image_url': profile_image_url,
        'project_experiences': project_experiences,
        'projects': projects,
        'candidate_projects': candidate_projects,
        'payments_made': payments_made,  # Pass payments made to the template
        'total_payments_received': total_payments_received,  # Pass the total payments received to the template
        'current_balance': current_balance,  # Pass the current balance to the template
    })



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

    form = EditUserForm(instance=request.user)
    change_passform = CustomPasswordChangeForm(request.user)

    if request.method == 'POST':
        if 'save_changes' in request.POST:
            form = EditUserForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Personal information updated successfully.', extra_tags='settings')
                return redirect('settings')
            else:
                messages.error(request, 'Please correct the errors below.', extra_tags='settings')
        elif 'change_password' in request.POST:
            change_passform = CustomPasswordChangeForm(request.user, request.POST)
            if change_passform.is_valid():
                user = change_passform.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully.', extra_tags='settings')
                return redirect('settings')
            else:
                messages.error(request, 'Please correct the errors below.', extra_tags='settings')

    context = {
        'custom_user': request.user,
        'profile': profile,
        'form': form,
        'change_passform': change_passform,
    }
    return render(request, 'profiles/settings.html', context)

@login_required
def edit_profile_View(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            if 'profile_image' in request.FILES:
                profile_image = request.FILES['profile_image']
                max_filename_length = 1000
                if len(profile_image.name) > max_filename_length:
                    profile_image.name = profile_image.name[:max_filename_length]
                    
            if 'resume' in request.FILES:
                resume_file = request.FILES['resume']
                max_filename_length = 5000
                if len(resume_file.name) > max_filename_length:
                    resume_file.name = resume_file.name[:max_filename_length]
                user_profile.resume = resume_file

            try:
                form.save()
                messages.success(request, 'Profile updated successfully.', extra_tags='edit_profile')
                return redirect('profiles')
            except ValidationError as e:
                edit_messages = e.message_dict
                return render(request, 'profiles/edit_profile.html', {'form': form, 'edit_messages': edit_messages})
        else:
            edit_messages = form.errors
            return render(request, 'profiles/edit_profile.html', {'form': form, 'edit_messages': edit_messages})
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'profiles/edit_profile.html', {'form': form})

@login_required
def add_project(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = ProjectExperienceForm(request.POST)
        if form.is_valid():
            project_experience = form.save(commit=False)
            project_experience.user_profile = user_profile
            project_experience.save()
            messages.success(request, 'Project/Experience added successfully.', extra_tags='add_project')
            return redirect('profiles')
        else:
            messages.error(request, 'Error adding project/experience. Please check the form and try again.', extra_tags='add_project')
    else:
        form = ProjectExperienceForm()
    return render(request, 'profiles/project_experience.html', {'form': form})

@login_required
def delete_project_experience(request, project_experience_id):
    project_experience = get_object_or_404(ProjectExperience, id=project_experience_id)

    if request.method == 'POST':
        project_experience.delete()
        messages.success(request, 'Project experience deleted successfully.', extra_tags='delete_project')
        return redirect('profiles')

    return render(request, 'profiles/confirm_delete.html', {'project_experience': project_experience})

def privacy_policy_view(request):
    privacy_policy = get_object_or_404(PrivacyPolicy)
    return render(request, 'profiles/privacy_policy.html', {'privacy_policy': privacy_policy})
