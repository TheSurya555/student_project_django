from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import ProjectExperienceForm, EditUserForm, CustomPasswordChangeForm, UserProfileForm, SocialLinkForm
from .models import UserProfile, ProjectExperience, PrivacyPolicy, SocialLink
from signUp.models import CustomUser, RecruiterProfile, CandidateProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from progress_tracker.models import Project, Progress
from payment.models import Payment
from django.db.models import Sum
from examination.models import Test  # Import the Test model
from progress_tracker.models import Project
from .models import UserProfile, EducationDetail
from .forms import UserProfileForm, EducationDetailForm
from django.forms import modelformset_factory

@login_required
def profiles_View(request):
    # Ensure the user has a profile
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
    
    # Get the user's projects
    candidate_projects = Project.objects.filter(user=request.user)
    client_projects = Project.objects.filter(client=request.user)

    # Aggregate payment data
    payments_made = Payment.objects.filter(recruiter=request.user)
    total_payments_made = payments_made.aggregate(Sum('amount'))['amount__sum'] or 0

    payments_received = None
    total_payments_received = 0
    if hasattr(request.user, 'candidateprofile'):
        payments_received = Payment.objects.filter(candidate=request.user.candidateprofile)
        total_payments_received = payments_received.aggregate(Sum('amount'))['amount__sum'] or 0

    # Calculate current balance
    current_balance = total_payments_made

    # Social Links
    social_links = SocialLink.objects.filter(user_profile=user_profile)

    # Education Details............................
    education_details = EducationDetail.objects.filter(user_profile=user_profile)
    
    # Fetch score and level
    score = Test.fetch_latest_score(request.user) if hasattr(request.user, 'candidate_profile') else None
    completed_projects_count = candidate_projects.filter(status='terminated').count()

    level = "Beginner"  # Default level
    
    if score is not None:
        if score > 80:
            if completed_projects_count >= 5:
                level = "Level 4"
            elif completed_projects_count >= 3:
                level = "Level 3"
            elif completed_projects_count >= 1:
                level = "Level 2"
            else:
                level = "Level 1"
        else:
            level = "Beginner"

    # Update level in profile
    user_profile.level = level
    user_profile.save()
    

    # Check if all stages are completed and confirmed for the user's projects
    all_stages_completed = True
    for project in candidate_projects:
        progresses = Progress.objects.filter(project=project)
        # Check if all stages for this project are completed and confirmed
        if progresses.filter(is_completed=True, client_confirmation=True).count() != progresses.count():
            all_stages_completed = False
            break

    # Count the number of completed projects
    completed_projects_count = candidate_projects.filter(status='terminated').count()

    # Identify user roles (ensures values are always defined)
    role = getattr(request.user, 'role', None)
    is_candidate = role == 'candidate'
    is_recruiter = role == 'recruiter'
    is_admin = role == 'admin'

    return render(request, 'profiles/profiles.html', {
        'user_profile': user_profile,
        'profile_image_url': profile_image_url,
        'project_experiences': ProjectExperience.objects.filter(user_profile=user_profile),
        'projects': client_projects,
        'candidate_projects': candidate_projects,
        'payments_made': payments_made,
        'total_payments_received': total_payments_received,
        'current_balance': current_balance,
        'social_links': social_links,
        'education_details': education_details,
        'level': level if is_candidate else None,
        'score': score if is_candidate else None,
        'is_candidate': is_candidate,
        'is_recruiter': is_recruiter,
        'is_admin': is_admin,
        'all_stages_completed': all_stages_completed,  # Pass the completion status to the template
        'completed_projects_count': completed_projects_count, # Display count of completed projects
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
    
    profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None

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
        'profile_image_url':profile_image_url
    }
    return render(request, 'profiles/settings.html', context)

@login_required
def edit_profile_View(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)

    profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None        

    # Create a formset for EducationDetail
    EducationFormSet = modelformset_factory(EducationDetail, form=EducationDetailForm, extra=0, can_delete=True)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        
        education_formset = EducationFormSet(request.POST, queryset=EducationDetail.objects.filter(user_profile=user_profile))
        
        
        if form.is_valid() and education_formset.is_valid():
            # Handle file naming for profile image and resume
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
                
                # Save education formset
                education_instances = education_formset.save(commit=False)
                for instance in education_instances:
                    instance.user_profile = user_profile
                    instance.save()
                education_formset.save()
                
                messages.success(request, 'Profile updated successfully.', extra_tags='edit_profile')
                return redirect('profiles')
            except ValidationError as e:
                edit_messages = e.message_dict
                return render(request, 'profiles/edit_profile.html', {'form': form, 'edit_messages': edit_messages,'education_formset': education_formset,})
        else:
            # edit_messages = form.errors
            edit_messages = form.errors if not form.is_valid() else education_formset.errors
            return render(request, 'profiles/edit_profile.html', {'form': form, 'edit_messages': edit_messages, 'education_formset': education_formset})
    else:
        form = UserProfileForm(instance=user_profile)
        #eduction
        education_formset = EducationFormSet(queryset=EducationDetail.objects.filter(user_profile=user_profile))

    return render(request, 'profiles/edit_profile.html', {'form': form , 'profile_image_url':profile_image_url,'education_formset': education_formset,})

@login_required
def add_project(request):
    profile_image_url = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None
    
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
    return render(request, 'profiles/project_experience.html', {'form': form ,'profile_image_url':profile_image_url})

@login_required
def update_project(request, experience_id=None):
    profile_image_url = None
    user_profile = None

    # Fetch user profile and profile image
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None

    # If experience_id is provided, fetch the existing project experience
    if experience_id:
        project_experience = get_object_or_404(ProjectExperience, id=experience_id, user_profile=user_profile)
    else:
        project_experience = None

    if request.method == 'POST':
        form = ProjectExperienceForm(request.POST, instance=project_experience)
        if form.is_valid():
            project_experience = form.save(commit=False)
            project_experience.user_profile = user_profile
            project_experience.save()
            if experience_id:
                messages.success(request, 'Project experience updated successfully.', extra_tags='update_project')
            else:
                messages.success(request, 'Project experience added successfully.', extra_tags='add_project')
            return redirect('profiles')
        else:
            messages.error(request, 'Error processing the form. Please check and try again.', extra_tags='project_error')
    else:
        form = ProjectExperienceForm(instance=project_experience)

    return render(request, 'profiles/project_experience.html', {
        'form': form,
        'profile_image_url': profile_image_url,
        'project_experience': project_experience
    })            
    
@login_required
def delete_project_experience(request, project_experience_id):
    project_experience = get_object_or_404(ProjectExperience, id=project_experience_id)

    profile_image_url = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None  

    if request.method == 'POST':
        project_experience.delete()
        messages.success(request, 'Project experience deleted successfully.', extra_tags='delete_project')
        return redirect('profiles')

    return render(request, 'profiles/confirm_delete.html', {'project_experience': project_experience ,'profile_image_url':profile_image_url})

def add_social_link(request):
    if request.method == 'POST':
        form = SocialLinkForm(request.POST)
        if form.is_valid():
            social_link = form.save(commit=False)
            social_link.user_profile = request.user.userprofile  # Assuming the user has a UserProfile
            social_link.save()
            return redirect('profiles')  # Redirect to the user's profile or any other page
    else:
        form = SocialLinkForm()
        
    profile_image_url = None
    
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None        
    context={
        'form': form,
        'profile_image_url':profile_image_url,
    }            

    return render(request, 'profiles/add_social_link.html', context)


def update_social_link(request, platform):
    social_link = get_object_or_404(SocialLink, platform=platform, user_profile=request.user.userprofile)

    if request.method == 'POST':
        new_link = request.POST.get('link')
        if new_link:  # Ensure the input is not empty
            social_link.link = new_link
            social_link.save()
            return redirect('profiles')  # Redirect after saving

    return render(request, 'profiles/update_social_link.html', {'social_link': social_link})

def privacy_policy_view(request):
    profile_image_url = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None
     
    privacy_policy = get_object_or_404(PrivacyPolicy)
    return render(request, 'profiles/privacy_policy.html', {'privacy_policy': privacy_policy ,'profile_image_url':profile_image_url})
